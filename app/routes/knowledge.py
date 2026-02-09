from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.models import Knowledge
from app.schemas.knowledge import KnowledgeCreate, KnowledgeResponse
from app.core.deps import get_db, get_current_user

router = APIRouter(prefix="/knowledge", tags=["Knowledge"])

@router.post("", response_model=KnowledgeResponse)
def create_knowledge(
    data: KnowledgeCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    item = Knowledge(
        user_id=user.id,
        **data.dict()
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("", response_model=list[KnowledgeResponse])
def get_all_knowledge(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return db.query(Knowledge).filter(Knowledge.user_id == user.id).all()

@router.get("/{id}", response_model=KnowledgeResponse)
def get_knowledge(
    id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    item = db.query(Knowledge).filter(
        Knowledge.id == id,
        Knowledge.user_id == user.id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Knowledge not found")

    return item

@router.put("/{id}", response_model=KnowledgeResponse)
def update_knowledge(
    id: int,
    data: KnowledgeCreate,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    item = db.query(Knowledge).filter(
        Knowledge.id == id,
        Knowledge.user_id == user.id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Knowledge not found")

    for key, value in data.dict().items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item

@router.delete("/{id}")
def delete_knowledge(
    id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    item = db.query(Knowledge).filter(
        Knowledge.id == id,
        Knowledge.user_id == user.id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Knowledge not found")

    db.delete(item)
    db.commit()
    return {"message": "Knowledge deleted"}
