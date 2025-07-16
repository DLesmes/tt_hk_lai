from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.sqlite import UUID
from sqlalchemy.sql import func
import uuid
from .database import Base

class User(Base):
    """User model for storing user and role data"""
    
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(String(255), unique=True, nullable=False)
    role = Column(String(10), nullable=False)  # 'driver' or 'user'
    conversation_id = Column(UUID(as_uuid=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, session_id={self.session_id}, role={self.role})>" 