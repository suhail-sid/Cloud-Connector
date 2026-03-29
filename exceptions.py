"""
Exceptions module for GitHub Connector
Custom exceptions for error handling
"""


class GitHubConnectorError(Exception):
    """Base exception for GitHub Connector"""
    pass


class AuthenticationError(GitHubConnectorError):
    """Raised when authentication fails"""
    pass


class APIError(GitHubConnectorError):
    """Raised when GitHub API returns an error"""
    pass


class ValidationError(GitHubConnectorError):
    """Raised when input validation fails"""
    pass


class NotFoundError(GitHubConnectorError):
    """Raised when resource is not found"""
    pass
