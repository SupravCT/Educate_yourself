import httpx
from src.config import settings


async def run_code(source_code: str, language: str = "python") -> dict:
    payload = {
        "language": language,
        "version": "*",  
        "files": [
            {"content": source_code}
        ],
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.PISTON_API_URL}/execute",
            json=payload,
            timeout=20,
        )
        response.raise_for_status()
        return response.json()