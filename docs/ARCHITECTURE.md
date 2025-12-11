# System Architecture

## Overview

The Testing Platform follows a **3-tier MVC architecture** with Flask as the web framework, MySQL/PostgreSQL for data persistence, and a service-oriented design pattern.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
├─────────────────────────────────────────────────────────────┤
│  Web Browsers (Chrome, Firefox, Edge)                        │
│  - Admin Dashboard                                            │
│  - Teacher Panel                                              │
│  - Student Test Interface                                     │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS
┌────────────────────▼────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
├─────────────────────────────────────────────────────────────┤
│  Flask Templates (Jinja2)                                    │
│  ├── Admin Templates                                         │
│  ├── Teacher Templates                                       │
│  └── Student Templates                                       │
│                                                               │
│  Static Assets                                                │
│  ├── CSS (Bootstrap 5, Custom)                               │
│  ├── JavaScript (Timer, Navigation Control)                  │
│  └── Images                                                   │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
├─────────────────────────────────────────────────────────────┤
│  Flask Blueprints                                            │
│  ├── auth_bp       (Authentication)                          │
│  ├── admin_bp      (Admin Module)                            │
│  ├── teacher_bp    (Teacher Module)                          │
│  └── student_bp    (Student Module)                          │
│                                                               │
│  Middleware                                                   │
│  ├── Authentication (Flask-Login)                            │
│  ├── CSRF Protection                                          │
│  ├── Rate Limiting (Flask-Limiter)                           │
│  └── Session Management                                       │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                     BUSINESS LAYER                           │
├─────────────────────────────────────────────────────────────┤
│  Services                                                     │
│  ├── AuthService         (User authentication)               │
│  ├── UserService         (User management)                   │
│  ├── TestService         (Test CRUD)                         │
│  ├── QuestionService     (Question management)               │
│  ├── FileParserService   (Document parsing)                  │
│  ├── TermsService        (T&C management)                    │
│  ├── ResultService       (Results processing)                │
│  ├── ExcelService        (Excel generation)                  │
│  └── EncryptionService   (Data encryption)                   │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                      DATA LAYER                              │
├─────────────────────────────────────────────────────────────┤
│  ORM (SQLAlchemy)                                            │
│  Models                                                       │
│  ├── User                                                     │
│  ├── Test                                                     │
│  ├── Question                                                 │
│  ├── TermsConditions                                          │
│  ├── Assignment                                               │
│  ├── Result                                                   │
│  └── AuditLog                                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                   PERSISTENCE LAYER                          │
├─────────────────────────────────────────────────────────────┤
│  Database (MySQL/PostgreSQL/SQLite)                          │
│  ├── Users Table                                              │
│  ├── Tests Table                                              │
│  ├── Questions Table                                          │
│  ├── Results Table                                            │
│  └── Assignments Table                                        │
│                                                               │
│  File Storage                                                 │
│  ├── storage/encrypted/results/ (Encrypted Excel files)      │
│  └── storage/uploads/ (Temporary uploads)                    │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Breakdown

### 1. Client Layer
- **Purpose**: User interface interaction
- **Technology**: Modern web browsers
- **Features**: Responsive design, mobile-friendly

### 2. Presentation Layer
- **Templates**: Jinja2 for server-side rendering
- **Static Assets**: CSS (Bootstrap 5 + custom), JavaScript
- **Key JS Components**:
  - Test timer (countdown, auto-submit)
  - Navigation control (disable back button)
  - Form validation
  - AJAX handlers

### 3. Application Layer (Controllers)
- **Blueprints**: Modular route organization
  - `auth_bp`: Login, logout, session management
  - `admin_bp`: User management, system oversight
  - `teacher_bp`: Test creation, question upload, results
  - `student_bp`: Test-taking interface, results viewing
  
### 4. Business Layer (Services)
- **Design Pattern**: Service-oriented architecture
- **Responsibilities**:
  - Business logic isolation
  - Data transformation
  - Validation
  - Encryption/Decryption
  - File processing

### 5. Data Layer (Models)
- **ORM**: SQLAlchemy
- **Design**: Normalized relational database
- **Key Relationships**:
  - User → Tests (one-to-many)
  - Test → Questions (one-to-many)
  - Test → Assignments (one-to-many)
  - Student → Results (one-to-many)

### 6. Persistence Layer
- **Database**: Relational (MySQL/PostgreSQL)
- **File Storage**: Encrypted file system
- **Backups**: Automated daily backups

---

## Data Flow

### Teacher Creating Test
```
Teacher → Create Test Form → POST /teacher/api/tests
                           ↓
                    TestService.create_test()
                           ↓
                    Test Model (SQLAlchemy)
                           ↓
                      Database INSERT
                           ↓
                    Return test_id
```

### Student Taking Test
```
Student → Start Test → POST /student/tests/<id>/start
                    ↓
            Create session (start_time, end_time)
                    ↓
        Load Question 1 → EncryptionService.decrypt()
                    ↓
        Display ONE question with timer
                    ↓
        Submit Answer → Store in session
                    ↓
        Load Next Question (repeat)
                    ↓
        Submit Test → Calculate score
                    ↓
        Create Result record
                    ↓
        Display immediate results
```

---

## Security Architecture

