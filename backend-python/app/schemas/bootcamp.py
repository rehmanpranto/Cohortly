"""
Bootcamp schemas for request/response validation
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from app.models.bootcamp import BootcampStatus


class BootcampCreate(BaseModel):
    """Schema for creating a bootcamp"""
    name: str = Field(..., min_length=3, max_length=200)
    description: str = Field(..., min_length=10)
    start_date: datetime
    end_date: datetime
    duration_weeks: int = Field(..., ge=1, le=104)  # 1 week to 2 years
    max_students: int = Field(default=30, ge=1, le=200)
    status: BootcampStatus = Field(default=BootcampStatus.DRAFT)


class BootcampUpdate(BaseModel):
    """Schema for updating a bootcamp"""
    name: Optional[str] = Field(None, min_length=3, max_length=200)
    description: Optional[str] = Field(None, min_length=10)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    duration_weeks: Optional[int] = Field(None, ge=1, le=104)
    max_students: Optional[int] = Field(None, ge=1, le=200)
    status: Optional[BootcampStatus] = None


class BootcampResponse(BaseModel):
    """Schema for bootcamp response"""
    id: str
    name: str
    description: str
    instructor_id: str
    start_date: datetime
    end_date: datetime
    duration_weeks: int
    max_students: int
    status: BootcampStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BootcampListResponse(BaseModel):
    """Schema for list of bootcamps"""
    bootcamps: List[BootcampResponse]
    total: int
    page: int
    page_size: int
