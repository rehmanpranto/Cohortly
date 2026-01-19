"""
Assignment schemas for request/response validation
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class AssignmentCreate(BaseModel):
    """Schema for creating an assignment"""
    bootcamp_id: str
    title: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10)
    due_date: datetime
    points: str = Field(default="100")


class AssignmentUpdate(BaseModel):
    """Schema for updating an assignment"""
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    due_date: Optional[datetime] = None
    points: Optional[str] = None


class AssignmentResponse(BaseModel):
    """Schema for assignment response"""
    id: str
    bootcamp_id: str
    instructor_id: str
    title: str
    description: str
    due_date: datetime
    points: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AssignmentListResponse(BaseModel):
    """Schema for list of assignments"""
    assignments: List[AssignmentResponse]
    total: int
    page: int
    page_size: int
