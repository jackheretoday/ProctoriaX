# PART 2: Admin Module
**Team Member**: 2  
**Complexity**: Medium  
**Priority**: High  
**Dependencies**: Part 1 (Core Infrastructure must be complete)  
**Estimated Time**: 5-7 days

---

## 🎯 Your Responsibilities
- Admin dashboard and interface
- User provisioning (create users, teachers, other admins)
- Test assignment to students
- Test date management
- System logs viewing

---

## 📁 Your Files (15 files)

### Backend - API (2 files)
```
✓ app/api/v1/admin.py
✓ app/services/user_service.py
```

### Frontend - Templates (7 files)
```
✓ app/templates/admin/base_admin.html
✓ app/templates/admin/dashboard.html
✓ app/templates/admin/manage_users.html
✓ app/templates/admin/create_user.html
✓ app/templates/admin/assign_tests.html
✓ app/templates/admin/manage_test_dates.html
✓ app/templates/admin/system_logs.html
```

### Styling (1 file)
```
✓ app/static/css/admin.css
```

### JavaScript (Optional - 2 files)
```
✓ app/static/js/admin-dashboard.js (if needed)
✓ app/static/js/user-management.js (if needed)
```

---

## ✅ Task Checklist

### Phase 1: User Service (Day 1-2)
**File: `app/services/user_service.py`**

- [ ] **`create_user(username, email, password, role)`**:
  - Validate username is unique
  - Validate email format
  - Hash password using auth_service
  - Create User record in database
  - Return user object or error
  
- [ ] **`get_all_users(role=None)`**:
  - Fetch all users from database
  - Optional filter by role (admin/teacher/student)
  - Return list of users
  
- [ ] **`get_user_by_id(user_id)`**:
  - Fetch single user
  - Return user object or None
  
- [ ] **`update_user(user_id, **kwargs)`**:
  - Update user details (email, role, is_active)
  - Validate changes
  - Return updated user
  
- [ ] **`delete_user(user_id)`**:
  - Soft delete (set is_active=False)
  - Or hard delete from database
  - Cannot delete self
  
- [ ] **`reset_user_password(user_id)`**:
  - Generate random password
  - Hash and update
  - Return new password (to be shown to admin)
  
- [ ] **`get_user_statistics()`**:
  - Count total users by role
  - Return dict with stats

### Phase 2: Admin API Endpoints (Day 2-3)
**File: `app/api/v1/admin.py`**

- [ ] **`GET /api/v1/admin/dashboard`**:
  - Return statistics: total users, tests, recent activity
  - Requires `@role_required('admin')`
  
- [ ] **`GET /api/v1/admin/users`**:
  - List all users (with pagination)
  - Query params: ?role=student&page=1&per_page=20
  - Return JSON list
  
- [ ] **`POST /api/v1/admin/users`**:
  - Create new user (admin/teacher/student)
  - Body: {username, email, password, role}
  - Return created user and status 201
  
- [ ] **`GET /api/v1/admin/users/<user_id>`**:
  - Get single user details
  - Return user JSON
  
- [ ] **`PUT /api/v1/admin/users/<user_id>`**:
  - Update user details
  - Body: {email, role, is_active}
  - Return updated user
  
- [ ] **`DELETE /api/v1/admin/users/<user_id>`**:
  - Delete user
  - Return success message
  
- [ ] **`POST /api/v1/admin/users/<user_id>/reset-password`**:
  - Reset user password
  - Return new password (show once)
  
- [ ] **`GET /api/v1/admin/tests`**:
  - List all tests created by teachers
  - Return test list
  
- [ ] **`POST /api/v1/admin/assignments`**:
  - Assign test to student(s)
  - Body: {test_id, student_ids: [], assigned_date}
  - Return assignment details
  
- [ ] **`GET /api/v1/admin/assignments`**:
  - List all test assignments
  - Query params: ?test_id=1 or ?student_id=5
  - Return assignments list
  
- [ ] **`PUT /api/v1/admin/assignments/<assignment_id>`**:
  - Update assignment date
  - Body: {assigned_date}
  
- [ ] **`GET /api/v1/admin/audit-logs`**:
  - Fetch audit logs (with pagination)
  - Query params: ?user_id=1&action=login&page=1
  - Return logs

### Phase 3: Frontend Templates - Base (Day 3)
**File: `app/templates/admin/base_admin.html`**

- [ ] Extend from `base.html`
- [ ] Sidebar navigation:
  - Dashboard
  - Manage Users
  - Assign Tests
  - System Logs
  - Logout
- [ ] Show admin name in header
- [ ] Responsive design (Bootstrap)

