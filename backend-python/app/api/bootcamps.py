"""
Bootcamp API routes
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.bootcamp import Bootcamp
from app.schemas.bootcamp import (
    BootcampCreate,
    BootcampUpdate,
    BootcampResponse,
    BootcampListResponse,
)
from app.middleware.auth import get_current_user, require_instructor


router = APIRouter(prefix="/bootcamps", tags=["Bootcamps"])


@router.get("", response_model=BootcampListResponse)
async def list_bootcamps(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all bootcamps with pagination
    """
    query = db.query(Bootcamp)
    
    # Filter by status if provided
    if status:
        query = query.filter(Bootcamp.status == status)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    bootcamps = query.offset(offset).limit(page_size).all()
    
    return BootcampListResponse(
        bootcamps=[BootcampResponse.model_validate(b) for b in bootcamps],
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("", response_model=BootcampResponse, status_code=status.HTTP_201_CREATED)
async def create_bootcamp(
    bootcamp_data: BootcampCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_instructor)
):
    """
    Create a new bootcamp (Instructor/Admin only)
    """
    # Create bootcamp
    new_bootcamp = Bootcamp(
        name=bootcamp_data.name,
        description=bootcamp_data.description,
        instructor_id=str(current_user.id),
        start_date=bootcamp_data.start_date,
        end_date=bootcamp_data.end_date,
        duration_weeks=bootcamp_data.duration_weeks,
        max_students=bootcamp_data.max_students,
        status=bootcamp_data.status,
    )
    
    db.add(new_bootcamp)
    db.commit()
    db.refresh(new_bootcamp)
    
    return BootcampResponse.model_validate(new_bootcamp)


@router.get("/{bootcamp_id}", response_model=BootcampResponse)
async def get_bootcamp(
    bootcamp_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get bootcamp details by ID
    """
    bootcamp = db.query(Bootcamp).filter(Bootcamp.id == bootcamp_id).first()
    if not bootcamp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bootcamp not found"
        )
    
    return BootcampResponse.model_validate(bootcamp)


@router.put("/{bootcamp_id}", response_model=BootcampResponse)
async def update_bootcamp(
    bootcamp_id: str,
    bootcamp_data: BootcampUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_instructor)
):
    """
    Update bootcamp (Instructor/Admin only, must be bootcamp owner)
    """
    bootcamp = db.query(Bootcamp).filter(Bootcamp.id == bootcamp_id).first()
    if not bootcamp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bootcamp not found"
        )
    
    # Check if user is the instructor or admin
    if str(bootcamp.instructor_id) != str(current_user.id) and current_user.role.value != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this bootcamp"
        )
    
    # Update fields if provided
    update_data = bootcamp_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bootcamp, field, value)
    
    db.commit()
    db.refresh(bootcamp)
    
    return BootcampResponse.model_validate(bootcamp)


@router.delete("/{bootcamp_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bootcamp(
    bootcamp_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_instructor)
):
    """
    Delete bootcamp (Instructor/Admin only, must be bootcamp owner)
    """
    bootcamp = db.query(Bootcamp).filter(Bootcamp.id == bootcamp_id).first()
    if not bootcamp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bootcamp not found"
        )
    
    # Check if user is the instructor or admin
    if str(bootcamp.instructor_id) != str(current_user.id) and current_user.role.value != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this bootcamp"
        )
    
    db.delete(bootcamp)
    db.commit()
    
    return None
