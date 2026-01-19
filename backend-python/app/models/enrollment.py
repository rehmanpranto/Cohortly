from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from app.database import Base


class EnrollmentStatus(str, enum.Enum):
    """Enrollment status enumeration"""
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    DROPPED = "DROPPED"
    PENDING = "PENDING"


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    bootcamp_id = Column(UUID(as_uuid=True), ForeignKey('bootcamps.id'), nullable=False)
    status = Column(
        Enum(EnrollmentStatus),
        default=EnrollmentStatus.ACTIVE,
        nullable=False
    )
    enrolled_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    student = relationship("User", back_populates="enrollments")
    bootcamp = relationship("Bootcamp", back_populates="enrollments")

    def __repr__(self):
        return f"<Enrollment student={self.student_id} bootcamp={self.bootcamp_id}>"