### Phase 4: Dashboard (Day 3-4)
**File: `app/templates/admin/dashboard.html`**

- [ ] Statistics cards:
  - Total Students
  - Total Teachers
  - Total Tests
  - Active Assignments
- [ ] Recent activity table (last 10 actions from audit log)
- [ ] Quick actions:
  - Create User button → links to create_user.html
  - Assign Test button → links to assign_tests.html
- [ ] Charts (optional): Users by role (pie chart)

### Phase 5: User Management (Day 4-5)
**File: `app/templates/admin/manage_users.html`**

- [ ] Filter dropdown: All | Admins | Teachers | Students
- [ ] Search bar: Search by username or email
- [ ] Users table with columns:
  - ID
  - Username
  - Email
  - Role
  - Status (Active/Inactive)
  - Actions (Edit, Delete, Reset Password)
- [ ] Pagination (20 users per page)
- [ ] Delete confirmation modal
- [ ] Show success/error messages

**File: `app/templates/admin/create_user.html`**

- [ ] Form fields:
  - Username (required, unique)
  - Email (required, valid email)
  - Password (required, min 8 chars)
  - Confirm Password
  - Role dropdown (Admin/Teacher/Student)
- [ ] Client-side validation
- [ ] Submit button
- [ ] Cancel button → back to manage_users
- [ ] Show validation errors

### Phase 6: Test Assignment (Day 5-6)
**File: `app/templates/admin/assign_tests.html`**

- [ ] Step 1: Select Test
  - Dropdown: List all available tests (fetched from API)
  - Show test details: name, subject, duration, questions count
- [ ] Step 2: Select Students
  - Multi-select list or checkboxes
  - "Select All" option
  - Search/filter students
- [ ] Step 3: Set Date
  - Date picker for test date
  - Validation: cannot be in the past
- [ ] Review section: Show selected test + students + date
- [ ] Assign button
- [ ] Show success message with assignment details

**File: `app/templates/admin/manage_test_dates.html`**

- [ ] Table of all assignments:
  - Test Name
  - Student Name
  - Assigned Date
  - Status (Pending/Completed)
  - Actions (Edit Date, Remove Assignment)
- [ ] Filter by test or student
- [ ] Edit date modal: Update assigned_date
- [ ] Show success/error messages

### Phase 7: System Logs (Day 6)
**File: `app/templates/admin/system_logs.html`**

- [ ] Filters:
  - User dropdown (filter by user)
  - Action dropdown (login, logout, create, update, delete, access)
  - Date range picker (from - to)
- [ ] Logs table:
  - Timestamp
  - User
  - Action
  - Details
  - IP Address
- [ ] Pagination (50 logs per page)
- [ ] Export logs button (optional - CSV download)
- [ ] Real-time update (optional - WebSocket)

### Phase 8: Styling (Day 7)
**File: `app/static/css/admin.css`**

- [ ] Sidebar styling:
  - Fixed left sidebar
  - Active menu item highlight
  - Hover effects
- [ ] Dashboard cards:
  - Gradient backgrounds
  - Icons for each stat
  - Shadow effects
- [ ] Tables:
  - Striped rows
  - Hover effect on rows
  - Action buttons styling
- [ ] Forms:
  - Input field styling
  - Button colors (primary, danger)
  - Validation error styling
- [ ] Modals:
  - Confirmation dialogs
  - Form modals
- [ ] Responsive design:
  - Mobile-friendly sidebar (collapsible)
  - Responsive tables (horizontal scroll on mobile)

### Phase 9: JavaScript (Optional - Day 7)

**Admin Dashboard JS:**
- [ ] Fetch dashboard stats via AJAX
- [ ] Update stats without page reload
- [ ] Charts rendering (Chart.js)

**User Management JS:**
- [ ] Delete confirmation dialog
- [ ] Reset password confirmation
- [ ] Live search in users table
- [ ] Form validation before submit
- [ ] AJAX user creation (no page reload)

**Test Assignment JS:**
- [ ] Multi-select students with "Select All"
- [ ] Date picker initialization
- [ ] Form validation
- [ ] AJAX submission

### Phase 10: Testing (Day 7)
- [ ] Test user creation (all roles)
- [ ] Test user update
- [ ] Test user deletion
- [ ] Test password reset
- [ ] Test test assignment to single student
- [ ] Test test assignment to multiple students
- [ ] Test date validation (cannot assign past date)
- [ ] Test audit logs display
- [ ] Test filters and search
- [ ] Test pagination
- [ ] Test responsive design on mobile

---

## 🔐 Security Checklist

