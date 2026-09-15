"""
Test suite for the Mergington High School API endpoints.
Tests cover happy paths for all three endpoints: GET /activities, POST /signup, DELETE /unregister.
"""

import pytest


def test_get_activities_returns_all_activities(client, fresh_activities):
    """
    Test that GET /activities returns all activities with correct structure.
    """
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify all test activities are returned
    assert len(data) == 3
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    
    # Verify activity structure
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_get_activities_has_correct_count(client, fresh_activities):
    """
    Test that GET /activities returns correct participant counts.
    """
    response = client.get("/activities")
    data = response.json()
    
    # Verify participant counts
    assert len(data["Chess Club"]["participants"]) == 1
    assert len(data["Programming Class"]["participants"]) == 0
    assert len(data["Gym Class"]["participants"]) == 2


def test_signup_adds_participant(client, fresh_activities):
    """
    Test that POST /signup successfully adds a new participant to an activity.
    """
    activity_name = "Programming Class"
    email = "alice@mergington.edu"
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == 1


def test_signup_returns_success_message(client, fresh_activities):
    """
    Test that POST /signup returns a success message.
    """
    activity_name = "Chess Club"
    email = "bob@mergington.edu"
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_unregister_removes_participant(client, fresh_activities):
    """
    Test that DELETE /unregister successfully removes a participant from an activity.
    """
    activity_name = "Gym Class"
    email = "john@mergington.edu"
    
    # Verify participant exists before deletion
    activities_before = client.get("/activities").json()
    assert email in activities_before[activity_name]["participants"]
    
    # Delete the participant
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    
    # Verify participant was removed
    activities_after = client.get("/activities").json()
    assert email not in activities_after[activity_name]["participants"]
    assert len(activities_after[activity_name]["participants"]) == 1


def test_unregister_returns_success_message(client, fresh_activities):
    """
    Test that DELETE /unregister returns a success message.
    """
    activity_name = "Gym Class"
    email = "olivia@mergington.edu"
    
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": email}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]
