# Project Division Guide - Testing Platform

## Team Structure (5 Members)

This document outlines how to divide the Testing Platform project among 5 team members.

---

## 🎯 OPTION 1: Division by Role/Feature (RECOMMENDED)

### **PART 1: Core Infrastructure & Security** 👤 Team Member 1
**Complexity**: High | **Priority**: Critical | **Must Complete First**

#### Responsibilities:
- Set up project foundation
- Database configuration
- Security implementation
- Encryption services

#### Files to Work On:

**Root Level:**
```
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── run.py
├── wsgi.py
└── docker-compose.yml
```

**Core Application:**
```
├── app/
│   ├── __init__.py (Application Factory)
│   ├── config/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   ├── testing.py
│   │   └── security.py
│   ├── extensions/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── login_manager.py
│   │   ├── session_manager.py
│   │   ├── cache.py
│   │   └── limiter.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── test.py
│   │   ├── question.py
│   │   ├── assignment.py
│   │   ├── result.py
│   │   ├── terms_conditions.py
│   │   ├── audit_log.py
│   │   └── mixins.py
```

**Security Components:**
```
├── app/
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── authentication.py
│   │   ├── authorization.py
│   │   ├── rate_limiter.py
│   │   ├── audit_logger.py
│   │   ├── session_security.py
│   │   └── error_handler.py
│   ├── services/
│   │   ├── encryption_service.py (AES-256)
│   │   ├── auth_service.py
│   │   └── session_service.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── decorators.py
│   │   ├── validators.py
│   │   ├── helpers.py
│   │   ├── constants.py
│   │   └── exceptions.py
```

**Base Templates:**
```
├── app/templates/
│   ├── base.html
│   ├── auth/
│   │   ├── login.html
│   │   └── change_password.html
│   └── errors/
│       ├── 403.html
│       ├── 404.html
│       ├── 500.html
│       └── session_expired.html
```

**Scripts:**
```
├── scripts/
│   ├── init_db.py
│   └── create_admin.py
```

#### Key Tasks:
- [ ] Set up Flask application factory
- [ ] Configure SQLAlchemy with SQLite/MySQL
- [ ] Implement AES-256 encryption service
- [ ] Create all database models
- [ ] Set up authentication & authorization middleware
- [ ] Implement session management
- [ ] Create base HTML template
- [ ] Set up login page
- [ ] Create database initialization script
- [ ] Write requirements.txt with all dependencies

---

### **PART 2: Admin Module** 👤 Team Member 2
**Complexity**: Medium | **Priority**: High | **Dependencies**: Part 1

#### Responsibilities:
- Admin dashboard
- User management (CRUD for users/teachers/admins)
- Test assignment to students
- System logs viewing

#### Files to Work On:

**Backend - Admin API:**
```
├── app/api/v1/
│   └── admin.py
├── app/services/
│   └── user_service.py
```

**Frontend - Admin Templates:**
```
├── app/templates/admin/
│   ├── base_admin.html
│   ├── dashboard.html
│   ├── manage_users.html
│   ├── create_user.html
│   ├── assign_tests.html
│   ├── manage_test_dates.html
│   └── system_logs.html
```

**Styling:**
```
├── app/static/css/
│   └── admin.css
```

#### Key Tasks:
- [ ] Create admin API endpoints (provision users, assign tests)
- [ ] Implement user service (create/update/delete users)
- [ ] Design admin dashboard UI
- [ ] Create user management interface
- [ ] Build test assignment interface with date picker
- [ ] Implement system logs viewer
- [ ] Style admin pages
- [ ] Test role-based access control for admin

---

### **PART 3: Teacher Module** 👤 Team Member 3
**Complexity**: High | **Priority**: High | **Dependencies**: Part 1

#### Responsibilities:
- Question upload (Word/PowerPoint parsing)
- Terms & conditions upload
- Results viewing
- Excel export functionality

#### Files to Work On:

**Backend - Teacher API:**
```
├── app/api/v1/
│   └── teacher.py
├── app/services/
│   ├── question_service.py
│   ├── file_parser_service.py (Word/PPT parsing)
│   ├── excel_service.py
│   ├── terms_service.py
│   └── result_service.py
```

