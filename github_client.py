"""
GitHub API Client module
Handles authentication and API communication with GitHub
"""
import logging
import requests
from typing import Dict, List, Any, Optional
from exceptions import AuthenticationError, APIError, NotFoundError, ValidationError

logger = logging.getLogger(__name__)


class GitHubClient:
    """
    GitHub API Client for making authenticated requests to GitHub API
    Handles authentication and provides methods for GitHub operations
    """
    
    def __init__(self, token: str, base_url: str = "https://api.github.com"):
        """
        Initialize GitHub client
        
        Args:
            token: GitHub Personal Access Token
            base_url: GitHub API base URL
            
        Raises:
            ValidationError: If token is empty or invalid
        """
        if not token or not isinstance(token, str) or len(token.strip()) == 0:
            raise ValidationError("GitHub token is required and must be a non-empty string")
        
        self.token = token
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Connector"
        }
        self._verify_authentication()
    
    def _verify_authentication(self) -> None:
        """
        Verify that the token is valid by making a test request
        
        Raises:
            AuthenticationError: If token is invalid or authentication fails
        """
        try:
            response = requests.get(
                f"{self.base_url}/user",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 401:
                raise AuthenticationError("Invalid GitHub token. Please check your credentials.")
            response.raise_for_status()
            logger.info("GitHub authentication successful")
        except requests.exceptions.RequestException as e:
            logger.error(f"Authentication failed: {str(e)}")
            raise AuthenticationError(f"Failed to authenticate with GitHub: {str(e)}")
    
    def get_user_repos(self, username: str, per_page: int = 30) -> List[Dict[str, Any]]:
        """
        Fetch repositories for a given user
        
        Args:
            username: GitHub username
            per_page: Number of results per page (max 100)
            
        Returns:
            List of repository dictionaries
            
        Raises:
            ValidationError: If username is invalid
            NotFoundError: If user not found
            APIError: If API request fails
        """
        if not username or not isinstance(username, str) or len(username.strip()) == 0:
            raise ValidationError("Username is required and must be a non-empty string")
        
        if not 1 <= per_page <= 100:
            raise ValidationError("per_page must be between 1 and 100")
        
        try:
            url = f"{self.base_url}/users/{username}/repos"
            response = requests.get(
                url,
                headers=self.headers,
                params={"per_page": per_page, "sort": "updated", "direction": "desc"},
                timeout=10
            )
            
            if response.status_code == 404:
                raise NotFoundError(f"User '{username}' not found on GitHub")
            
            response.raise_for_status()
            logger.info(f"Successfully fetched repositories for user: {username}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching repositories: {str(e)}")
            raise APIError(f"Failed to fetch repositories: {str(e)}")
    
    def get_org_repos(self, org_name: str, per_page: int = 30) -> List[Dict[str, Any]]:
        """
        Fetch repositories for a given organization
        
        Args:
            org_name: GitHub organization name
            per_page: Number of results per page (max 100)
            
        Returns:
            List of repository dictionaries
            
        Raises:
            ValidationError: If org_name is invalid
            NotFoundError: If organization not found
            APIError: If API request fails
        """
        if not org_name or not isinstance(org_name, str) or len(org_name.strip()) == 0:
            raise ValidationError("Organization name is required and must be a non-empty string")
        
        if not 1 <= per_page <= 100:
            raise ValidationError("per_page must be between 1 and 100")
        
        try:
            url = f"{self.base_url}/orgs/{org_name}/repos"
            response = requests.get(
                url,
                headers=self.headers,
                params={"per_page": per_page, "sort": "updated", "direction": "desc"},
                timeout=10
            )
            
            if response.status_code == 404:
                raise NotFoundError(f"Organization '{org_name}' not found on GitHub")
            
            response.raise_for_status()
            logger.info(f"Successfully fetched repositories for organization: {org_name}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching organization repositories: {str(e)}")
            raise APIError(f"Failed to fetch organization repositories: {str(e)}")
    
    def list_issues(
        self,
        owner: str,
        repo: str,
        state: str = "open",
        per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """
        List issues from a repository
        
        Args:
            owner: Repository owner username
            repo: Repository name
            state: Issue state - 'open', 'closed', or 'all'
            per_page: Number of results per page (max 100)
            
        Returns:
            List of issue dictionaries
            
        Raises:
            ValidationError: If parameters are invalid
            NotFoundError: If repository not found
            APIError: If API request fails
        """
        if not owner or not isinstance(owner, str) or len(owner.strip()) == 0:
            raise ValidationError("Owner is required and must be a non-empty string")
        
        if not repo or not isinstance(repo, str) or len(repo.strip()) == 0:
            raise ValidationError("Repository name is required and must be a non-empty string")
        
        if state not in ["open", "closed", "all"]:
            raise ValidationError("State must be 'open', 'closed', or 'all'")
        
        if not 1 <= per_page <= 100:
            raise ValidationError("per_page must be between 1 and 100")
        
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/issues"
            response = requests.get(
                url,
                headers=self.headers,
                params={"state": state, "per_page": per_page},
                timeout=10
            )
            
            if response.status_code == 404:
                raise NotFoundError(f"Repository '{owner}/{repo}' not found")
            
            response.raise_for_status()
            logger.info(f"Successfully listed issues for {owner}/{repo}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error listing issues: {str(e)}")
            raise APIError(f"Failed to list issues: {str(e)}")
    
    def create_issue(
        self,
        owner: str,
        repo: str,
        title: str,
        body: Optional[str] = None,
        labels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create an issue in a repository
        
        Args:
            owner: Repository owner username
            repo: Repository name
            title: Issue title
            body: Issue description
            labels: List of label names
            
        Returns:
            Created issue dictionary
            
        Raises:
            ValidationError: If parameters are invalid
            NotFoundError: If repository not found
            APIError: If API request fails
        """
        if not owner or not isinstance(owner, str) or len(owner.strip()) == 0:
            raise ValidationError("Owner is required and must be a non-empty string")
        
        if not repo or not isinstance(repo, str) or len(repo.strip()) == 0:
            raise ValidationError("Repository name is required and must be a non-empty string")
        
        if not title or not isinstance(title, str) or len(title.strip()) == 0:
            raise ValidationError("Title is required and must be a non-empty string")
        
        if len(title) > 500:
            raise ValidationError("Title must be less than 500 characters")
        
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/issues"
            payload = {
                "title": title,
                "body": body or "",
                "labels": labels or []
            }
            
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 404:
                raise NotFoundError(f"Repository '{owner}/{repo}' not found")
            elif response.status_code == 403:
                raise APIError("You don't have permission to create issues in this repository")
            
            response.raise_for_status()
            logger.info(f"Successfully created issue in {owner}/{repo}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating issue: {str(e)}")
            raise APIError(f"Failed to create issue: {str(e)}")
    
    def get_commits(
        self,
        owner: str,
        repo: str,
        per_page: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Fetch commits from a repository
        
        Args:
            owner: Repository owner username
            repo: Repository name
            per_page: Number of results per page (max 100)
            
        Returns:
            List of commit dictionaries
            
        Raises:
            ValidationError: If parameters are invalid
            NotFoundError: If repository not found
            APIError: If API request fails
        """
        if not owner or not isinstance(owner, str) or len(owner.strip()) == 0:
            raise ValidationError("Owner is required and must be a non-empty string")
        
        if not repo or not isinstance(repo, str) or len(repo.strip()) == 0:
            raise ValidationError("Repository name is required and must be a non-empty string")
        
        if not 1 <= per_page <= 100:
            raise ValidationError("per_page must be between 1 and 100")
        
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/commits"
            response = requests.get(
                url,
                headers=self.headers,
                params={"per_page": per_page},
                timeout=10
            )
            
            if response.status_code == 404:
                raise NotFoundError(f"Repository '{owner}/{repo}' not found")
            
            response.raise_for_status()
            logger.info(f"Successfully fetched commits for {owner}/{repo}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching commits: {str(e)}")
            raise APIError(f"Failed to fetch commits: {str(e)}")
    
    def get_user_info(self) -> Dict[str, Any]:
        """
        Get authenticated user information
        
        Returns:
            User information dictionary
            
        Raises:
            APIError: If API request fails
        """
        try:
            response = requests.get(
                f"{self.base_url}/user",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            logger.info("Successfully fetched user information")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching user info: {str(e)}")
            raise APIError(f"Failed to fetch user information: {str(e)}")
    
    def create_pull_request(
        self,
        owner: str,
        repo: str,
        title: str,
        head: str,
        base: str,
        body: Optional[str] = None,
        draft: bool = False
    ) -> Dict[str, Any]:
        """
        Create a pull request in a repository
        
        Args:
            owner: Repository owner username
            repo: Repository name
            title: Pull request title
            head: The name of the branch where your changes are implemented
            base: The name of the branch you want the changes pulled into
            body: Pull request description
            draft: Create as a draft pull request
            
        Returns:
            Created pull request dictionary
            
        Raises:
            ValidationError: If parameters are invalid
            NotFoundError: If repository not found
            APIError: If API request fails
        """
        if not owner or not isinstance(owner, str) or len(owner.strip()) == 0:
            raise ValidationError("Owner is required and must be a non-empty string")
        
        if not repo or not isinstance(repo, str) or len(repo.strip()) == 0:
            raise ValidationError("Repository name is required and must be a non-empty string")
        
        if not title or not isinstance(title, str) or len(title.strip()) == 0:
            raise ValidationError("Title is required and must be a non-empty string")
        
        if len(title) > 500:
            raise ValidationError("Title must be less than 500 characters")
        
        if not head or not isinstance(head, str) or len(head.strip()) == 0:
            raise ValidationError("Head branch is required")
        
        if not base or not isinstance(base, str) or len(base.strip()) == 0:
            raise ValidationError("Base branch is required")
        
        try:
            url = f"{self.base_url}/repos/{owner}/{repo}/pulls"
            payload = {
                "title": title,
                "head": head,
                "base": base,
                "body": body or "",
                "draft": draft
            }
            
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 404:
                raise NotFoundError(f"Repository '{owner}/{repo}' not found")
            elif response.status_code == 403:
                raise APIError("You don't have permission to create pull requests in this repository")
            elif response.status_code == 422:
                error_msg = response.json().get("message", "Unprocessable entity")
                raise APIError(f"Failed to create pull request: {error_msg}")
            
            response.raise_for_status()
            logger.info(f"Successfully created pull request in {owner}/{repo}")
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating pull request: {str(e)}")
            raise APIError(f"Failed to create pull request: {str(e)}")


class GitHubOAuth:
    """
    GitHub OAuth 2.0 client for handling OAuth authentication flow
    """
    
    GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
    GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        """
        Initialize OAuth client
        
        Args:
            client_id: GitHub OAuth app client ID
            client_secret: GitHub OAuth app client secret
            redirect_uri: OAuth redirect URI
            
        Raises:
            ValidationError: If credentials are missing
        """
        if not client_id or not isinstance(client_id, str) or len(client_id.strip()) == 0:
            raise ValidationError("Client ID is required")
        if not client_secret or not isinstance(client_secret, str) or len(client_secret.strip()) == 0:
            raise ValidationError("Client secret is required")
        if not redirect_uri or not isinstance(redirect_uri, str) or len(redirect_uri.strip()) == 0:
            raise ValidationError("Redirect URI is required")
        
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
    
    def get_authorization_url(self, state: Optional[str] = None, scopes: Optional[List[str]] = None) -> str:
        """
        Generate GitHub OAuth authorization URL
        
        Args:
            state: OAuth state parameter for security
            scopes: List of OAuth scopes to request
            
        Returns:
            Authorization URL
        """
        scopes = scopes or ["repo", "user"]
        params = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": ",".join(scopes),
            "allow_signup": "true"
        }
        if state:
            params["state"] = state
        
        query_string = "&".join([f"{k}={v}" for k, v in params.items()])
        return f"{self.GITHUB_AUTH_URL}?{query_string}"
    
    def exchange_code_for_token(self, code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token
        
        Args:
            code: Authorization code from GitHub
            
        Returns:
            Token response containing access_token
            
        Raises:
            ValidationError: If code is invalid
            APIError: If token exchange fails
        """
        if not code or not isinstance(code, str) or len(code.strip()) == 0:
            raise ValidationError("Authorization code is required")
        
        try:
            response = requests.post(
                self.GITHUB_TOKEN_URL,
                headers={"Accept": "application/json"},
                data={
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "redirect_uri": self.redirect_uri
                },
                timeout=10
            )
            
            response.raise_for_status()
            data = response.json()
            
            if "error" in data:
                raise APIError(f"OAuth error: {data.get('error_description', data.get('error'))}")
            
            logger.info("Successfully exchanged authorization code for access token")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error exchanging code for token: {str(e)}")
            raise APIError(f"Failed to exchange authorization code: {str(e)}")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error creating pull request: {str(e)}")
            raise APIError(f"Failed to create pull request: {str(e)}")
