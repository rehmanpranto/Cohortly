"""
Assignment API routes
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.assignment import Assignment
from app.models.bootcamp import Bootcamp
from app.schemas.assignment import (
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentResponse,
    AssignmentListResponse,
)
from app.middleware.auth import get_current_user, require_instructor


router = APIRouter(prefix="/assignments", tags=["Assignments"])


@router.get("", response_model=AssignmentListResponse)
async def list_assignments(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    bootcamp_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List assignments with optional bootcamp filter
    """
    query = db.query(Assignment)
    
    # Filter by bootcamp if provided
    if bootcamp_id:
        query = query.filter(Assignment.bootcamp_id == bootcamp_id)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    assignments = query.offset(offset).limit(page_size).all()
    
    return AssignmentListResponse(
        assignments=[AssignmentResponse.model_validate(a) for a in assignments],
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
async def create_assignment(
    assignment_data: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_instructor)
):
    """
    Create a new assignment (Instructor/Admin only)
    """
    # Check if bootcamp exists
    bootcamp = db.query(Bootcamp).filter(Bootcamp.id == assignment_data.bootcamp_id).first()
    if not bootcamp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bootcamp not found"
        )
    
    # Check if user is the instructor or admin
    if str(bootcamp.instructor_id) != str(current_user.id) and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to create assignments for this bootcamp"
        )
    
    # Create assignment
    new_assignment = Assignment(
        bootcamp_id=assignment_data.bootcamp_id,
        instructor_id=str(current_user.id),
        title=assignment_data.title,
        description=assignment_data.description,
        due_date=assignment_data.due_date,
        points=assignment_data.points,
    )
    
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    
    return AssignmentResponse.model_validate(new_assignment)


@router.get("/{assignment_id}", response_model=AssignmentResponse)
async def get_assignment(
    assignment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get assignment details by ID
    """
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    return AssignmentResponse.model_validate(assignment)


@router.put("/{assignment_id}", response_model=AssignmentResponse)
async def update_assignment(
    assignment_id: str,
    assignment_data: AssignmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_instructor)
):
    """
    Update assignment (Instructor/Admin only, must be assignment owner)
    """
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Check if user is the instructor or admin
    if str(assignment.instructor_id) != str(current_user.id) and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this assignment"
        )
    
    # Update fields if provided
    update_data = assignment_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(assignment, field, value)
    
    db.commit()
    db.refresh(assignment)
    
    return AssignmentResponse.model_validate(assignment)


@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_assignment(
    assignment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_instructor)
):
    """
    Delete assignment (Instructor/Admin only, must be assignment owner)
    """
    assignment = db.query(Assignment).filter(Assignment.id == assignment_id).first()
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assignment not found"
        )
    
    # Check if user is the instructor or admin
    if str(assignment.instructor_id) != str(current_user.id) and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this assignment"
        )
    
    db.delete(assignment)
    db.commit()
    
    return None
