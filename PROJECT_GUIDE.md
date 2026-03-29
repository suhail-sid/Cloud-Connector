# GitHub Connector API - Complete Project Guide for Interviews

## 📌 Executive Summary

**What is this project?**

A **production-ready REST API** that connects to GitHub and allows you to manage repositories, issues, and commits programmatically. It's built with Python and FastAPI, demonstrating professional backend development skills.

**Why was it created?**

This project demonstrates:
- ✅ Integration with external APIs (GitHub)
- ✅ Secure authentication handling
- ✅ Professional error handling
- ✅ Clean code architecture
- ✅ RESTful API design
- ✅ Production-ready backend development

---

## 🎯 What Does This Project Do?

### Core Functionality

This API allows you to:

1. **Authenticate with GitHub** using Personal Access Token
2. **List user repositories** - See all repos of any GitHub user
3. **List organization repositories** - See all repos of any GitHub organization
4. **Manage issues** - View and create issues in any repository
5. **View commits** - See commit history of repositories
6. **Get user information** - Fetch GitHub user profile data
7. **Health monitoring** - Check API status anytime

---

## 🔑 Key Concepts Explained

### What is GitHub PAT (Personal Access Token)?

- **PAT** = A secure password-like token for API authentication
- It's like a special key that proves you are a valid GitHub user
- Safer than using your actual GitHub password
- Can be revoked anytime if compromised

**How we use it:**
- Store it in `.env` file (never share it)
- API uses it to make authenticated requests to GitHub
- GitHub trusts requests with valid PAT token

### What is REST API?

- **REST** = Representational State Transfer (a web standard)
- Uses standard **HTTP methods**: GET (fetch), POST (create), DELETE, PUT
- Uses **URLs/endpoints** to define operations
- Returns **JSON** (structured data)

**In our project:**
- `GET /repos/user/octocat` - Fetch octocat's repositories
- `POST /issues/octocat/Hello-World` - Create issue
- `GET /health` - Check if API is working

---

## 📚 Documentation URLs Explained

When you run the API (`python main.py`), you get three documentation URLs:

### 1️⃣ **Swagger UI** - `/docs`
**URL:** `http://localhost:8000/docs`

**What is it?**
- Interactive, visual interface to test your API
- Shows all endpoints with descriptions
- Let's you "try out" endpoints directly

**How to use it:**
1. Open the URL in browser
2. You'll see all available endpoints listed
3. Click on any endpoint to expand it
4. Click "Try it out" button
5. Enter any required parameters
6. Click "Execute"
7. See the response immediately

**Why show to interviewer?**
- Proves your API is well-documented
- Shows professional development practices
- Interactive demo is impressive
- Demonstrates understanding of API design

---

### 2️⃣ **ReDoc** - `/redoc`
**URL:** `http://localhost:8000/redoc`

**What is it?**
- Alternative documentation viewer
- More formal, professional appearance
- Better for reading documentation
- Organized in columns

**How to use it:**
1. Open the URL in browser
2. Browse through all endpoints
3. Read descriptions and examples
4. View request/response models
5. **Note:** Can't test endpoints from ReDoc

**Why show to interviewer?**
- Shows you understand different documentation formats
- Professional look for client presentations
- Good for code review and understanding

---

### 3️⃣ **OpenAPI JSON** - `/openapi.json`
**URL:** `http://localhost:8000/openapi.json`

**What is it?**
- Machine-readable API specification
- Standard format: OpenAPI/Swagger specification
- Used by other tools and systems
- Contains ALL API information in JSON format

**How to use it:**
1. Open URL in browser (or curl command)
2. You'll see raw JSON data
3. Contains endpoint definitions, parameters, response schemas
4. This is what Swagger UI and ReDoc use

**Example format:**
```json
{
  "openapi": "3.0.2",
  "info": {
    "title": "GitHub Connector API",
    "version": "1.0.0"
  },
  "paths": {
    "/health": {
      "get": {
        "summary": "Health check endpoint",
        ...
      }
    }
  }
}
```

**Why show to interviewer?**
- Demonstrates understanding of API standards
- Shows knowledge of OpenAPI specification
- Used for code generation and integrations

---

## 🧪 How to Test & Demo to Interviewer

### Setup for Demo

**Before interview, make sure:**
```bash
# 1. Add your GitHub token to .env file
# 2. Run the API
python main.py

# 3. Keep terminal open during interview
```

