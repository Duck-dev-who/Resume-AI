from http.client import HTTPException
import os
import json
from urllib import response
from dotenv import load_dotenv
from google import genai

load_dotenv()
print("API Key:", os.getenv("GEMINI_API_KEY"))
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

try:
    analysis = json.loads(response.text)
except json.JSONDecodeError:
    raise HTTPException(
        status_code=500,
        detail="AI returned invalid JSON."
    )

async def analyze_resume(resume_text: str):
    """
    Analyze the extracted resume text.
    """

    # Build the prompt
    prompt = f"""
You are an experienced hiring manager, ATS specialist, and professional resume reviewer.

Your job is to evaluate the following resume for an ENTRY-LEVEL position using ONLY the information provided.

Evaluate the resume based on these categories:

- Resume Structure (20 points)
- Grammar & Spelling (20 points)
- Work Experience (20 points)
- Skills (20 points)
- Overall Presentation (20 points)

Calculate the Overall Resume Score by summing the category scores.

Also provide:

- Strengths
- Weaknesses
- Missing Skills
- Actionable Suggestions
- Career Recommendations
- Estimated ATS Compatibility Score
- ATS Feedback
- Hiring Recommendation
- Three interview questions you would ask this candidate

Return ONLY valid JSON using this EXACT structure:

{{
    "overall_score": number,

    "score_breakdown": {{
        "structure": {{
            "score": number,
            "max_score": 20,
            "deductions": [
                "..."
            ]
        }},
        "grammar": {{
            "score": number,
            "max_score": 20,
            "deductions": [
                "..."
            ]
        }},
        "experience": {{
            "score": number,
            "max_score": 20,
            "deductions": [
                "..."
            ]
        }},
        "skills": {{
            "score": number,
            "max_score": 20,
            "deductions": [
                "..."
            ]
        }},
        "presentation": {{
            "score": number,
            "max_score": 20,
            "deductions": [
                "..."
            ]
        }}
    }},

    "structure_feedback": "...",
    "clarity_feedback": "...",
    "overall_impression": "...",
    "grammar_feedback": "...",

    "strengths": [
        "...",
        "...",
        "...",
        "...",
        "..."
    ],

    "weaknesses": [
        "...",
        "...",
        "...",
        "...",
        "..."
    ],

    "missing_skills": [
        "...",
        "...",
        "...",
        "...",
        "..."
    ],

    "suggestions": [
        "...",
        "...",
        "...",
        "...",
        "..."
    ],

    "recommended_careers": [
        "...",
        "...",
        "..."
    ],

    "ats": {{
        "score": number,
        "matched_keywords": [
            "..."
        ],
        "missing_keywords": [
            "..."
        ],
        "feedback": "..."
    }},

    "hiring_decision": {{
        "would_hire": true,
        "confidence": number,
        "reasoning": "..."
    }},

    "interview_questions": [
        "...",
        "...",
        "..."
    ],

    "resume_grade": {{
        "letter": "...",
        "summary": "..."
    }}
}}

Rules:

- Return ONLY valid JSON.
- Return EXACTLY ONE JSON object.
- Do NOT include markdown.
- Do NOT wrap the JSON in triple backticks.
- Do NOT include explanations outside the JSON.
- Every array must contain exactly the requested number of items.
- The overall_score must equal the sum of the five category scores.
- confidence must be an integer from 0 to 100.
- ats.score must be an integer from 0 to 100.
- Keep every response concise.
- Base your evaluation ONLY on the resume provided.
- Do not invent qualifications or experience.

Resume:

{resume_text}
"""

    # Send the prompt to Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    print(response)
    analysis = json.loads(response.text)
    
    return analysis