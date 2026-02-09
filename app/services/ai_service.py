from sqlalchemy.orm import Session
from app.db.models import Knowledge
from app.core.ai_provider import ai_provider

def summarize_knowledge(db: Session, knowledge: Knowledge) -> str:
    try:
        summary = ai_provider.summarize(knowledge.content)
    except Exception:
        summary = "Summary unavailable (AI fallback mode)"

    knowledge.ai_summary = summary
    db.commit()
    return summary


def auto_tag_knowledge(db: Session, knowledge: Knowledge) -> list[str]:
    try:
        tags = ai_provider.auto_tag(knowledge.content)
    except Exception:
        tags = []

    knowledge.tags = tags
    db.commit()
    return tags


def ask_knowledge_base(db: Session, user_id: int, question: str) -> str:
    notes = db.query(Knowledge).filter(
        Knowledge.user_id == user_id
    ).all()

    context = "\n".join(
        [n.ai_summary or n.content for n in notes]
    )

    try:
        return ai_provider.ask(question, context)
    except Exception:
        return "AI is temporarily unavailable."