**Frontend - Teacher Templates:**
```
├── app/templates/teacher/
│   ├── base_teacher.html
│   ├── dashboard.html
│   ├── upload_questions.html
│   ├── manage_tests.html
│   ├── view_results.html
│   ├── export_results.html
│   └── upload_terms.html
```

**Styling:**
```
├── app/static/css/
│   └── teacher.css
```

#### Key Tasks:
- [ ] Create teacher API endpoints
- [ ] Implement Word document parser (python-docx)
- [ ] Implement PowerPoint parser (python-pptx)
- [ ] Parse questions (numbered format for Word, 1 per slide for PPT)
- [ ] Implement terms & conditions service (max 10 bullets validation)
- [ ] Create question encryption before storage
- [ ] Build results viewing interface
- [ ] Implement Excel export (openpyxl) with columns: Name, ID, Total, Correct, Percentage
- [ ] Encrypt Excel results file
- [ ] Design teacher dashboard
- [ ] Test file upload and parsing

---

### **PART 4: Student Module** 👤 Team Member 4
**Complexity**: High | **Priority**: Critical | **Dependencies**: Part 1, Part 3

#### Responsibilities:
- Student dashboard (view assigned tests)
- Test taking interface (one question per page)
- Timer implementation
- Navigation prevention
- Results display
- Answer review

#### Files to Work On:

**Backend - Student API:**
```
├── app/api/v1/
│   └── student.py
├── app/services/
│   └── test_service.py
```

**Frontend - Student Templates:**
```
├── app/templates/student/
│   ├── base_student.html
│   ├── dashboard.html
│   ├── test_instructions.html (Shows T&C)
│   ├── take_test.html (ONE question per page)
│   ├── test_result.html (Immediate results)
│   └── review_answers.html
```

**JavaScript - Test Logic:**
```
├── app/static/js/
│   ├── test-timer.js (Running clock, no stop)
│   ├── disable-back.js (Disable browser back)
│   ├── prevent-navigation.js (Disable all navigation)
│   ├── auto-submit.js (Auto-submit on timer end)
│   └── form-validator.js
```

**Styling:**
```
├── app/static/css/
│   └── student.css
```

#### Key Tasks:
- [ ] Create student API endpoints
- [ ] Implement test service (fetch assigned tests, decrypt questions)
- [ ] Build student dashboard showing today's tests
- [ ] Create test instructions page with T&C
- [ ] Design test-taking interface (1 question per page, no going back)
- [ ] Implement running timer (display prominently)
- [ ] Disable browser back button using JavaScript
- [ ] Prevent page navigation during test
- [ ] Implement auto-submit when timer expires
- [ ] Show immediate results after submission (Name, Total, Correct, Percentage)
- [ ] Create answer review page (with correct answers)
- [ ] Style student pages with focus on UX
- [ ] Test timer accuracy and navigation blocking

---

### **PART 5: Testing, Documentation & DevOps** 👤 Team Member 5
**Complexity**: Medium | **Priority**: High | **Can Start Early**

#### Responsibilities:
- Write unit tests
- Integration testing
- API documentation
- Architecture diagram
- Security documentation
- Deployment guide

#### Files to Work On:

**Testing:**
```
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_services.py
│   ├── test_api.py
│   ├── test_encryption.py
│   ├── test_security.py
│   └── test_integration.py
```

**Documentation:**
```
├── docs/
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── SECURITY.md
│   ├── DEPLOYMENT.md
│   └── USER_MANUAL.md
├── README.md
```

**Scripts:**
```
├── scripts/
│   ├── backup_db.py
│   ├── seed_data.py
│   └── generate_architecture.py
```

**Common Components:**
```
├── app/api/
│   ├── validators.py
│   └── v1/common.py
├── app/static/
│   ├── css/main.css
│   └── js/
│       ├── main.js
│       └── ajax-handler.js
```

#### Key Tasks:
- [ ] Write unit tests for all models
- [ ] Write tests for encryption service (AES-256)
- [ ] Test all API endpoints
- [ ] Write integration tests (user flows)
- [ ] Test security features (SQL injection, XSS, CSRF)
- [ ] Document all API endpoints (request/response formats)
- [ ] Create architecture diagram (using diagrams.py or draw.io)
- [ ] Document implemented cyber security principles
- [ ] Write deployment guide
- [ ] Create user manual for all three roles
- [ ] Write comprehensive README
- [ ] Create database seeding script with sample data
- [ ] Implement database backup script
- [ ] Set up common validators and utilities
- [ ] Create main.css for shared styles

