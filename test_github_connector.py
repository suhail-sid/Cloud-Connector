"""
Unit tests for GitHub Client and API endpoints
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from github_client import GitHubClient
from exceptions import ValidationError, AuthenticationError, NotFoundError, APIError
from models import CreateIssueRequest


class TestGitHubClient:
    """Test cases for GitHubClient"""
    
    @patch('github_client.requests.get')
    def test_client_initialization_success(self, mock_get):
        """Test successful client initialization"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"login": "testuser"}
        mock_get.return_value = mock_response
        
        client = GitHubClient("valid_token")
        assert client.token == "valid_token"
        assert client.base_url == "https://api.github.com"
    
    def test_client_initialization_empty_token(self):
        """Test client initialization with empty token"""
        with pytest.raises(ValidationError):
            GitHubClient("")
    
    def test_client_initialization_none_token(self):
        """Test client initialization with None token"""
        with pytest.raises(ValidationError):
            GitHubClient(None)
    
    @patch('github_client.requests.get')
    def test_client_authentication_failure(self, mock_get):
        """Test client initialization with invalid token"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_get.return_value = mock_response
        
        with pytest.raises(AuthenticationError):
            GitHubClient("invalid_token")
    
    @patch('github_client.requests.get')
    def test_get_user_repos_success(self, mock_get):
        """Test successful user repositories fetch"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": 1, "name": "repo1", "full_name": "user/repo1"},
            {"id": 2, "name": "repo2", "full_name": "user/repo2"}
        ]
        mock_get.return_value = mock_response
        
        client = GitHubClient("valid_token")
        with patch('github_client.requests.get', return_value=mock_response):
            repos = client.get_user_repos("testuser")
            assert len(repos) == 2
            assert repos[0]["name"] == "repo1"
    
    @patch('github_client.requests.get')
    def test_get_user_repos_not_found(self, mock_get):
        """Test user not found error"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        client = GitHubClient("valid_token")
        with patch('github_client.requests.get', return_value=mock_response):
            with pytest.raises(NotFoundError):
                client.get_user_repos("nonexistent")
    
    def test_get_user_repos_invalid_username(self):
        """Test with invalid username"""
        client = GitHubClient("valid_token")
        with patch('github_client.requests.get'):
            with pytest.raises(ValidationError):
                client.get_user_repos("")
    
    def test_create_issue_request_validation(self):
        """Test CreateIssueRequest validation"""
        # Valid request
        issue = CreateIssueRequest(title="Test issue", body="Description")
        assert issue.title == "Test issue"
        
        # Empty title should fail
        with pytest.raises(ValueError):
            CreateIssueRequest(title="", body="Description")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
