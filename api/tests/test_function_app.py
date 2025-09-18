#!/usr/bin/env python3
# /// script
# dependencies = [
#     "pytest>=7.0.0",
#     "pytest-mock",
#     "pytest-asyncio", 
#     "azure-functions",
#     "bcrypt",
# ]
# ///

import pytest
import json
import azure.functions as func
from unittest.mock import patch, MagicMock, Mock
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from function_app import postUser, postVote, getVote

class MockDocument:
    def __init__(self, data):
        self._data = data.copy() 
    
    def get(self, key, default=None):
        return self._data.get(key, default)
    
    def __getitem__(self, key):
        return self._data[key]
    
    def __setitem__(self, key, value):
        """Support item assignment like vote['pseudo'] = username"""
        self._data[key] = value
    
    def __iter__(self):
        return iter(self._data)
    
    def keys(self):
        return self._data.keys()
    
    def values(self):
        return self._data.values()
    
    def items(self):
        return self._data.items()

class TestAzureFunction:
    
    def test_post_user_success(self):
        """Test successful user creation"""
        test_data = {
            "username": "testuser",
            "email": "test@example.com", 
            "password": "testpassword"
        }
        req = func.HttpRequest(
            method='POST',
            body=json.dumps(test_data).encode('utf-8'),
            url='http://localhost:7071/api/postUser',
            headers={'Content-Type': 'application/json'}
        )
        
        mock_output = Mock()
  
        response = postUser(req, mock_output)
        
        assert response.status_code == 201
        response_data = json.loads(response.get_body().decode())
        assert "User testuser registered successfully." in response_data["message"]
        assert "userId" in response_data
        assert response_data["username"] == "testuser"
        mock_output.set.assert_called_once()
    
    def test_post_user_missing_fields(self):
        """Test user creation with missing required fields"""
        test_data = {"username": "testuser"} 
        req = func.HttpRequest(
            method='POST',
            body=json.dumps(test_data).encode('utf-8'),
            url='http://localhost:7071/api/postUser',
            headers={'Content-Type': 'application/json'}
        )
        
        mock_output = Mock()

        response = postUser(req, mock_output)
        
        assert response.status_code == 400
        assert "Missing username, email, or password" in response.get_body().decode()
    
    def test_post_user_invalid_json(self):
        """Test user creation with invalid JSON"""
        req = func.HttpRequest(
            method='POST',
            body=b'invalid json',
            url='http://localhost:7071/api/postUser',
            headers={'Content-Type': 'application/json'}
        )
        
        mock_output = Mock()
        
        response = postUser(req, mock_output)
        
        assert response.status_code == 400
        assert "Invalid request body" in response.get_body().decode()

    def test_post_vote_success(self):
        """Test successful vote creation"""
        test_data = {
            "userId": "user123",
            "vote": "Oui"
        }
        req = func.HttpRequest(
            method='POST',
            body=json.dumps(test_data).encode('utf-8'),
            url='http://localhost:7071/api/postVote',
            headers={'Content-Type': 'application/json'}
        )
        
        mock_input = []
        mock_output = Mock()
        
        response = postVote(req, mock_input, mock_output)
        
        assert response.status_code == 200
        assert "Vote recorded successfully" in response.get_body().decode()
        mock_output.set.assert_called_once()
    
    def test_post_vote_duplicate(self):
        """Test voting when user has already voted"""
        test_data = {
            "userId": "user123",
            "vote": "Oui"
        }
        req = func.HttpRequest(
            method='POST',
            body=json.dumps(test_data).encode('utf-8'),
            url='http://localhost:7071/api/postVote',
            headers={'Content-Type': 'application/json'}
        )
        
        existing_vote = MockDocument({"userId": "user123", "vote": "Non"})
        mock_input = [existing_vote]
        mock_output = Mock()
        
        response = postVote(req, mock_input, mock_output)
        
        assert response.status_code == 400
        assert "User user123 has already voted" in response.get_body().decode()
        mock_output.set.assert_not_called()
    
    def test_post_vote_missing_fields(self):
        """Test vote creation with missing required fields"""
 
        test_data = {"userId": "user123"}
        req = func.HttpRequest(
            method='POST',
            body=json.dumps(test_data).encode('utf-8'),
            url='http://localhost:7071/api/postVote',
            headers={'Content-Type': 'application/json'}
        )
        
        mock_input = []
        mock_output = Mock()
        
        response = postVote(req, mock_input, mock_output)

        assert response.status_code == 400
        assert "Missing userId or vote" in response.get_body().decode()

    def test_get_vote_success(self):
        """Test successful vote retrieval with percentage calculation"""
        req = func.HttpRequest(
            method='GET',
            body=b'',
            url='http://localhost:7071/api/getVote'
        )
        
        vote1 = MockDocument({"id": "vote1", "userId": "user1", "vote": "Oui"})
        vote2 = MockDocument({"id": "vote2", "userId": "user2", "vote": "Non"})
        vote3 = MockDocument({"id": "vote3", "userId": "user3", "vote": "Oui"})
        mock_votes = [vote1, vote2, vote3]

        user1 = MockDocument({"id": "user1", "username": "alice"})
        user2 = MockDocument({"id": "user2", "username": "bob"})
        user3 = MockDocument({"id": "user3", "username": "charlie"})
        mock_users = [user1, user2, user3]

        response = getVote(req, mock_votes, mock_users)

        assert response.status_code == 200
        response_data = json.loads(response.get_body().decode())
        assert response_data["totalVotes"] == 3
        assert response_data["percentageYes"] == pytest.approx(66.67, rel=1e-2)
        assert response_data["percentageNo"] == pytest.approx(33.33, rel=1e-2)
        assert len(response_data["votes"]) == 3
        
        votes_with_pseudo = response_data["votes"]
        usernames = [vote["pseudo"] for vote in votes_with_pseudo]
        assert "alice" in usernames
        assert "bob" in usernames
        assert "charlie" in usernames
    
    def test_get_vote_no_votes(self):
        """Test vote retrieval when no votes exist"""
        req = func.HttpRequest(
            method='GET',
            body=b'',
            url='http://localhost:7071/api/getVote'
        )
        
        mock_votes = []
        mock_users = []

        response = getVote(req, mock_votes, mock_users)
        
        assert response.status_code == 404
        assert "No votes found" in response.get_body().decode()
    
    def test_get_vote_all_yes(self):
        """Test vote retrieval with all 'Oui' votes"""
        req = func.HttpRequest(
            method='GET',
            body=b'',
            url='http://localhost:7071/api/getVote'
        )
        
        vote1 = MockDocument({"id": "vote1", "userId": "user1", "vote": "Oui"})
        vote2 = MockDocument({"id": "vote2", "userId": "user2", "vote": "Oui"})
        mock_votes = [vote1, vote2]
        
        user1 = MockDocument({"id": "user1", "username": "alice"})
        user2 = MockDocument({"id": "user2", "username": "bob"})
        mock_users = [user1, user2]
        
        response = getVote(req, mock_votes, mock_users)

        assert response.status_code == 200
        response_data = json.loads(response.get_body().decode())
        assert response_data["percentageYes"] == 100.0
        assert response_data["percentageNo"] == 0.0
    
    def test_get_vote_all_no(self):
        """Test vote retrieval with all 'Non' votes"""
        req = func.HttpRequest(
            method='GET',
            body=b'',
            url='http://localhost:7071/api/getVote'
        )

        vote1 = MockDocument({"id": "vote1", "userId": "user1", "vote": "Non"})
        vote2 = MockDocument({"id": "vote2", "userId": "user2", "vote": "Non"})
        mock_votes = [vote1, vote2]
        
        user1 = MockDocument({"id": "user1", "username": "alice"})
        user2 = MockDocument({"id": "user2", "username": "bob"})
        mock_users = [user1, user2]
        
        response = getVote(req, mock_votes, mock_users)
        
        assert response.status_code == 200
        response_data = json.loads(response.get_body().decode())
        assert response_data["percentageYes"] == 0.0
        assert response_data["percentageNo"] == 100.0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])