---

## 📅 Development Timeline (Suggested)

### **Week 1: Foundation** (Oct 29 - Nov 4)
- **Member 1**: Complete Part 1 (Core Infrastructure)
- **Member 5**: Start documentation structure, README

### **Week 2: Module Development** (Nov 5 - Nov 11)
- **Member 2**: Complete Admin Module (Part 2)
- **Member 3**: Complete Teacher Module (Part 3)
- **Member 4**: Start Student Module (Part 4)
- **Member 5**: Write tests for completed modules

### **Week 3: Integration & Testing** (Nov 12 - Nov 18)
- **Member 4**: Complete Student Module
- **All Members**: Integration testing
- **Member 5**: Complete all documentation

### **Week 4: Final Polish** (Nov 19 - Nov 25)
- **All Members**: Bug fixes, UI polish
- **Member 5**: Final testing, deployment guide
- **All Members**: Prepare presentation

### **Demo Day**: November 1, 2025 (12:00 PM)

---

## 🔄 Integration Points (Where modules connect)

### Critical Interfaces:

1. **Part 1 → All Parts**
   - Database models must be complete first
   - Authentication/Authorization middleware
   - Encryption service API

2. **Part 3 → Part 4**
   - Question format from teacher upload
   - Decryption method for test-taking
   - Terms & conditions display

3. **Part 2 → Part 4**
   - Test assignment data structure
   - Student-test mapping

4. **Part 4 → Part 3**
   - Result submission format
   - Data for Excel export

---

## 📝 Communication & Coordination

### Daily Standup (Recommended):
- What did you complete yesterday?
- What will you work on today?
- Any blockers?

### Version Control Strategy:
```
main
├── dev
│   ├── feature/core-infrastructure (Member 1)
│   ├── feature/admin-module (Member 2)
│   ├── feature/teacher-module (Member 3)
│   ├── feature/student-module (Member 4)
│   └── feature/testing-docs (Member 5)
```

### Code Review:
- Each member reviews at least one other member's code
- Member 1 (infrastructure) reviews security-critical code
- Member 5 (testing) verifies all functionality

---

## 🎯 Success Criteria

### Minimum Viable Product (MVP):
- [ ] All three roles can log in
- [ ] Admin can create users and assign tests
- [ ] Teacher can upload questions (Word/PPT) and view results
- [ ] Student can take test with timer and see results
- [ ] All data encrypted (AES-256)
- [ ] One question per page, no back navigation
- [ ] Excel export working

### Bonus Features (If time permits):
- [ ] Email notifications
- [ ] Password reset
- [ ] Test scheduling
- [ ] Multiple test attempts
- [ ] Analytics dashboard

---

## 🚨 Risk Mitigation

### Potential Blockers:

1. **Part 1 delays → Everything blocked**
   - Mitigation: Start immediately, simplify if needed

2. **Word/PPT parsing complexity (Part 3)**
   - Mitigation: Test libraries early, have fallback (manual JSON upload)

3. **Timer + Navigation blocking (Part 4)**
   - Mitigation: Test in multiple browsers early

4. **Integration issues**
   - Mitigation: Define APIs early, mock data for parallel development

---

## 📞 Support & Resources

### Libraries to Use:
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **python-docx**: Word parsing
- **python-pptx**: PowerPoint parsing
- **openpyxl**: Excel generation
- **cryptography**: AES-256 encryption
- **Flask-Login**: User session management
- **pytest**: Testing

### External Help:
- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy Docs: https://docs.sqlalchemy.org/
- Encryption Guide: https://cryptography.io/

---

## 📊 Progress Tracking

Create a shared spreadsheet/board with:
- [ ] Task completion status
- [ ] Current blockers
- [ ] Integration dependencies
- [ ] Test coverage percentage
- [ ] Documentation completion

---

## 🏆 Final Notes

- **Communicate early and often**
- **Test your own code before integration**
- **Document your APIs for other team members**
- **Follow the existing code style**
- **Ask for help when stuck**
- **Commit code frequently with clear messages**

Good luck! 🚀
