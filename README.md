# GitHub Connector API

A simple, production-ready cloud connector to GitHub API built with FastAPI and Python.

## Features

✅ **Authentication**: GitHub Personal Access Token (PAT) with secure credential management  
✅ **Multiple API Endpoints**: Repositories, Issues, Commits, and User information  
✅ **Error Handling**: Comprehensive error handling with meaningful error messages  
✅ **Input Validation**: Pydantic models for request/response validation  
✅ **Logging**: Structured logging for debugging and monitoring  
✅ **API Documentation**: Auto-generated Swagger UI documentation  
✅ **CORS Support**: Cross-Origin Resource Sharing enabled  
✅ **Health Checks**: Built-in health check endpoint  

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- GitHub Personal Access Token (PAT)

## Installation

### 1. Clone or Download the Project

```bash
cd github-connector
```

### 2. Create a Virtual Environment (Recommended)

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your GitHub Personal Access Token:

```
GITHUB_TOKEN=ghp_your_personal_access_token_here
GITHUB_API_BASE_URL=https://api.github.com
DEBUG=True
LOG_LEVEL=INFO
```

### Getting Your GitHub Personal Access Token

1. Go to [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token"
3. Select scopes:
   - `repo` - Full control of private repositories
   - `public_repo` - Access to public repositories
   - `read:user` - Read user profile data
4. Copy the token and paste it in your `.env` file

## Running the Application

### Development Mode

```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Production Mode (with Uvicorn)

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## Available Endpoints

### Health & User

#### Health Check
```
GET /health
```
Verifies API connectivity and authentication status.

**Response (200):**
```json
{
  "status": "healthy",
  "authenticated": true,
  "user": "octocat",
  "message": "GitHub connector is working properly"
}
```

#### Get Current User
```
GET /user
```
Returns authenticated user information.

**Response (200):**
```json
{
  "id": 1,
  "login": "octocat",
  "name": "The Octocat",
  "bio": "There once was...",
  "company": "@github",
  "location": "San Francisco",
  "public_repos": 2,
  "followers": 20,
  "following": 0,
  "created_at": "2011-01-25T18:44:36Z"
}
```

### Repositories

#### Get User Repositories
```
GET /repos/user/{username}?per_page=30
```
Fetch repositories for a GitHub user.

**Parameters:**
- `username` (required): GitHub username
- `per_page` (optional, default: 30): Number of results (1-100)

**Response (200):**
```json
[
  {
    "id": 1296269,
    "name": "Hello-World",
    "full_name": "octocat/Hello-World",
    "description": "This your first repo!",
    "url": "https://api.github.com/repos/octocat/Hello-World",
    "stars": 9,
    "forks": 9,
    "language": "Python"
  }
]
```

#### Get Organization Repositories
```
GET /repos/org/{org_name}?per_page=30
```
Fetch repositories for a GitHub organization.

**Parameters:**
- `org_name` (required): GitHub organization name
- `per_page` (optional, default: 30): Number of results (1-100)

### Issues

#### List Repository Issues
```
GET /issues/{owner}/{repo}?state=open&per_page=30
```
List issues in a repository.

**Parameters:**
- `owner` (required): Repository owner username
- `repo` (required): Repository name
- `state` (optional, default: "open"): Issue state - "open", "closed", or "all"
- `per_page` (optional, default: 30): Number of results (1-100)

**Response (200):**
```json
[
  {
    "id": 1,
    "number": 1347,
    "title": "Found a bug",
    "body": "I'm having a problem with this.",
    "state": "open",
    "created_at": "2011-04-22T13:33:48Z",
    "updated_at": "2011-04-23T13:33:48Z",
    "url": "https://api.github.com/repos/octocat/Hello-World/issues/1347"
  }
]
```

#### Create Repository Issue
```
POST /issues/{owner}/{repo}
Content-Type: application/json

{
  "title": "Found a bug",
  "body": "I'm having a problem with this.",
  "labels": ["bug", "help-wanted"]
}
```
Create a new issue in a repository.

**Parameters:**
- `owner` (required): Repository owner username
- `repo` (required): Repository name

**Request Body:**
```json
{
  "title": "Issue title (required)",
  "body": "Issue description (optional)",
  "labels": ["label1", "label2"] (optional)
}
```

**Response (201):**
```json
{
  "id": 1,
  "number": 1347,
  "title": "Found a bug",
  "body": "I'm having a problem with this.",
  "state": "open",
  "created_at": "2011-04-22T13:33:48Z",
  "updated_at": "2011-04-23T13:33:48Z",
  "url": "https://api.github.com/repos/octocat/Hello-World/issues/1347"
}
```

### Commits

#### Get Repository Commits
```
GET /commits/{owner}/{repo}?per_page=30
```
Fetch commits from a repository.

**Parameters:**
- `owner` (required): Repository owner username
- `repo` (required): Repository name
- `per_page` (optional, default: 30): Number of results (1-100)

**Response (200):**
```json
[
  {
    "sha": "6dcb09b5b57875f334f61aebed695e2e4193db5e",
    "message": "Fix all the bugs",
    "author": {
      "name": "Monalisa Octocat",
      "email": "support@github.com"
    },
    "url": "https://api.github.com/repos/octocat/Hello-World/commits/6dcb09b5b57875f334f61aebed695e2e4193db5e"
  }
]
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- **400 Bad Request**: Invalid input parameters
- **401 Unauthorized**: Authentication failed or invalid token
- **404 Not Found**: Resource (user, repo, etc.) not found
- **502 Bad Gateway**: GitHub API error
- **500 Internal Server Error**: Unexpected server error

**Error Response Format:**
```json
{
  "detail": "Detailed error message"
}
```

## Project Structure

```
.
├── main.py                      # FastAPI application
├── github_client.py             # GitHub API client
├── config.py                    # Configuration management
├── models.py                    # Pydantic models
├── exceptions.py                # Custom exceptions
├── test_github_connector.py     # Unit tests
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
└── README.md                    # This file
```

## Example Usage

### Using cURL

```bash
# Get current user
curl -X GET http://localhost:8000/user

# Get user repositories
curl -X GET "http://localhost:8000/repos/user/octocat?per_page=10"

# List open issues
curl -X GET "http://localhost:8000/issues/octocat/Hello-World?state=open"

# Create an issue
curl -X POST http://localhost:8000/issues/octocat/Hello-World \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Found a bug",
    "body": "I found a bug in the code",
    "labels": ["bug"]
  }'

# Get commits
curl -X GET "http://localhost:8000/commits/octocat/Hello-World?per_page=10"
```

### Using Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Get user repositories
response = requests.get(f"{BASE_URL}/repos/user/octocat")
repos = response.json()
print(repos)

# Create an issue
issue_data = {
    "title": "Found a bug",
    "body": "Description of the bug",
    "labels": ["bug"]
}
response = requests.post(
    f"{BASE_URL}/issues/octocat/Hello-World",
    json=issue_data
)
print(response.json())
```

## Testing

Run the test suite:

```bash
pytest test_github_connector.py -v
```

## Security Considerations

1. **Token Management**: Never commit `.env` file or tokens to version control
2. **HTTPS**: Use HTTPS in production
3. **Rate Limiting**: GitHub API has rate limits (60 requests/hour for unauthenticated, 5000 for authenticated)
4. **Token Scopes**: Only request necessary scopes for your use case
5. **Environment Variables**: Use environment variables to manage sensitive data

## Limitations

- GitHub API rate limits apply
- Some operations require specific repository permissions
- OAuth 2.0 implementation can be added for enhanced security

## Future Enhancements

- [ ] OAuth 2.0 authentication
- [ ] Rate limiting middleware
- [ ] Request/response caching
- [ ] Webhook support
- [ ] Pull request creation and management
- [ ] Additional repository operations
- [ ] Docker containerization
- [ ] CI/CD pipeline

## Troubleshooting

### Invalid Token Error
Ensure your GitHub Personal Access Token is correctly set in the `.env` file and hasn't expired.

### 404 Not Found
Verify that the username/organization/repository name is correct.

### Rate Limiting
GitHub API has rate limits. Check the response headers for rate limit information.

### Connection Refused
Ensure the API server is running on the specified port.

## License

This project is provided as an assignment submission.

## Support

For issues or questions, please refer to the GitHub API documentation:
https://docs.github.com/en/rest

---

**Built with ❤️ using FastAPI and Python**
