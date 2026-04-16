import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path=".env", override=True)
print("GROQ KEY:", os.getenv("GROQ_API_KEY"))

import json
import re
from chains.extract_chain import extract_chain
from chains.match_chain import match_chain
from chains.score_chain import score_chain
from chains.explain_chain import explain_chain
from utils.matcher import match_skills

# -------------------------------
# Helper function to safely parse JSON
# -------------------------------
def safe_json_parse(text):
    try:
        # extract JSON from messy output
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return text
    except:
        return text

# -------------------------------
# Main Pipeline Function
# -------------------------------
def run_pipeline(resume, job_description, candidate_type="Candidate"):

    print(f"\n================ {candidate_type.upper()} ================")

    print("RESUME LENGTH:", len(resume))

    # STEP 1: EXTRACTION
    print("\n🔹 STEP 1: SKILL EXTRACTION")
    extracted = extract_chain.invoke({"resume": resume})
    extracted_data = safe_json_parse(extracted.content)
    print(extracted_data)

    # STEP 2: PYTHON MATCHING (FIXED)
    print("\n🔹 STEP 2: MATCHING (PYTHON LOGIC)")
    print("DEBUG JD TYPE:", type(job_description))
    match_data = match_skills(extracted_data, job_description)
    print(match_data)

    # STEP 3: SCORING (EXPLICIT DISPLAY)
    print("\n🔹 STEP 3: SCORING")
    score = match_data["score"]
    print("Score:", score)

    # STEP 4: EXPLANATION (LLM ONLY)
    print("\n🔹 STEP 4: EXPLANATION")
    explanation = explain_chain.invoke({
        "resume_data": extracted_data,
        "match_data": match_data
    })

    print(explanation.content)

    return {
        "match_data": match_data,
        "explanation": explanation.content
    }


# -------------------------------
# File Loader
# -------------------------------
def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# -------------------------------
# MAIN EXECUTION
# -------------------------------
if __name__ == "__main__":

    # Load Job Description
    jd=json.loads(load_file("data/job_description.json"))

    # Load Resumes
    strong_resume = load_file("data/strong_resume.txt")
    avg_resume = load_file("data/average_resume.txt")
    weak_resume = load_file("data/weak_resume.txt")

    # Run Pipeline for all candidates
    run_pipeline(strong_resume, jd, "Strong Candidate")
    run_pipeline(avg_resume, jd, "Average Candidate")
    run_pipeline(weak_resume, jd, "Weak Candidate")