---

### Demo Flow (5-10 minutes)

#### **Part 1: Show the Documentation (2 minutes)**

1. **Open Swagger UI**
   ```
   Visit: http://localhost:8000/docs
   ```
   - Show all available endpoints
   - Explain what each endpoint does
   - Say: "This is auto-generated documentation that keeps our API well-documented"

2. **Show ReDoc**
   ```
   Visit: http://localhost:8000/redoc
   ```
   - Show more formal documentation
   - Say: "This is the formal documentation view, good for stakeholders"

3. **Show OpenAPI JSON**
   ```
   Visit: http://localhost:8000/openapi.json
   ```
   - Show raw JSON specification
   - Say: "This is the machine-readable specification that tools use"

---

#### **Part 2: Test Live Endpoints (5 minutes)**

**In Swagger UI (http://localhost:8000/docs), do this:**

##### **Test 1: Health Check**
1. Find "GET /health" endpoint
2. Click "Try it out"
3. Click "Execute"
4. Show response: `"status": "healthy"`
5. **Explain:** "This checks if our API and GitHub authentication are working"

---

##### **Test 2: Get Current User**
1. Find "GET /user" endpoint
2. Click "Try it out"
3. Click "Execute"
4. Show your GitHub username in response
5. **Explain:** "This fetches the authenticated user's information from GitHub"

---

##### **Test 3: Get User Repositories**
1. Find "GET /repos/user/{username}" endpoint
2. Click "Try it out"
3. Enter username: `torvalds` (Linus Torvalds - creator of Linux)
4. Leave per_page as 30
5. Click "Execute"
6. Show list of Linux kernel and other repos
7. **Explain:** "This fetches all public repositories of any GitHub user"

---

##### **Test 4: List Issues**
1. Find "GET /issues/{owner}/{repo}" endpoint
2. Click "Try it out"
3. Enter:
   - owner: `facebook`
   - repo: `react`
   - state: `open`
4. Click "Execute"
5. Show list of open React issues
6. **Explain:** "This shows all open issues in the React repository"

---

##### **Test 5: Create an Issue** (if you have permission)
1. Find "POST /issues/{owner}/{repo}" endpoint
2. Click "Try it out"
3. Enter:
   - owner: `your_username`
   - repo: `any_repo_you_own`
4. Request body:
   ```json
   {
     "title": "Test Issue from API",
     "body": "This issue was created using the GitHub Connector API",
     "labels": ["bug"]
   }
   ```
5. Click "Execute"
6. Show successful response with issue number
7. **Explain:** "This creates a real issue on GitHub programmatically"

---

##### **Test 6: Get Commits**
1. Find "GET /commits/{owner}/{repo}" endpoint
2. Click "Try it out"
3. Enter:
   - owner: `torvalds`
   - repo: `linux`
4. Click "Execute"
5. Show list of commits
6. **Explain:** "This fetches commit history of any repository"

---

### Using cURL for Testing (Alternative)

If Swagger UI doesn't work, use terminal commands:

```bash
# Test 1: Health Check
curl http://localhost:8000/health

# Test 2: Get Your User Info
curl http://localhost:8000/user

# Test 3: Get Torvalds' Repos
curl "http://localhost:8000/repos/user/torvalds?per_page=5"

# Test 4: Get React Issues
curl "http://localhost:8000/issues/facebook/react?state=open&per_page=5"

# Test 5: Get Linux Commits
curl "http://localhost:8000/commits/torvalds/linux?per_page=5"

# Test 6: Create an Issue (replace with your repo)
curl -X POST http://localhost:8000/issues/YOUR_USERNAME/YOUR_REPO \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Issue",
    "body": "Created via API",
    "labels": ["test"]
  }'
```

---

## 📊 How to Explain to Interviewer

### Opening Statement (1 minute)

> "This is a GitHub Connector API I built using Python and FastAPI. It demonstrates how to integrate with external APIs (GitHub in this case), handle authentication securely, and build a professional REST API.
> 
> The API allows users to list repositories, manage issues, view commits, and get user information - all by communicating with GitHub's API.
> 
> I've implemented proper error handling, input validation, and the entire codebase follows professional standards with type hints and documentation."

---

### Architecture Explanation (2 minutes)

Show the project structure:

```
main.py              → FastAPI application with endpoints
github_client.py     → GitHub API client (handles all API calls)
config.py            → Configuration management (loads .env file)
models.py            → Pydantic models (validates requests/responses)
exceptions.py        → Custom exceptions (proper error handling)
```

**Explain the flow:**

1. **User makes request** → `http://localhost:8000/repos/user/torvalds`
2. **FastAPI receives it** → `main.py` endpoint handler
3. **Validates input** → `models.py` checks data types
4. **Calls GitHub client** → `github_client.py` makes HTTP request
5. **GitHub returns data** → Client receives response
6. **Returns to user** → As JSON response

---

### Key Features to Highlight (2 minutes)

**1. Secure Authentication**
```
- GitHub PAT stored in .env file (never in code)
- Token validated on startup
- All requests authenticated with GitHub
```

**2. Error Handling**
```
- 5 custom exception types (AuthenticationError, NotFoundError, etc.)
- All errors return proper HTTP status codes (400, 401, 404, 500)
- Meaningful error messages for users
```

**3. Input Validation**
```
- Pydantic models validate all requests
- Type checking enforced
- Invalid inputs rejected with clear errors
```

**4. Professional Standards**
```
- 100% type hints
- Docstrings on all functions
- Clean, modular code
- Unit tests included
```

---

## 🔍 Deep Dive: Each Endpoint Explained

### 1. **GET /health** - Health Check
```
Purpose: Verify API is working and authenticated
Parameters: None
Response: {"status": "healthy", "authenticated": true, "user": "your_username"}
Use Case: Monitoring, status checks
```

---

### 2. **GET /user** - Get Current User
```
Purpose: Fetch your GitHub profile information
Parameters: None
Response: Your GitHub profile data (username, bio, followers, etc.)
Use Case: Verify authentication, get user info
```

---

### 3. **GET /repos/user/{username}** - Get User Repos
```
Purpose: List all repositories of a GitHub user
Parameters: 
  - username: GitHub username
  - per_page: How many repos to return (1-100)
Response: List of repositories with name, description, stars, forks
Use Case: Explore public repos, find projects
```

**Example:**
```
GET /repos/user/torvalds?per_page=10
Shows 10 most recent repos of Linus Torvalds
```

---

### 4. **GET /repos/org/{org_name}** - Get Organization Repos
```
Purpose: List all repositories of a GitHub organization
Parameters:
  - org_name: Organization name
  - per_page: How many repos to return (1-100)
Response: List of organization repositories
Use Case: Explore org projects, team collaboration tools
```

**Example:**
```
GET /repos/org/facebook?per_page=5
Shows 5 most recent repos from Facebook organization
```

---

### 5. **GET /issues/{owner}/{repo}** - List Issues
```
Purpose: Get all issues from a repository
Parameters:
  - owner: Repository owner username
  - repo: Repository name
  - state: "open" / "closed" / "all"
  - per_page: How many issues to return
Response: List of issues with title, description, state, etc.
Use Case: Track bugs, see project issues, project management
```

**Example:**
```
GET /issues/facebook/react?state=open&per_page=10
Shows 10 most recent open issues in React library
```

---

### 6. **POST /issues/{owner}/{repo}** - Create Issue
```
Purpose: Create a new issue in a repository
Parameters:
  - owner: Repository owner username
  - repo: Repository name
Request Body:
  {
    "title": "Issue title (required)",
    "body": "Issue description (optional)",
    "labels": ["bug", "feature"] (optional)
  }
Response: Created issue with issue number and details
Use Case: Report bugs, request features, project communication
```

**Example:**
```
POST /issues/yourname/yourrepo
{
  "title": "Bug: Login button not working",
  "body": "When I click login, nothing happens",
  "labels": ["bug"]
}
Creates a new issue on GitHub
```

---

### 7. **GET /commits/{owner}/{repo}** - Get Commits
```
Purpose: List commits from a repository
Parameters:
  - owner: Repository owner username
  - repo: Repository name
  - per_page: How many commits to return
Response: List of commits with SHA, message, author, date
Use Case: View project history, track changes, code review
```

**Example:**
```
GET /commits/torvalds/linux?per_page=5
Shows 5 most recent commits to Linux kernel
```

---

## ✅ Error Handling Demonstration

### Show Error Handling to Interviewer

**In Swagger UI, test error scenarios:**

#### **Scenario 1: Invalid Username**
1. GET /repos/user/{username}
2. Enter: `nonexistent_user_12345`
3. Execute
4. **Response:** 404 Not Found
   ```json
   {"detail": "User 'nonexistent_user_12345' not found on GitHub"}
   ```
5. **Explain:** "The API properly handles invalid input and returns meaningful error messages"

---

#### **Scenario 2: Invalid Repository**
1. GET /issues/{owner}/{repo}
2. Enter: owner: `torvalds`, repo: `nonexistent`
3. Execute
4. **Response:** 404 Not Found
   ```json
   {"detail": "Repository 'torvalds/nonexistent' not found"}
   ```
5. **Explain:** "Proper error handling with specific error codes"

---

#### **Scenario 3: Invalid Parameters**
1. GET /repos/user/{username}
2. Enter: username: `""` (empty)
3. Execute
4. **Response:** 400 Bad Request
   ```json
   {"detail": "Username is required"}
   ```
5. **Explain:** "Input validation happens before API calls"

---

## 📈 What Makes This Project Professional

1. **Proper Authentication** - Secure token management
2. **Error Handling** - All edge cases covered
3. **Input Validation** - Pydantic models ensure data quality
4. **Documentation** - Auto-generated Swagger/ReDoc
5. **Clean Code** - Type hints, docstrings, modular design
6. **Security** - No hardcoded credentials, environment-based config
7. **Testing** - Unit tests included
8. **Deployment Ready** - Docker support included

---

## 🎯 Interview Tips

### Things to Mention

✅ "I used FastAPI, which is a modern Python framework"
✅ "I implemented secure authentication with environment variables"
✅ "I added comprehensive error handling"
✅ "I used Pydantic for request/response validation"
✅ "The API is documented with Swagger UI and ReDoc"
✅ "I included unit tests"
✅ "The code is modular and maintainable"

### Things to Avoid

❌ Don't make excuses about simple things
❌ Don't claim features you didn't implement
❌ Don't skip explaining your code choices
❌ Don't ignore error handling

### Demo Checklist

- [ ] GitHub token added to .env
- [ ] `python main.py` running
- [ ] Open browser to http://localhost:8000/docs
- [ ] Test at least 3 endpoints live
- [ ] Show error handling
- [ ] Explain architecture
- [ ] Show code (models.py, main.py)

---

## 🚀 Live Demo Script (5 minutes)

```
1. "Let me show you the API documentation..."
   → Open /docs in browser

2. "This is an interactive interface where I can test endpoints..."
   → Click on GET /health, hit Execute

3. "Let me show you a more complex example..."
   → Click on GET /repos/user/{username}
   → Enter "torvalds"
   → Show Linux repos

4. "Here's error handling in action..."
   → Enter invalid username
   → Show 404 response

5. "The code is well-organized..."
   → Show main.py structure
   → Show github_client.py
   → Show error handling

6. "I implemented proper validation..."
   → Show models.py
   → Show Pydantic validators

7. "Everything is documented..."
   → Show /redoc
   → Show /openapi.json
```

---

## 📝 Sample Questions & Answers

**Q: Why did you use FastAPI?**
A: "FastAPI is modern, fast, and auto-generates documentation. It's perfect for building professional APIs quickly."

**Q: How do you handle authentication?**
A: "I use GitHub Personal Access Token stored in environment variables, never hardcoded. It's validated on startup."

**Q: What about error handling?**
A: "I have custom exception types for different scenarios - AuthenticationError, NotFoundError, ValidationError - each returning proper HTTP status codes."

**Q: How would you scale this?**
A: "I could add caching with Redis, implement rate limiting, use async/await for concurrent requests, and deploy with Docker."

**Q: Is this production-ready?**
A: "Yes - it has proper error handling, input validation, logging, security best practices, and is containerized with Docker."

---

## 🎊 Final Tips for Interview

1. **Start Simple** - Explain basic concept first, then details
2. **Show Code** - Be prepared to show your source files
3. **Live Demo** - The interactive Swagger UI is your best friend
4. **Explain Choices** - Why FastAPI? Why Pydantic? Why these endpoints?
5. **Show Testing** - Show that you tested error scenarios
6. **Mention DevOps** - Docker files show production mindset
7. **Security** - Highlight .env file, no hardcoded secrets
8. **Documentation** - This README and auto-generated docs show professionalism

---

**Good luck with your interview! You've built a professional-grade API.** 🚀

