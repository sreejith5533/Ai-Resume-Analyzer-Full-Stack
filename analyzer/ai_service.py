import json
import os
import re

import requests
from dotenv import load_dotenv



load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

MASTER_SKILLS = [
    "python",
    "django",
    "flask",
    "fastapi",
    "html",
    "css",
    "javascript",
    "bootstrap",
    "react",
    "mysql",
    "sql",
    "git",
    "github",
    "rest api",
    "api",
    "oop",
    "problem solving",
    "communication",
    "teamwork",
    "leadership",
    "time management",
    "debugging",
]


def extract_skills_from_text(text, skills_list):
    found = []
    text = re.sub(r"\s+", " ", text.lower())

    for skill in skills_list:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text):
            found.append(skill)

    return list(dict.fromkeys(found))


def build_fallback_analysis(resume_text, job_description):
    resume_skills = extract_skills_from_text(resume_text, MASTER_SKILLS)
    jd_skills = extract_skills_from_text(job_description, MASTER_SKILLS)

    matching_skills = [skill for skill in jd_skills if skill in resume_skills]
    missing_skills = [skill for skill in jd_skills if skill not in resume_skills]

    score = int((len(matching_skills) / len(jd_skills)) * 100) if jd_skills else 0

    suggestions = []

    if missing_skills:
        suggestions.append(
            f"Add missing skills like {', '.join(missing_skills[:3])} to your resume."
        )

    if score < 50:
        suggestions.append("Improve resume content based on the job description.")

    if "project" not in resume_text:
        suggestions.append("Add project details to show practical experience.")

    if not suggestions:
        suggestions.append("Your resume matches well. Add more measurable achievements.")

    return {
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "suggestions": suggestions[:3],
        "score": score,
        "source": "fallback",
    }



def get_ai_resume_analysis(resume_text,job_description):
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
                "messages": [
                    {
                        "role": "system",
                        "content" : "You are an ATS analyzer.Return only JSON."
                    },{
                        "role" : "user",
                        "content" : f"""
Resume : {resume_text}

Job Description :
{job_description}

Return JSON only:
{{
    "resume_skills": [],
    "jd_skills": [],
    "matching_skills": [],
    "missing_skills": [],
    "suggestions": [],
    "score": 0
}}
"""
                    }
                ]

            }
        )

        result = response.json()
        ai_text = result["choices"][0]["message"]["content"]
        parsed = json.loads(ai_text)
        parsed["source"] = "ai"

        return parsed
    
    except Exception as e:
        print("AI ERROR",e)
        return {
            "resume_skills": [],
            "jd_skills": [],
            "matching_skills": [],
            "missing_skills": [],
            "suggestions": ["AI failed"],
            "score": 0,
            "source": "fallback"
        }