"""
Pydantic models for request/response validation
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class RepositoryResponse(BaseModel):
    """Repository response model"""
    id: int
    name: str
    full_name: str
    description: Optional[str] = None
    url: str
    stars: int = Field(alias="stargazers_count")
    forks: int = Field(alias="forks_count")
    language: Optional[str] = None
    
    class Config:
        populate_by_name = True


class IssueResponse(BaseModel):
    """Issue response model"""
    id: int
    number: int
    title: str
    body: Optional[str] = None
    state: str
    created_at: str
    updated_at: str
    url: str
    user: Optional[dict] = None
    
    class Config:
        populate_by_name = True


class CreateIssueRequest(BaseModel):
    """Create issue request model"""
    title: str = Field(..., min_length=1, max_length=500, description="Issue title")
    body: Optional[str] = Field(None, description="Issue description")
    labels: Optional[List[str]] = Field(None, description="List of label names")


class CommitResponse(BaseModel):
    """Commit response model"""
    sha: str
    message: str = Field(alias="commit")
    author: Optional[dict] = None
    url: str
    
    class Config:
        populate_by_name = True


class UserResponse(BaseModel):
    """User response model"""
    id: int
    login: str
    name: Optional[str] = None
    bio: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    public_repos: int
    followers: int
    following: int
    created_at: str


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    authenticated: bool
    user: Optional[str] = None
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    status_code: int
