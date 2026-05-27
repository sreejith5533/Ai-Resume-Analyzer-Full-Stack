from pypdf import PdfReader
from pathlib import Path
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .ai_service import get_ai_resume_analysis
from .models import Resume


def home_view(request):
    found_skills = []
    jd_skills = []
    matching_skills = []
    missing_skills = []

    score = 0
    label_text = ""
    sub_text = ""
    is_submitted = False
    suggestions = []
    file_name = ""

    if request.method == "POST":
        is_submitted = True

        name = request.POST.get("name")
        file = request.FILES.get("file")
        role = request.POST.get("role")
        job_description = request.POST.get("job_description", "").strip()

        if not file:
            return render(request, "home.html", {"error": "Please upload a PDF file"})

        if not job_description:
            return render(request, "home.html", {"error": "Please enter job description"})

        resume = Resume.objects.create(
            name=name,
            file=file,
            role=role,
            job_description=job_description,
        )

        resume_path = resume.file.path
        file_name = Path(resume_path).name

        text = ""
        with open(resume_path, "rb") as f:
            pdf = PdfReader(f)
            for page in pdf.pages:
                text += page.extract_text() or ""

        resume_text = text.lower()
        resume.extracted_text = resume_text

        result = get_ai_resume_analysis(resume_text, job_description.lower())

        found_skills = result.get("resume_skills", [])
        jd_skills = result.get("jd_skills", [])
        matching_skills = result.get("matching_skills", [])
        missing_skills = result.get("missing_skills", [])
        score = result.get("score", 0)
        ai_suggestions = result.get("suggestions", [])
        analysis_source = result.get("source", "unknown")

        print("Analysis source:", analysis_source)

        resume.found_skills = ", ".join(found_skills)
        resume.jd_skills = ", ".join(jd_skills)
        resume.matching_skills = ", ".join(matching_skills)
        resume.missing_skills = ", ".join(missing_skills)
        resume.score = score
        resume.save()

        if score > 80:
            label_text = "Excellent Profile"
            sub_text = "You are a perfect fit for this role."
        elif score > 60:
            label_text = "Good Profile"
            sub_text = "You are a good fit for this role."
        elif score > 40:
            label_text = "Average Profile"
            sub_text = "You are an average fit for this role."
        else:
            label_text = "Needs Improvement"
            sub_text = "You are not a good fit for this role."

        suggestions = []

        for item in ai_suggestions[:4]:
            suggestions.append(
                {
                    "title": "AI Suggestion",
                    "description": item,
                    "type": "info",
                }
            )

        contain_digit = any(char.isdigit() for char in resume_text)
        if not contain_digit:
            suggestions.append(
                {
                    "title": "Add measurable impact to your resume",
                    "description": "Include numbers like percentages, team size, users served, or time saved to strengthen your resume.",
                    "highlight": "Tip: Use numbers like 20%, 5+ projects, 1000 users",
                    "type": "warning",
                }
            )

        project_words = ["project", "developed", "built", "created"]
        contain_project = any(word in resume_text for word in project_words)

        if not contain_project:
            suggestions.append(
                {
                    "title": "Add project details",
                    "description": "Mention project work clearly to show your practical skills.",
                    "highlight": "Tip: Add project name, tech stack, and your role",
                    "type": "warning",
                }
            )

        if len(resume_text.split()) < 150:
            suggestions.append(
                {
                    "title": "Resume needs strong revision",
                    "description": "Your resume looks too short. Add more useful content, skills, and project details.",
                    "type": "warning",
                }
            )

        suggestions = suggestions[:3]

    resumes = Resume.objects.all()

    return render(
        request,
        "home.html",
        {
            "resumes": resumes,
            "found_skills": found_skills,
            "jd_skills": jd_skills,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "score": score,
            "label_text": label_text,
            "sub_text": sub_text,
            "is_submitted": is_submitted,
            "suggestions": suggestions,
            "file_name": file_name,
        },
    )


def history_view(request):
    query = request.GET.get("q")
    resume_list = Resume.objects.all().order_by("-uploaded_at")

    if query:
        resume_list = Resume.objects.filter(name__icontains=query).order_by("-uploaded_at")

    paginator = Paginator(resume_list, 6)
    page_number = request.GET.get("page")
    resumes = paginator.get_page(page_number)

    return render(request, "history.html", {"resumes": resumes})


def delete_resume(request, id):
    resume = get_object_or_404(Resume, id=id)
    resume.delete()
    return redirect("history")


def delete_all(request):
    resumes = Resume.objects.all()
    resumes.delete()
    return redirect("history")


def resume_details(request, id):
    resume = get_object_or_404(Resume, id=id)

    found_skills = resume.found_skills.split(", ") if resume.found_skills else []
    jd_skills = resume.jd_skills.split(", ") if resume.jd_skills else []
    matching_skills = resume.matching_skills.split(", ") if resume.matching_skills else []
    missing_skills = resume.missing_skills.split(", ") if resume.missing_skills else []

    context = {
        "resume": resume,
        "found_skills": found_skills,
        "jd_skills": jd_skills,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
    }

    return render(request, "resume_details.html", context)