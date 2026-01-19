"""
Enrollment API routes
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.models.enrollment import Enrollment
from app.models.bootcamp import Bootcamp
from app.schemas.enrollment import (
    EnrollmentCreate,
    EnrollmentUpdate,
    EnrollmentResponse,
    EnrollmentListResponse,
)
from app.middleware.auth import get_current_user


router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.get("", response_model=EnrollmentListResponse)
async def list_enrollments(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    bootcamp_id: Optional[str] = None,
    student_id: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List enrollments with filters
    Students can only see their own enrollments
    """
    query = db.query(Enrollment)
    
    # Students can only see their own enrollments
    if current_user.role == UserRole.STUDENT:
        query = query.filter(Enrollment.student_id == str(current_user.id))
    elif student_id:
        query = query.filter(Enrollment.student_id == student_id)
    
    # Filter by bootcamp if provided
    if bootcamp_id:
        query = query.filter(Enrollment.bootcamp_id == bootcamp_id)
    
    # Filter by status if provided
    if status:
        query = query.filter(Enrollment.status == status)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    enrollments = query.offset(offset).limit(page_size).all()
    
    return EnrollmentListResponse(
        enrollments=[EnrollmentResponse.model_validate(e) for e in enrollments],
        total=total,
        page=page,
        page_size=page_size
    )


@router.post("", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def create_enrollment(
    enrollment_data: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new enrollment
    Students can only enroll themselves
    Sales/Admin can enroll any student
    """
    # Check if student exists
    student = db.query(User).filter(User.id == enrollment_data.student_id).first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    
    # Check if bootcamp exists
    bootcamp = db.query(Bootcamp).filter(Bootcamp.id == enrollment_data.bootcamp_id).first()
    if not bootcamp:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bootcamp not found"
        )
    
    # Students can only enroll themselves
    if current_user.role == UserRole.STUDENT:
        if str(current_user.id) != enrollment_data.student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Students can only enroll themselves"
            )
    
    # Check if enrollment already exists
    existing = db.query(Enrollment).filter(
        Enrollment.student_id == enrollment_data.student_id,
        Enrollment.bootcamp_id == enrollment_data.bootcamp_id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student already enrolled in this bootcamp"
        )
    
    # Create enrollment
    new_enrollment = Enrollment(
        student_id=enrollment_data.student_id,
        bootcamp_id=enrollment_data.bootcamp_id,
        status=enrollment_data.status,
    )
    
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    
    return EnrollmentResponse.model_validate(new_enrollment)


@router.get("/{enrollment_id}", response_model=EnrollmentResponse)
async def get_enrollment(
    enrollment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get enrollment details by ID
    """
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    # Students can only see their own enrollments
    if current_user.role == UserRole.STUDENT:
        if str(enrollment.student_id) != str(current_user.id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this enrollment"
            )
    
    return EnrollmentResponse.model_validate(enrollment)


@router.put("/{enrollment_id}", response_model=EnrollmentResponse)
async def update_enrollment(
    enrollment_id: str,
    enrollment_data: EnrollmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update enrollment status (Admin/Sales/Instructor only)
    """
    # Only admin, sales, and instructors can update enrollments
    if current_user.role == UserRole.STUDENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Students cannot update enrollments"
        )
    
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    # Update fields if provided
    update_data = enrollment_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(enrollment, field, value)
    
    db.commit()
    db.refresh(enrollment)
    
    return EnrollmentResponse.model_validate(enrollment)


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_enrollment(
    enrollment_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete enrollment (Admin only)
    """
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can delete enrollments"
        )
    
    enrollment = db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    db.delete(enrollment)
    db.commit()
    
    return None