- [ ] All admin routes protected with `@role_required('admin')`
- [ ] Cannot delete own admin account
- [ ] Cannot downgrade own role
- [ ] Password validation enforced
- [ ] Email validation enforced
- [ ] SQL injection prevention (use SQLAlchemy ORM)
- [ ] XSS prevention (escape all user input in templates)
- [ ] CSRF tokens on all forms
- [ ] Audit log all admin actions

---

## 📤 What You Need from Part 1 (Core Infrastructure)

✅ **Before you start**:
- [ ] User model with role field working
- [ ] Assignment model created
- [ ] Test model created
- [ ] AuditLog model created
- [ ] Role-based authorization decorator: `@role_required('admin')`
- [ ] Database initialized with tables
- [ ] Admin user created (to log in and test)
- [ ] Authentication working

---

## 📥 What Other Parts Need from You

### For Teacher Module (Member 3):
- User creation API (they may need to check if users exist)

### For Student Module (Member 4):
- Assignment data (students need to see assigned tests)

### For Testing (Member 5):
- All API endpoints documented
- Sample users created for testing

---

## 🎨 UI/UX Guidelines

**Admin Panel Should Look**:
- Professional and clean
- Easy to navigate
- Clear call-to-action buttons
- Confirmation for destructive actions (delete)
- Helpful error messages
- Success feedback for actions

**Color Scheme Suggestion**:
- Primary: Blue (#007bff)
- Success: Green (#28a745)
- Danger: Red (#dc3545)
- Background: Light gray (#f8f9fa)
- Sidebar: Dark (#343a40)

**Fonts**:
- Headers: Bold, sans-serif
- Body: Regular, sans-serif (Roboto, Open Sans)

---

## 🧪 Sample Data You Need

Create these test users for development:

```python
# In scripts/seed_data.py (ask Member 1 or create yourself)
admin_user = User(username='admin', email='admin@test.com', role='admin')
teacher1 = User(username='teacher1', email='teacher1@test.com', role='teacher')
student1 = User(username='student1', email='student1@test.com', role='student')
student2 = User(username='student2', email='student2@test.com', role='student')
```

---

## 📋 Admin Workflows to Support

### Workflow 1: Onboarding New Teacher
1. Admin logs in
2. Goes to "Manage Users"
3. Clicks "Create User"
4. Fills form: username, email, password, role=teacher
5. Submits
6. Teacher account created
7. Admin shares credentials with teacher

### Workflow 2: Assigning Test to Students
1. Admin logs in
2. Goes to "Assign Tests"
3. Selects test from dropdown
4. Selects multiple students (checkboxes)
5. Sets test date
6. Clicks "Assign"
7. Assignments created
8. Students see test on their dashboard on the assigned date

### Workflow 3: Managing Users
1. Admin views all users in table
2. Filters by role (students)
3. Searches for specific student
4. Clicks "Edit" on student row
5. Updates email
6. Saves changes

### Workflow 4: Viewing System Activity
1. Admin goes to "System Logs"
2. Filters by action type (e.g., "login")
3. Filters by date range (last 7 days)
4. Views who logged in when and from which IP
5. Identifies suspicious activity

---

## 🆘 Common Issues & Solutions

**Issue**: Cannot fetch users list  
**Solution**: Check if User model query is correct, verify database has users

**Issue**: Password not hashing  
**Solution**: Use `auth_service.hash_password()` from Part 1

**Issue**: Cannot delete user  
**Solution**: Check foreign key constraints, use soft delete

**Issue**: Assignment not showing up for student  
**Solution**: Verify assignment.assigned_date matches today's date

**Issue**: Audit logs not recording actions  
**Solution**: Ensure `audit_logger` middleware is active

---

## 📞 Communication

**Coordinate with**:
- **Member 1**: Get User model API, auth decorators
- **Member 3**: Share test data structure (test model)
- **Member 4**: Explain assignment data structure
- **Member 5**: Provide API endpoints for testing

**Daily Updates**:
- User management API complete
- Frontend dashboard done
- Test assignment working
- Any blockers

---

## 🏆 Success Criteria

At the end of your part, admin should be able to:
- [ ] Log in as admin
- [ ] See dashboard with statistics
- [ ] Create new users (admin, teacher, student)
- [ ] View all users in a table
- [ ] Edit user details
- [ ] Delete users
- [ ] Reset user passwords
- [ ] Assign tests to students with dates
- [ ] View all assignments
- [ ] Modify assignment dates
- [ ] View system audit logs
- [ ] Filter and search logs
- [ ] UI is responsive and professional

**Good luck! You're building the control center! 🎛️**