```
┌─────────────────────────────────────────┐
│          Security Layers                │
├─────────────────────────────────────────┤
│ 1. Transport Layer                      │
│    └── HTTPS/TLS                        │
├─────────────────────────────────────────┤
│ 2. Authentication Layer                 │
│    ├── Flask-Login (Sessions)           │
│    └── Bcrypt (Password hashing)        │
├─────────────────────────────────────────┤
│ 3. Authorization Layer                  │
│    ├── RBAC (admin/teacher/student)     │
│    └── Ownership checks                 │
├─────────────────────────────────────────┤
│ 4. Application Layer                    │
│    ├── CSRF Protection                  │
│    ├── Rate Limiting                    │
│    └── Input Validation                 │
├─────────────────────────────────────────┤
│ 5. Data Layer                           │
│    ├── AES-256-GCM Encryption           │
│    ├── Encrypted Questions/Answers      │
│    └── Encrypted Excel Exports          │
├─────────────────────────────────────────┤
│ 6. Audit Layer                          │
│    └── Comprehensive logging            │
└─────────────────────────────────────────┘
```

---

## Technology Stack

### Backend
- **Framework**: Flask 3.0
- **ORM**: SQLAlchemy 2.0
- **Authentication**: Flask-Login
- **Encryption**: cryptography (Fernet)
- **File Parsing**: python-docx, python-pptx
- **Excel**: openpyxl
- **Rate Limiting**: Flask-Limiter

### Frontend
- **CSS Framework**: Bootstrap 5.3
- **JavaScript**: Vanilla JS (no dependencies)
- **Icons**: Bootstrap Icons

### Database
- **Primary**: MySQL 8.0 / PostgreSQL 14
- **Development**: SQLite 3
- **Migration**: Flask-Migrate (Alembic)

### DevOps
- **Server**: Gunicorn (WSGI)
- **Proxy**: Nginx
- **Container**: Docker (optional)
- **Testing**: pytest

---

## Deployment Architecture

```
┌────────────────────────────────────┐
│         Internet                   │
└────────┬───────────────────────────┘
         │
┌────────▼───────────────────────────┐
│      Nginx (Reverse Proxy)         │
│      - SSL/TLS Termination         │
│      - Static file serving         │
│      - Load balancing              │
└────────┬───────────────────────────┘
         │
┌────────▼───────────────────────────┐
│   Gunicorn (WSGI Server)           │
│   - 4 worker processes             │
│   - Flask application              │
└────────┬───────────────────────────┘
         │
┌────────▼───────────────────────────┐
│   MySQL/PostgreSQL Database        │
│   - Persistent storage             │
│   - Automated backups              │
└────────────────────────────────────┘
```

---

## Design Patterns

### 1. MVC Pattern
- **Model**: SQLAlchemy models
- **View**: Jinja2 templates
- **Controller**: Flask blueprints

### 2. Service Layer Pattern
- Business logic separated from controllers
- Reusable service classes
- Clean separation of concerns

### 3. Repository Pattern
- Data access abstraction
- SQLAlchemy ORM as repository

### 4. Factory Pattern
- Application factory (`create_app()`)
- Supports multiple environments

### 5. Singleton Pattern
- EncryptionService (single instance)
- Database connection pool

---

## Scalability Considerations

### Horizontal Scaling
- Stateless application design
- Session storage in Redis (future)
- Load balancer ready

### Vertical Scaling
- Database connection pooling
- Efficient queries with indexes
- Caching layer (future)

### Performance Optimization
- Lazy loading for large datasets
- Pagination for results
- Encrypted data cached temporarily
- Static file CDN (future)

---

## File Structure

```
testing-platform/
├── app/
│   ├── __init__.py                 # App factory
│   ├── api/v1/                     # API blueprints
│   │   ├── auth.py
│   │   ├── admin.py
│   │   ├── teacher.py
│   │   └── student.py
│   ├── models/                     # Database models
│   ├── services/                   # Business logic
│   ├── templates/                  # Jinja2 templates
│   ├── static/                     # CSS, JS, images
│   └── utils/                      # Utilities
├── tests/                          # Test suite
├── docs/                           # Documentation
├── scripts/                        # Utility scripts
├── storage/                        # File storage
├── migrations/                     # Database migrations
├── config.py                       # Configuration
├── requirements.txt                # Dependencies
└── run.py                          # Entry point
```

---

## Database Schema

### Users Table
```sql
- id (PK)
- username (unique)
- email (unique)
- password_hash
- role (admin/teacher/student)
- full_name
- roll_number (students only)
- is_active
- created_at
```

### Tests Table
```sql
- id (PK)
- name
- subject
- duration (minutes)
- description
- created_by (FK → users.id)
- is_published
- is_active
- created_at
```

### Questions Table
```sql
- id (PK)
- test_id (FK → tests.id)
- question_number
- encrypted_question
- encrypted_options
- encrypted_answer
- encrypted_explanation
- created_at
```

### Results Table
```sql
- id (PK)
- student_id (FK → users.id)
- test_id (FK → tests.id)
- total_questions
- correct_answers
- wrong_answers
- unattempted
- score
- percentage
- time_taken
- status
- completed_at
```

---

## Integration Points

### External Libraries
- **python-docx**: Word document parsing
- **python-pptx**: PowerPoint parsing
- **openpyxl**: Excel generation
- **cryptography**: AES encryption

### Future Integrations
- Email notifications (SMTP)
- SMS alerts (Twilio)
- Cloud storage (AWS S3)
- Analytics (Google Analytics)
- Monitoring (Sentry)

---

**Architecture Version**: 1.0  
**Last Updated**: 2024  
**Author**: Development Team
