"""
Enrollment schemas for request/response validation
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.models.enrollment import EnrollmentStatus


class EnrollmentCreate(BaseModel):
    """Schema for creating an enrollment"""
    student_id: str
    bootcamp_id: str
    status: EnrollmentStatus = EnrollmentStatus.PENDING


class EnrollmentUpdate(BaseModel):
    """Schema for updating an enrollment"""
    status: Optional[EnrollmentStatus] = None
    completed_at: Optional[datetime] = None


class EnrollmentResponse(BaseModel):
    """Schema for enrollment response"""
    id: str
    student_id: str
    bootcamp_id: str
    status: EnrollmentStatus
    enrolled_at: datetime
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EnrollmentListResponse(BaseModel):
    """Schema for list of enrollments"""
    enrollments: List[EnrollmentResponse]
    total: int
    page: int
    page_size: int
