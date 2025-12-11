# PART 1: Core Infrastructure & Security
**Team Member**: 1  
**Complexity**: High  
**Priority**: CRITICAL - Must Complete First  
**Estimated Time**: 1 week

---

## 🎯 Your Responsibilities
- Set up entire project foundation
- Database configuration and models
- Security implementation (AES-256)
- Authentication & Authorization
- Base templates and login system

---

## 📁 Your Files

### Root Level (9 files)
```
✓ .env.example
✓ .gitignore
✓ requirements.txt
✓ requirements-dev.txt
✓ pytest.ini
✓ run.py
✓ wsgi.py
✓ docker-compose.yml
✓ README.md (initial)
```

### Configuration (6 files)
```
✓ app/config/__init__.py
✓ app/config/base.py
✓ app/config/development.py
✓ app/config/production.py
✓ app/config/testing.py
✓ app/config/security.py
```

### Database Models (9 files)
```
✓ app/models/__init__.py
✓ app/models/user.py (User, Teacher, Admin roles)
✓ app/models/test.py
✓ app/models/question.py
✓ app/models/assignment.py
✓ app/models/result.py
✓ app/models/terms_conditions.py
✓ app/models/audit_log.py
✓ app/models/mixins.py
```

### Extensions (6 files)
```
✓ app/extensions/__init__.py
✓ app/extensions/database.py
✓ app/extensions/login_manager.py
✓ app/extensions/session_manager.py
✓ app/extensions/cache.py
✓ app/extensions/limiter.py
```

### Middleware (7 files)
```
✓ app/middleware/__init__.py
✓ app/middleware/authentication.py
✓ app/middleware/authorization.py
✓ app/middleware/rate_limiter.py
✓ app/middleware/audit_logger.py
✓ app/middleware/session_security.py
✓ app/middleware/error_handler.py
```

### Core Services (3 files)
```
✓ app/services/encryption_service.py (AES-256)
✓ app/services/auth_service.py
✓ app/services/session_service.py
```

### Utilities (6 files)
```
✓ app/utils/__init__.py
✓ app/utils/decorators.py
✓ app/utils/validators.py
✓ app/utils/helpers.py
✓ app/utils/constants.py
✓ app/utils/exceptions.py
```

### Base Templates (6 files)
```
✓ app/templates/base.html
✓ app/templates/auth/login.html
✓ app/templates/auth/change_password.html
✓ app/templates/errors/403.html
✓ app/templates/errors/404.html
✓ app/templates/errors/500.html
✓ app/templates/errors/session_expired.html
```

### API Auth (2 files)
```
✓ app/api/v1/auth.py
✓ app/api/__init__.py
✓ app/api/v1/__init__.py
```

### Scripts (2 files)
```
✓ scripts/init_db.py
✓ scripts/create_admin.py
```

**Total: ~57 files**

---

## ✅ Task Checklist

### Phase 1: Project Setup (Day 1)
- [ ] Create virtual environment
- [ ] Install Flask and core dependencies
- [ ] Create `.env.example` with all environment variables
- [ ] Write `requirements.txt` with version numbers
- [ ] Set up `.gitignore` (Python, IDE, environment files)
- [ ] Write basic `README.md` with setup instructions
- [ ] Create `run.py` for development server
- [ ] Create `wsgi.py` for production

### Phase 2: Configuration (Day 1-2)
- [ ] `config/base.py`: Common config (SECRET_KEY, DATABASE_URI)
- [ ] `config/development.py`: Debug mode ON, SQLite
- [ ] `config/production.py`: Debug OFF, security headers
- [ ] `config/testing.py`: Test database config
- [ ] `config/security.py`: AES key, session timeout, CORS

### Phase 3: Database Setup (Day 2-3)
- [ ] `extensions/database.py`: Initialize SQLAlchemy
- [ ] `models/mixins.py`: TimestampMixin, EncryptedFieldMixin
- [ ] `models/user.py`:
  - User model with role (admin/teacher/student)
  - Password hashing (bcrypt)
  - username, email, password_hash, role, is_active
- [ ] `models/test.py`:
  - Test model: name, subject, duration, created_by, start_date, end_date
- [ ] `models/question.py`:
  - Question: test_id, encrypted_content, encrypted_answer, question_number
- [ ] `models/assignment.py`:
  - Assignment: student_id, test_id, assigned_date, status
- [ ] `models/result.py`:
  - Result: student_id, test_id, score, total_questions, percentage, completed_at
- [ ] `models/terms_conditions.py`:
  - TermsConditions: test_id, encrypted_content, created_at
- [ ] `models/audit_log.py`:
  - AuditLog: user_id, action, ip_address, timestamp, details

### Phase 4: Security - Encryption (Day 3)
- [ ] `services/encryption_service.py`:
  - `generate_key()`: Generate AES-256 key
  - `encrypt_data(plain_text)`: Encrypt using AES-256-GCM
  - `decrypt_data(encrypted_data)`: Decrypt
  - `encrypt_file(file_path)`: Encrypt file
  - `decrypt_file(file_path)`: Decrypt file
- [ ] Test encryption/decryption with sample data
- [ ] Store encryption key securely in environment variable

### Phase 5: Authentication (Day 4)
- [ ] `services/auth_service.py`:
  - `hash_password(password)`: Hash using bcrypt
  - `verify_password(password, hash)`: Verify password
  - `authenticate_user(username, password)`: Login logic
  - `create_session(user)`: Create user session
  - `destroy_session()`: Logout
- [ ] `extensions/login_manager.py`: Flask-Login setup
- [ ] `extensions/session_manager.py`: Session configuration
- [ ] `services/session_service.py`: Session timeout, validation

### Phase 6: Middleware (Day 4-5)
- [ ] `middleware/authentication.py`:
  - `@login_required` decorator
  - Verify user session before each request
