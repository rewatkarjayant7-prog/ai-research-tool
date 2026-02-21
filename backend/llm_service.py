import os
from openai import OpenAI
from backend.models import EarningsCallSummary
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI Client (this will pick up OPENAI_API_KEY from environment)
# For Gemini compatibility via openai SDK, the user would configure 
# OPENAI_BASE_URL and OPENAI_API_KEY appropriately in the .env file.
client = OpenAI()

SYSTEM_PROMPT = """You are an expert financial analyst. Your task is to extract structured information from the provided earnings call transcript or management commentary.

STRICT RULES:
1. ONLY use the information explicitly found in the provided transcript text.
2. Do NOT guess, infer, or fabricate any information.
3. If specific information for a field is not present in the transcript, you MUST return "Not mentioned in transcript" for that field (or the closest valid enum value like "not_mentioned").
4. Maintain a completely objective, non-conversational tone. Output should be deterministic and analyst-friendly.
5. Your output must exactly match the requested JSON schema.
"""

def analyze_transcript(transcript_text: str) -> dict:
    """
    Sends the transcript to the LLM to extract a structured EarningsCallSummary.
    """
    try:
        response = client.beta.chat.completions.parse(
            model="gemini-2.5-flash", # Use a supported Gemini version
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Here is the transcript:\n\n{transcript_text}"}
            ],
            response_format=EarningsCallSummary,
            temperature=0.0, # Deterministic output
        )
        
        # The parsed Pydantic object
        summary = response.choices[0].message.parsed
        return summary.model_dump()
        
    except Exception as e:
        raise RuntimeError(f"Failed to analyze transcript with LLM: {str(e)}")
