from sqlalchemy import Column, String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from app.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration"""
    ADMIN = "ADMIN"
    SALES = "SALES"
    INSTRUCTOR = "INSTRUCTOR"
    MENTOR = "MENTOR"
    STUDENT = "STUDENT"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    role = Column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.STUDENT
    )
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    enrollments = relationship("Enrollment", back_populates="student")
    created_bootcamps = relationship("Bootcamp", back_populates="instructor")
    assignments = relationship("Assignment", back_populates="instructor")
    leads = relationship("Lead", back_populates="user")

    def __repr__(self):
        return f"<User {self.email}>"