- [ ] `middleware/authorization.py`:
  - `@role_required(role)` decorator
  - Check if user has required role (admin/teacher/student)
- [ ] `middleware/rate_limiter.py`:
  - Limit login attempts (5 per minute)
  - Limit API calls per user
- [ ] `middleware/audit_logger.py`:
  - Log all important actions (login, logout, data access)
  - Store in audit_log table
- [ ] `middleware/session_security.py`:
  - Check session expiry
  - Regenerate session ID periodically
- [ ] `middleware/error_handler.py`:
  - Handle 403, 404, 500 errors
  - Log errors securely (no sensitive data in logs)

### Phase 7: Utilities (Day 5)
- [ ] `utils/constants.py`:
  - USER_ROLES = ['admin', 'teacher', 'student']
  - MAX_TERMS_BULLETS = 10
  - SESSION_TIMEOUT = 3600
- [ ] `utils/decorators.py`:
  - `@validate_input` decorator
  - `@cache_result` decorator
- [ ] `utils/validators.py`:
  - `validate_email(email)`
  - `validate_password_strength(password)`
  - `validate_role(role)`
- [ ] `utils/helpers.py`:
  - `generate_random_password()`
  - `format_datetime(dt)`
  - `sanitize_filename(filename)`
- [ ] `utils/exceptions.py`:
  - Custom exceptions: `AuthenticationError`, `AuthorizationError`, `EncryptionError`

### Phase 8: API - Authentication (Day 6)
- [ ] `api/v1/auth.py`:
  - `POST /api/v1/auth/login`: Login endpoint
  - `POST /api/v1/auth/logout`: Logout endpoint
  - `GET /api/v1/auth/current-user`: Get current user info
  - `POST /api/v1/auth/change-password`: Change password

### Phase 9: Templates (Day 6-7)
- [ ] `templates/base.html`:
  - Bootstrap 5 layout
  - Header with org name, logout button
  - Flash message display
  - Block for content
- [ ] `templates/auth/login.html`:
  - Username and password fields
  - Login button
  - Error message display
  - Clean, professional design
- [ ] `templates/auth/change_password.html`:
  - Old password, new password, confirm password
- [ ] `templates/errors/403.html`: Access Denied
- [ ] `templates/errors/404.html`: Page Not Found
- [ ] `templates/errors/500.html`: Server Error
- [ ] `templates/errors/session_expired.html`: Session expired message

### Phase 10: Database Scripts (Day 7)
- [ ] `scripts/init_db.py`:
  - Drop all tables
  - Create all tables
  - Run with: `python scripts/init_db.py`
- [ ] `scripts/create_admin.py`:
  - Create first admin user
  - Username: admin
  - Generate random password and print it
  - Run with: `python scripts/create_admin.py`

### Phase 11: Testing & Documentation (Day 7)
- [ ] Test database connection
- [ ] Test user creation
- [ ] Test encryption/decryption
- [ ] Test login functionality
- [ ] Test role-based access
- [ ] Document setup steps in README
- [ ] Create sample `.env` file
- [ ] Write API documentation for auth endpoints

---

## 🔧 Key Libraries You Need

```txt
# Core
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
python-dotenv==1.0.0

# Database
SQLAlchemy==2.0.23

# Security
cryptography==41.0.7
bcrypt==4.1.2
Flask-Limiter==3.5.0

# Development
pytest==7.4.3
```

---

## 🔐 Security Requirements YOU Must Implement

1. **AES-256-GCM Encryption**:
   - Questions encrypted at rest
   - Answers encrypted at rest
   - Terms & conditions encrypted
   - Results encrypted in Excel

2. **Password Security**:
   - Hash passwords with bcrypt (cost factor 12)
   - Enforce strong passwords (8+ chars, mixed case, numbers)

3. **Session Security**:
   - Secure session cookies (HttpOnly, Secure, SameSite)
   - Session timeout after 1 hour of inactivity
   - Regenerate session ID after login

4. **Audit Logging**:
   - Log all logins (success and failure)
   - Log all data access
   - Log all administrative actions

5. **Rate Limiting**:
   - Max 5 login attempts per minute per IP
   - Max 100 API requests per hour per user

---

## 📤 What Other Team Members Need from You

### For Admin Module (Member 2):
- User model with CRUD operations
- Role-based authorization working
- Database initialized

### For Teacher Module (Member 3):
- Question and Test models
- Encryption service API
- File storage structure

### For Student Module (Member 4):
- Assignment and Result models
- Authentication working
- Session management

### For Testing (Member 5):
- All models with test data seeding capability
- Clear API contracts

---

## 🚨 Critical Notes

1. **Start with database models** - everything depends on this
2. **Test encryption early** - it's critical for the project
3. **Make sure authentication works** - others can't test without login
4. **Document your functions** - others will use your code
5. **Use environment variables** - never hardcode secrets
6. **Create sample .env** - with dummy values for others to copy

---

## 📊 Deliverables Checklist

At the end of your part, others should be able to:
- [ ] Clone repo and run the application
- [ ] Log in as admin/teacher/student
- [ ] See role-based access control working
- [ ] Access encrypted storage through your service
- [ ] Create new users via database script
- [ ] Run the application without errors

---

## 🆘 When You're Stuck

1. **Encryption issues**: Check `cryptography` documentation
2. **Database errors**: Verify model relationships
3. **Login not working**: Check Flask-Login configuration
4. **Session issues**: Verify SECRET_KEY is set

---

## 📞 Communication

**Update team daily on**:
- Models completed (so others can start using them)
- Encryption service ready (Part 3 needs this)
- Authentication working (everyone needs this)
- Any changes to database schema

**Good luck! You're building the foundation! 🚀**
