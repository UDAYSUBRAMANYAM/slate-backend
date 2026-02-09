from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from datetime import datetime
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Knowledge(Base):
    __tablename__ = "knowledge"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    type = Column(String)  # note | link | insight
    source_url = Column(String, nullable=True)

    tags = Column(JSON, default=[])
    ai_summary = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
