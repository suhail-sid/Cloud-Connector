"""
Main FastAPI application
GitHub Connector API server
"""
import logging
import sys
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from config import Settings, get_settings
from github_client import GitHubClient, GitHubOAuth
from exceptions import (
    GitHubConnectorError,
    AuthenticationError,
    APIError,
    ValidationError,
    NotFoundError
)
from models import (
    RepositoryResponse,
    IssueResponse,
    CreateIssueRequest,
    CommitResponse,
    UserResponse,
    HealthResponse,
    ErrorResponse,
    PullRequestResponse,
    CreatePullRequestRequest,
    OAuthTokenResponse,
    OAuthAuthorizationRequest
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="GitHub Connector API",
    description="A simple cloud connector to GitHub API",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global GitHub client instance
github_client: Optional[GitHubClient] = None


def get_github_client(settings: Settings = Depends(get_settings)) -> GitHubClient:
    """
    Dependency to get GitHub client
    Initializes client on first request using PAT authentication
    """
    global github_client
    if github_client is None:
        try:
            if not settings.github_token:
                raise ValidationError(
                    "GitHub token is required. Set GITHUB_TOKEN in .env file or use OAuth 2.0"
                )
            github_client = GitHubClient(settings.github_token, settings.github_api_base_url)
        except Exception as e:
            logger.error(f"Failed to initialize GitHub client: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
    return github_client


@app.on_event("startup")
async def startup_event():
    """Application startup event"""
    logger.info("GitHub Connector API starting up...")
    try:
        settings = get_settings()
        
        # Check if authentication is configured
        if not settings.github_token and not (settings.oauth_enabled and settings.oauth_client_id):
            logger.warning(
                "No authentication configured. Configure GITHUB_TOKEN for PAT or "
                "OAUTH_ENABLED with OAUTH_CLIENT_ID for OAuth 2.0"
            )
        else:
            if settings.github_token:
                logger.info("Using Personal Access Token (PAT) authentication")
                get_github_client(settings)
            if settings.oauth_enabled:
                logger.info("OAuth 2.0 authentication is enabled")
        
        logger.info("GitHub Connector API initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize application: {str(e)}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown event"""
    logger.info("GitHub Connector API shutting down...")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information"""
    return {
        "name": "GitHub Connector API",
        "version": "1.0.0",
        "description": "A simple cloud connector to GitHub API",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check(client: GitHubClient = Depends(get_github_client)):
    """
    Health check endpoint
    Verifies API connectivity and authentication
    """
    try:
        user_info = client.get_user_info()
        return HealthResponse(
            status="healthy",
            authenticated=True,
            user=user_info.get("login"),
            message="GitHub connector is working properly"
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            authenticated=False,
            message=str(e)
        )


@app.get("/user", response_model=UserResponse, tags=["User"])
async def get_current_user(client: GitHubClient = Depends(get_github_client)):
    """
    Get authenticated user information
    
    Returns:
        Current authenticated user's information
    """
    try:
        return client.get_user_info()
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except AuthenticationError as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(status_code=401, detail=str(e))
    except APIError as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get(
    "/repos/user/{username}",
    response_model=List[RepositoryResponse],
    tags=["Repositories"]
)
async def get_user_repositories(
    username: str,
    per_page: int = Query(30, ge=1, le=100),
    client: GitHubClient = Depends(get_github_client)
):
    """
    Fetch repositories for a GitHub user
    
    Parameters:
        username: GitHub username
        per_page: Number of repositories to return (1-100)
    
    Returns:
        List of user repositories
    """
    try:
        return client.get_user_repos(username, per_page)
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except NotFoundError as e:
        logger.warning(f"Not found error: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except APIError as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get(
    "/repos/org/{org_name}",
    response_model=List[RepositoryResponse],
    tags=["Repositories"]
)
async def get_org_repositories(
    org_name: str,
    per_page: int = Query(30, ge=1, le=100),
    client: GitHubClient = Depends(get_github_client)
):
    """
    Fetch repositories for a GitHub organization
    
    Parameters:
        org_name: GitHub organization name
        per_page: Number of repositories to return (1-100)
    
    Returns:
        List of organization repositories
    """
    try:
        return client.get_org_repos(org_name, per_page)
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except NotFoundError as e:
        logger.warning(f"Not found error: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except APIError as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get(
    "/issues/{owner}/{repo}",
    response_model=List[IssueResponse],
    tags=["Issues"]
)
async def list_repository_issues(
    owner: str,
    repo: str,
    state: str = Query("open", regex="^(open|closed|all)$"),
    per_page: int = Query(30, ge=1, le=100),
    client: GitHubClient = Depends(get_github_client)
):
    """
    List issues in a repository
    
    Parameters:
        owner: Repository owner username
        repo: Repository name
        state: Issue state - 'open', 'closed', or 'all'
        per_page: Number of issues to return (1-100)
    
    Returns:
        List of repository issues
    """
    try:
        return client.list_issues(owner, repo, state, per_page)
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except NotFoundError as e:
        logger.warning(f"Not found error: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except APIError as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post(
    "/issues/{owner}/{repo}",
    response_model=IssueResponse,
    tags=["Issues"],
    status_code=201
)
async def create_repository_issue(
    owner: str,
    repo: str,
    issue: CreateIssueRequest,
    client: GitHubClient = Depends(get_github_client)
):
    """
    Create an issue in a repository
    
    Parameters:
        owner: Repository owner username
        repo: Repository name
        issue: Issue details (title, body, labels)
    
    Returns:
        Created issue information
    """
    try:
        return client.create_issue(
            owner,
            repo,
            issue.title,
            issue.body,
            issue.labels
        )
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except NotFoundError as e:
        logger.warning(f"Not found error: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except APIError as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get(
    "/commits/{owner}/{repo}",
    response_model=List[CommitResponse],
    tags=["Commits"]
)
async def get_repository_commits(
    owner: str,
    repo: str,
    per_page: int = Query(30, ge=1, le=100),
    client: GitHubClient = Depends(get_github_client)
):
    """
    Fetch commits from a repository
    
    Parameters:
        owner: Repository owner username
        repo: Repository name
        per_page: Number of commits to return (1-100)
    
    Returns:
        List of repository commits
    """
    try:
        return client.get_commits(owner, repo, per_page)
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except NotFoundError as e:
        logger.warning(f"Not found error: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except APIError as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post(
    "/pulls/{owner}/{repo}",
    response_model=PullRequestResponse,
    tags=["Pull Requests"],
    status_code=201
)
async def create_pull_request(
    owner: str,
    repo: str,
    pr: CreatePullRequestRequest,
    client: GitHubClient = Depends(get_github_client)
):
    """
    Create a pull request in a repository
    
    Parameters:
        owner: Repository owner username
        repo: Repository name
        pr: Pull request details (title, head, base, body, draft)
    
    Returns:
        Created pull request information
    """
    try:
        return client.create_pull_request(
            owner,
            repo,
            pr.title,
            pr.head,
            pr.base,
            pr.body,
            pr.draft
        )
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except NotFoundError as e:
        logger.warning(f"Not found error: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except APIError as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/oauth/authorize", tags=["OAuth 2.0"])
async def get_oauth_authorization_url(
    settings: Settings = Depends(get_settings)
):
    """
    Get GitHub OAuth 2.0 authorization URL
    
    Returns:
        Authorization URL to redirect user to GitHub login
    """
    if not settings.oauth_enabled or not settings.oauth_client_id:
        raise HTTPException(
            status_code=400,
            detail="OAuth 2.0 is not enabled. Configure OAUTH_CLIENT_ID and related settings."
        )
    
    try:
        oauth_client = GitHubOAuth(
            settings.oauth_client_id,
            settings.oauth_client_secret,
            settings.oauth_redirect_uri
        )
        auth_url = oauth_client.get_authorization_url(scopes=["repo", "user"])
        return {
            "authorization_url": auth_url,
            "message": "Redirect user to this URL to authorize the application"
        }
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating authorization URL: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate authorization URL")


@app.post("/oauth/callback", response_model=OAuthTokenResponse, tags=["OAuth 2.0"])
async def oauth_callback(
    auth_request: OAuthAuthorizationRequest,
    settings: Settings = Depends(get_settings)
):
    """
    Handle OAuth 2.0 callback and exchange code for access token
    
    Parameters:
        auth_request: Authorization code from GitHub
    
    Returns:
        Access token information
    """
    if not settings.oauth_enabled or not settings.oauth_client_id:
        raise HTTPException(
            status_code=400,
            detail="OAuth 2.0 is not enabled"
        )
    
    try:
        oauth_client = GitHubOAuth(
            settings.oauth_client_id,
            settings.oauth_client_secret,
            settings.oauth_redirect_uri
        )
        token_response = oauth_client.exchange_code_for_token(auth_request.code)
        
        return OAuthTokenResponse(
            access_token=token_response.get("access_token"),
            token_type=token_response.get("token_type", "bearer"),
            scope=token_response.get("scope", "")
        )
    except ValidationError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except APIError as e:
        logger.error(f"API error: {str(e)}")
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.exception_handler(GitHubConnectorError)
async def github_connector_exception_handler(request, exc: GitHubConnectorError):
    """Handle GitHub Connector exceptions"""
    logger.error(f"GitHub Connector error: {str(exc)}")
    
    if isinstance(exc, AuthenticationError):
        return JSONResponse(
            status_code=401,
            content={"error": "Authentication failed", "detail": str(exc)}
        )
    elif isinstance(exc, NotFoundError):
        return JSONResponse(
            status_code=404,
            content={"error": "Not found", "detail": str(exc)}
        )
    elif isinstance(exc, ValidationError):
        return JSONResponse(
            status_code=400,
            content={"error": "Validation error", "detail": str(exc)}
        )
    elif isinstance(exc, APIError):
        return JSONResponse(
            status_code=502,
            content={"error": "API error", "detail": str(exc)}
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "detail": str(exc)}
        )


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
