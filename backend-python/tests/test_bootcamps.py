"""
Tests for bootcamp endpoints
"""

import pytest
from fastapi import status
from datetime import datetime, timedelta


@pytest.fixture
def test_bootcamp_data():
    """Sample bootcamp data"""
    return {
        "name": "Full Stack Web Development",
        "description": "Learn full stack web development with modern technologies",
        "start_date": (datetime.now() + timedelta(days=30)).isoformat(),
        "end_date": (datetime.now() + timedelta(days=120)).isoformat(),
        "duration_weeks": 12,
        "max_students": 30,
        "status": "DRAFT"
    }


def test_create_bootcamp_success(client, instructor_headers, test_bootcamp_data):
    """Test creating a bootcamp as instructor"""
    response = client.post(
        "/api/v1/bootcamps",
        headers=instructor_headers,
        json=test_bootcamp_data
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == test_bootcamp_data["name"]
    assert data["status"] == test_bootcamp_data["status"]


def test_create_bootcamp_student_forbidden(client, auth_headers, test_bootcamp_data):
    """Test creating a bootcamp as student (should fail)"""
    response = client.post(
        "/api/v1/bootcamps",
        headers=auth_headers,
        json=test_bootcamp_data
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_list_bootcamps(client, auth_headers):
    """Test listing bootcamps"""
    response = client.get(
        "/api/v1/bootcamps",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "bootcamps" in data
    assert "total" in data
    assert "page" in data


def test_get_bootcamp_success(client, instructor_headers, auth_headers, test_bootcamp_data):
    """Test getting a specific bootcamp"""
    # Create bootcamp
    create_response = client.post(
        "/api/v1/bootcamps",
        headers=instructor_headers,
        json=test_bootcamp_data
    )
    bootcamp_id = create_response.json()["id"]
    
    # Get bootcamp
    response = client.get(
        f"/api/v1/bootcamps/{bootcamp_id}",
        headers=auth_headers
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == bootcamp_id
    assert data["name"] == test_bootcamp_data["name"]


def test_update_bootcamp_success(client, instructor_headers, test_bootcamp_data):
    """Test updating a bootcamp as owner"""
    # Create bootcamp
    create_response = client.post(
        "/api/v1/bootcamps",
        headers=instructor_headers,
        json=test_bootcamp_data
    )
    bootcamp_id = create_response.json()["id"]
    
    # Update bootcamp
    response = client.put(
        f"/api/v1/bootcamps/{bootcamp_id}",
        headers=instructor_headers,
        json={"name": "Updated Bootcamp Name", "status": "PUBLISHED"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Updated Bootcamp Name"
    assert data["status"] == "PUBLISHED"


def test_delete_bootcamp_success(client, instructor_headers, test_bootcamp_data):
    """Test deleting a bootcamp as owner"""
    # Create bootcamp
    create_response = client.post(
        "/api/v1/bootcamps",
        headers=instructor_headers,
        json=test_bootcamp_data
    )
    bootcamp_id = create_response.json()["id"]
    
    # Delete bootcamp
    response = client.delete(
        f"/api/v1/bootcamps/{bootcamp_id}",
        headers=instructor_headers
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT
