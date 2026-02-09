import os
from typing import List

# ----------------------------
# Base Provider
# ----------------------------

class AIProvider:
    def summarize(self, text: str) -> str:
        raise NotImplementedError

    def auto_tag(self, text: str) -> List[str]:
        raise NotImplementedError

    def ask(self, question: str, context: str) -> str:
        raise NotImplementedError


# ----------------------------
# OpenAI Provider
# ----------------------------

class OpenAIProvider(AIProvider):
    def __init__(self):
        from openai import OpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not found")

        self.client = OpenAI(api_key=api_key)

    def summarize(self, text: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Summarize the following knowledge clearly and concisely."},
                {"role": "user", "content": text},
            ],
        )
        return response.choices[0].message.content.strip()

    def auto_tag(self, text: str) -> List[str]:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Generate 5 short, relevant tags as a comma-separated list. "
                        "No explanations."
                    ),
                },
                {"role": "user", "content": text},
            ],
        )
        return [t.strip() for t in response.choices[0].message.content.split(",")]

    def ask(self, question: str, context: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Answer ONLY using the user's private knowledge context.",
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context}\n\nQuestion:\n{question}",
                },
            ],
        )
        return response.choices[0].message.content.strip()


# ----------------------------
# Stub Provider (Fallback)
# ----------------------------

class StubAIProvider(AIProvider):
    def summarize(self, text: str) -> str:
        return f"[Stub Summary] {text[:200]}..."

    def auto_tag(self, text: str) -> List[str]:
        return list(set(text.lower().split()[:5]))

    def ask(self, question: str, context: str) -> str:
        return "[Stub Answer] AI unavailable. Showing context-based response."


# ----------------------------
# Provider Selector
# ----------------------------

def get_ai_provider() -> AIProvider:
    provider = os.getenv("AI_PROVIDER")

    if provider == "openai":
        try:
            return OpenAIProvider()
        except Exception:
            pass  # fallback safely

    return StubAIProvider()


ai_provider = get_ai_provider()
