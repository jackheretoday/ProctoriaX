# API Documentation

## Overview

Testing Platform REST API provides endpoints for authentication, user management, test management, question handling, and result processing.

**Base URL**: `http://localhost:5000`  
**API Version**: v1  
**Authentication**: Session-based (Flask-Login)

---

## Authentication Endpoints

### POST /auth/login
Login user and create session.

**Request**:
```json
{
  "username": "admin",
  "password": "Admin@123"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Login successful",
  "redirect": "/admin/dashboard"
}
```

### POST /auth/logout
Logout current user.

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

## Admin API

All admin endpoints require `@login_required` and `@admin_required`.

### GET /admin/api/dashboard
Get admin dashboard statistics.

**Response** (200 OK):
```json
{
  "total_users": 150,
  "total_tests": 25,
  "total_students": 120,
  "total_teachers": 10,
  "active_tests": 5,
  "recent_users": [...]
}
```

### POST /admin/api/users
Create new user.

**Request**:
```json
{
  "username": "student01",
  "email": "student01@example.com",
  "password": "Student@123",
  "full_name": "John Doe",
  "role": "student",
  "roll_number": "ST001"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "user_id": 15,
  "message": "User created successfully"
}
```

### DELETE /admin/api/users/<user_id>
Delete user by ID.

**Response** (200 OK):
```json
{
  "success": true,
  "message": "User deleted successfully"
}
```

---

## Teacher API

All teacher endpoints require `@login_required` and `@teacher_required`.

### GET /teacher/api/tests
Get all tests created by teacher.

**Response** (200 OK):
```json
{
  "success": true,
  "tests": [
    {
      "id": 1,
      "name": "Python Basics",
      "subject": "Python",
      "duration": 60,
      "question_count": 50,
      "is_published": true,
      "created_at": "2024-01-01T10:00:00"
    }
  ]
}
```

### POST /teacher/api/tests
Create new test.

**Request**:
```json
{
  "name": "Python Advanced",
  "subject": "Python",
  "duration": 90,
  "description": "Advanced Python concepts"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "test_id": 5,
  "message": "Test created successfully"
}
```

### POST /teacher/api/tests/<test_id>/questions/upload
Upload questions from Word/PowerPoint file.

**Request**: Form-data with file upload
- `file`: Document file (.docx or .pptx)
- `file_type`: "word" or "powerpoint"

**Response** (200 OK):
```json
{
  "success": true,
  "questions_created": 25,
  "message": "Questions uploaded successfully"
}
```

### GET /teacher/api/tests/<test_id>/results
Get results for specific test.

**Response** (200 OK):
```json
{
  "success": true,
  "statistics": {
    "total_attempts": 50,
    "average_score": 75.5,
    "highest_score": 95,
    "lowest_score": 45
  },
  "results": [
    {
      "student_name": "John Doe",
      "roll_number": "ST001",
      "score": 85,
      "percentage": 85.0,
      "completed_at": "2024-01-01T11:00:00"
    }
  ]
}
```

---

## Student API

All student endpoints require `@login_required` and `@student_required`.

### GET /student/api/dashboard
Get student dashboard data.

**Response** (200 OK):
```json
{
  "success": true,
  "todays_tests": [
    {
      "id": 1,
      "name": "Python Basics",
      "subject": "Python",
      "duration": 60,
      "status": "pending"
    }
  ],
  "upcoming_tests": [],
  "past_tests": []
}
```

### POST /student/tests/<test_id>/start
Start test and create session.

**Response** (200 OK):
```json
{
  "success": true,
  "test_id": 1,
  "start_time": "2024-01-01T10:00:00",
  "end_time": "2024-01-01T11:00:00",
  "duration": 60,
  "question_count": 50,
  "redirect_url": "/student/tests/1/question/1"
}
```

### POST /student/tests/<test_id>/submit-answer
Submit answer for current question.

**Request**:
```json
{
  "question_id": 15,
  "selected_answer": "B",
  "question_number": 5
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "last_question": false,
  "next_question": 6,
  "redirect_url": "/student/tests/1/question/6"
}
```

### POST /student/tests/<test_id>/submit
Submit entire test and calculate results.

**Response** (200 OK - redirects to results page)

### GET /student/api/tests/<test_id>/time-remaining
Server-side timer validation.

**Response** (200 OK):
```json
{
  "success": true,
  "expired": false,
  "remaining_seconds": 1800
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": "Invalid input data",
  "details": "Password must be at least 8 characters"
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "error": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "success": false,
  "error": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "success": false,
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Internal server error",
  "message": "An unexpected error occurred"
}
```

---

## Rate Limiting

Certain endpoints have rate limiting:
- Question upload: **10 requests per hour**
- Excel export: **5 requests per hour**
- Answer submission: **100 requests per hour**

Rate limit response (429):
```json
{
  "success": false,
  "error": "Rate limit exceeded",
  "retry_after": 3600
}
```

---

## Security

### Authentication
- Session-based authentication using Flask-Login
- Sessions expire after 30 minutes of inactivity
- CSRF protection on all POST/PUT/DELETE requests

### Encryption
- All sensitive data encrypted using AES-256-GCM
- Questions, answers, and explanations encrypted at rest
- Terms & conditions encrypted
- Excel exports encrypted before storage

### Access Control
- Role-based access control (RBAC)
- Three roles: admin, teacher, student
- Ownership verification on all resources
- Teachers can only access their own tests
- Students can only access assigned tests

---

## Example Workflows

### Complete Teacher Workflow
```bash
# 1. Login
POST /auth/login

# 2. Create test
POST /teacher/api/tests

# 3. Upload questions
POST /teacher/api/tests/1/questions/upload

# 4. Upload terms
POST /teacher/api/tests/1/terms

# 5. Publish test
POST /teacher/api/tests/1/publish

# 6. View results
GET /teacher/api/tests/1/results

# 7. Export to Excel
GET /teacher/api/tests/1/results/export
```

### Complete Student Workflow
```bash
# 1. Login
POST /auth/login

# 2. View dashboard
GET /student/api/dashboard

# 3. View instructions
GET /student/tests/1/instructions

# 4. Start test
POST /student/tests/1/start

# 5. Answer questions (loop)
POST /student/tests/1/submit-answer

# 6. Submit test
POST /student/tests/1/submit

# 7. View results
GET /student/tests/1/result

# 8. Review answers
GET /student/tests/1/review
```
