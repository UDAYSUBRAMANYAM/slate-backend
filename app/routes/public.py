from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.db.models import Knowledge
from app.core.ai_provider import ai_provider

router = APIRouter(prefix="/api/public", tags=["Public Brain"])

@router.get("/brain/query")
def public_brain_query(
    q: str = Query(..., description="Natural language question"),
    db: Session = Depends(get_db),
):
    notes = db.query(Knowledge).filter(
        Knowledge.ai_summary.isnot(None)
    ).all()

    if not notes:
        return {
            "answer": "No knowledge available yet.",
            "sources": []
        }

    context = "\n".join(
        [f"{n.title}: {n.ai_summary}" for n in notes]
    )

    try:
        answer = ai_provider.ask(q, context)
    except Exception:
        answer = "AI unavailable. Showing knowledge-based response."

    sources = [
        {"id": n.id, "title": n.title}
        for n in notes[:5]
    ]

    return {
        "answer": answer,
        "sources": sources
    }
