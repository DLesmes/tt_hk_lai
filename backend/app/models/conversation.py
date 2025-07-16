from sqlalchemy import Column, String, DateTime, Text, Boolean
from sqlalchemy.dialects.sqlite import UUID
from sqlalchemy.sql import func
import uuid
from .database import Base

class Conversation(Base):
    """Conversation model for storing conversation data"""
    
    __tablename__ = "conversations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role = Column(String(10), nullable=False)  # 'driver' or 'user'
    status = Column(String(20), nullable=False, default='active')  # 'active', 'completed', 'failed'
    origin = Column(String(255))
    destination = Column(String(255))
    timestamp_of_anomaly = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Conversation(id={self.id}, role={self.role}, status={self.status})>" 