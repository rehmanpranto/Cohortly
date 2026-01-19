from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from app.database import Base


class BootcampStatus(str, enum.Enum):
    """Bootcamp status enumeration"""
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Bootcamp(Base):
    __tablename__ = "bootcamps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    instructor_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    duration_weeks = Column(Integer, nullable=False)
    max_students = Column(Integer, default=30)
    status = Column(
        Enum(BootcampStatus),
        nullable=False,
        default=BootcampStatus.DRAFT
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    instructor = relationship("User", back_populates="created_bootcamps")
    enrollments = relationship("Enrollment", back_populates="bootcamp", cascade="all, delete-orphan")
    assignments = relationship("Assignment", back_populates="bootcamp", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Bootcamp {self.name}>"
