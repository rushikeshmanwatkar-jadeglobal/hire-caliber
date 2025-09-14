import json
import numpy as np
from openai import AsyncAzureOpenAI
from backend.app.core.config import settings

# Initialize Azure OpenAI client
client = AsyncAzureOpenAI(
    api_key=settings.AZURE_OPENAI_API_KEY,
    api_version=settings.OPENAI_API_VERSION,
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
)


async def get_embedding(text: str) -> list[float]:
    """Generates embeddings for a given text using Azure OpenAI."""
    response = await client.embeddings.create(
        input=text, model=settings.EMBEDDING_MODEL_NAME
    )
    return response.data[0].embedding


async def standardize_resume(raw_text: str) -> dict:
    """Uses a chat model to parse and standardize resume text into a detailed JSON format."""

    # Updated system prompt to guide the LLM for a more structured output.
    system_prompt = """
    You are an expert HR data analyst specializing in parsing resumes. Your task is to extract and structure information from the provided resume text into a specific JSON format.

    The JSON output must be a single, valid JSON object with the following keys: "personal_info", "summary", "technical_skills", "work_experience", "education", and "certifications".

    Follow these instructions for each key:
    - "personal_info": An object containing the candidate's "name" and "title" (e.g., 'AWS Devops').
    - "summary": Professional summary, summarizing the candidate's core expertise and years of experience.
    - "technical_skills": An object where each key is a skill category as listed in the resume (e.g., "Operating Systems", "SCM Tools", "Cloud"). The value for each key must be a list of strings, where each string is a specific skill.
    - "work_experience": A list of objects, where each object represents a job. Each job object must have:
        - "title": The job title(s) held at the company.
        - "company": The name of the company.
        - "duration": The employment period (e.g., "Nov 2018 - Jul 2021").
        - "projects": A list of objects, where each object represents a project worked on during that job. Each project object must contain:
            - "name": The name of the project.
            - "description": A brief, 1-2 sentence description of the project.
            - "responsibilities": A list of strings, with each string being a specific task, duty, or accomplishment from the resume.
    - "education": A list of objects, where each object has "degree" and "institution".
    - "certifications": A list of strings, each string being a certificate name.

    IMPORTANT: Do not include any personal contact information (email, phone, address). Do not add any explanatory text or markdown formatting before or after the JSON object.
    """

    response = await client.chat.completions.create(
        model=settings.CHAT_MODEL_NAME,  # Your actual model
        # model="gpt-4-turbo",  # Example model
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Here is the resume text:\n\n{raw_text}"},
        ],
    )

    try:
        return json.loads(response.choices[0].message.content)
    except (json.JSONDecodeError, IndexError, AttributeError):
        return {"error": "Failed to parse resume content from LLM response"}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise e


def calculate_cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    """Calculates the cosine similarity between two embedding vectors."""
    dot_product = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    similarity = dot_product / (norm_a * norm_b)
    return float(similarity)


def create_summary_from_profile(profile: dict) -> str:
    """Creates a concise text summary from a standardized profile for embedding."""
    summary = profile.get("summary", "")
    skills = ", ".join(profile.get("skills", []))
    return f"Professional Summary: {summary}\nKey Skills: {skills}"
