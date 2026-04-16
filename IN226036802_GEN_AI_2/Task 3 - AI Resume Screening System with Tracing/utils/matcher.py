import json

def match_skills(resume_data, job_description):

    # STEP 1: Convert string → dict if needed
    if isinstance(job_description, str):
        try:
            job_description = json.loads(job_description)
        except:
            raise ValueError("Job description is not valid JSON format")

    resume_skills = set(resume_data.get("skills", []))
    job_skills = set(job_description.get("Required Skills", []))

    if not job_skills:
        return {
            "matched_skills": [],
            "missing_skills": [],
            "score": 0
        }

    matched = list(resume_skills & job_skills)
    missing = list(job_skills - resume_skills)

    score = round((len(matched) / len(job_skills)) * 100, 2)

    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "score": score
    }