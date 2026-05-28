import json
import os
import re

import requests
from dotenv import load_dotenv



load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
print("API KEY", API_KEY)

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
    print("Function Started")
    resume_text = resume_text[:4000]
    job_description = job_description[:3000]

    try :
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers ={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "nvidia/nemotron-3-super-120b-a12b:free",
                "messages": [
                    {
                        "role" : "system",
                        "content" : (
                            "You are an ATS Resume Analyzer. "
                            "Return only clean valid JSON."
                        )
                    },
                    {
                        "role" : "user",
                        "content" : f"""
Resume : {resume_text}
Job Description : {job_description}


Return JSON only :
{{
    "resume_skills" : [],
    "jd_skills" :  [],
    "matching_skills" : [],
    "missing_skills" : [],
    "score" : 0,
    "suggestions" : [],
    "source"  :  "ai"
}}
"""
                    }
                ],
                "temperature": 0.3
            },
            timeout=20
        )

        print("After api call")

        print("status:", response.status_code)
        print("text:", response.text)
        print("json:", response.json())
        data = response.json()
        if "choices" not in data :
            print("No choices found")
            return build_fallback_analysis(resume_text,job_description)
        ai_content = data['choices'][0]['message']['content']
        cleaned_json = ai_content.strip()
        cleaned_json = cleaned_json.replace("```json", "")
        cleaned_json = cleaned_json.replace("```", "")
        cleaned_json = cleaned_json.strip()
        result = json.loads(cleaned_json)
        return result
    except Exception as e:
        print("\nERROR OCCURED")
        print(type(e))
        print(e)

        raise

        
  