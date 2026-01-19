"""
Lead schemas for request/response validation
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from app.models.lead import LeadStatus


class LeadCreate(BaseModel):
    """Schema for creating a lead"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    source: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None
    status: LeadStatus = LeadStatus.NEW
    assigned_to_id: Optional[str] = None


class LeadUpdate(BaseModel):
    """Schema for updating a lead"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    source: Optional[str] = Field(None, max_length=100)
    notes: Optional[str] = None
    status: Optional[LeadStatus] = None
    assigned_to_id: Optional[str] = None


class LeadResponse(BaseModel):
    """Schema for lead response"""
    id: str
    name: str
    email: str
    phone: Optional[str]
    source: Optional[str]
    notes: Optional[str]
    status: LeadStatus
    assigned_to_id: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class LeadListResponse(BaseModel):
    """Schema for list of leads"""
    leads: List[LeadResponse]
    total: int
    page: int
    page_size: int
