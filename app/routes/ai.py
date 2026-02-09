from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import Knowledge
from app.core.deps import get_db, get_current_user
from app.services.ai_service import (
    summarize_knowledge,
    auto_tag_knowledge,
    ask_knowledge_base,
)

router = APIRouter(tags=["AI"])

@router.post("/knowledge/{id}/summarize")
def summarize(
    id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    knowledge = db.query(Knowledge).filter(
        Knowledge.id == id,
        Knowledge.user_id == user.id
    ).first()

    if not knowledge:
        raise HTTPException(status_code=404, detail="Knowledge not found")

    summary = summarize_knowledge(db, knowledge)
    return {"summary": summary}


@router.post("/knowledge/{id}/auto-tag")
def auto_tag(
    id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    knowledge = db.query(Knowledge).filter(
        Knowledge.id == id,
        Knowledge.user_id == user.id
    ).first()

    if not knowledge:
        raise HTTPException(status_code=404, detail="Knowledge not found")

    tags = auto_tag_knowledge(db, knowledge)
    return {"tags": tags}


@router.post("/knowledge/ask")
def ask(
    question: str,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
):
    answer = ask_knowledge_base(db, user.id, question)
    return {"answer": answer}
