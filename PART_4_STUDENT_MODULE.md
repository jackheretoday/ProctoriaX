# PART 4: Student Module
**Team Member**: 4  
**Complexity**: High (Timer + Navigation Control)  
**Priority**: Critical  
**Dependencies**: Part 1 (Core) + Part 3 (Teacher - for questions)  
**Estimated Time**: 7-8 days

---

## 🎯 Your Responsibilities
- Student dashboard (view assigned tests for today)
- Test instructions page (show Terms & Conditions)
- Test-taking interface (ONE question per page, no going back)
- Running timer (cannot be stopped)
- Disable browser back button and navigation
- Auto-submit when timer expires
- Immediate results display after submission
- Answer review page

---

## 📁 Your Files (14 files)

### Backend - API & Services (2 files)
```
✓ app/api/v1/student.py
✓ app/services/test_service.py (shared with Part 3)
```

### Frontend - Templates (6 files)
```
✓ app/templates/student/base_student.html
✓ app/templates/student/dashboard.html
✓ app/templates/student/test_instructions.html
✓ app/templates/student/take_test.html
✓ app/templates/student/test_result.html
✓ app/templates/student/review_answers.html
```

### JavaScript (5 files) ⭐ CRITICAL
```
✓ app/static/js/test-timer.js
✓ app/static/js/disable-back.js
✓ app/static/js/prevent-navigation.js
✓ app/static/js/auto-submit.js
✓ app/static/js/form-validator.js
```

### Styling (1 file)
```
✓ app/static/css/student.css
```

---

## ✅ Task Checklist

### Phase 1: Student API Endpoints (Day 1-2)
**File: `app/api/v1/student.py`**

- [ ] **`GET /api/v1/student/dashboard`**:
  - Get logged-in student's ID
  - Fetch today's assigned tests
  - For each test: name, subject, duration, status (pending/completed)
  - Requires `@role_required('student')`
  - Return JSON

- [ ] **`GET /api/v1/student/tests`**:
  - Get all tests assigned to student
  - Include past and future tests
  - Return list

- [ ] **`GET /api/v1/student/tests/<test_id>/instructions`**:
  - Get test details (name, subject, duration, question count)
  - Get Terms & Conditions (decrypted)
  - Return test info + terms

- [ ] **`POST /api/v1/student/tests/<test_id>/start`**:
  - Mark test as started
  - Record start time
  - Create session for test
  - Return: {session_id, start_time, end_time, questions_count}

- [ ] **`GET /api/v1/student/tests/<test_id>/question/<question_number>`**:
  - Get specific question (decrypted)
  - Return question text, options (A, B, C, D)
  - Do NOT return correct answer
  - Do NOT return explanation

- [ ] **`POST /api/v1/student/tests/<test_id>/answer`**:
  - Submit answer for a question
  - Body: {question_id, selected_answer, time_spent}
  - Store answer in session or database
  - Return: {success: true}

- [ ] **`POST /api/v1/student/tests/<test_id>/submit`**:
  - Submit entire test
  - Calculate score: compare submitted answers with correct answers
  - Create Result record
  - Return: {score, total_questions, percentage, correct_answers}

- [ ] **`GET /api/v1/student/tests/<test_id>/result`**:
  - Get result for completed test
  - Return: student name, score, total, percentage

- [ ] **`GET /api/v1/student/tests/<test_id>/review`**:
  - Get all questions with correct answers and explanations
  - Only available AFTER test submission
  - Return questions with: question, your_answer, correct_answer, explanation

### Phase 2: Test Service Extensions (Day 2)
**File: `app/services/test_service.py`** (coordinate with Member 3)

- [ ] **`get_assigned_tests_for_student(student_id, date=None)`**:
  - Fetch tests assigned to student
  - If date provided: filter by assignment date
  - Return list of tests

- [ ] **`start_test_session(student_id, test_id)`**:
  - Create test session
  - Record start time
  - Calculate end time (start + duration)
  - Return session object

- [ ] **`get_question_by_number(test_id, question_number, decrypt=True)`**:
  - Fetch specific question
  - Decrypt if needed
  - Return question (without answer)

- [ ] **`save_answer(session_id, question_id, selected_answer)`**:
  - Store answer temporarily (session or database)
  - Track answer submission

- [ ] **`calculate_test_result(student_id, test_id, submitted_answers)`**:
  - Compare submitted answers with correct answers
  - Count correct answers
  - Calculate percentage
  - Create Result record
  - Return result object

- [ ] **`get_test_review(student_id, test_id)`**:
  - Get all questions with answers and explanations
  - Get student's submitted answers
  - Return complete review data

### Phase 3: Frontend - Base Template (Day 3)
**File: `app/templates/student/base_student.html`**

- [ ] Extend from `base.html`
- [ ] Simple navigation:
  - Dashboard
  - My Tests
  - Logout
- [ ] Show student name in header
- [ ] Show organization name prominently
- [ ] Minimal distractions (clean UI)
- [ ] Responsive design

### Phase 4: Dashboard (Day 3)
**File: `app/templates/student/dashboard.html`**

- [ ] Welcome message: "Welcome, [Student Name]"
- [ ] Today's date display
- [ ] **Today's Assigned Tests** section:
  - Card for each test assigned today
  - Show: Test name, Subject, Duration, Questions count
  - "Start Test" button (if not completed)
  - "View Results" button (if completed)
  - "Not Available Yet" if not scheduled for today
- [ ] **Upcoming Tests** section:
  - Show future assigned tests with dates
- [ ] **Past Tests** section:
  - Show completed tests with scores

### Phase 5: Test Instructions (Day 3-4)
**File: `app/templates/student/test_instructions.html`**

- [ ] Header: Organization name, Test name
- [ ] Test details card:
  - Test Name
  - Subject
  - Total Questions
  - Duration (in minutes)
- [ ] **Terms & Conditions section** (REQUIRED):
  - Title: "Terms & Conditions"
  - Display all terms (max 10 bullets)
  - Large, readable font
- [ ] **Important Instructions**:
  - "You cannot go back to previous questions"
  - "Each answer is final"
  - "Timer will be running and cannot be stopped"
  - "Test will auto-submit when time expires"
  - "Results will be shown immediately after submission"
- [ ] Checkbox: "I agree to the Terms & Conditions"
- [ ] "Start Test" button (disabled until checkbox checked)

### Phase 6: Take Test Interface (Day 4-5) ⭐ MOST CRITICAL
**File: `app/templates/student/take_test.html`**

#### Header Section:
- [ ] Organization name (left)
- [ ] Test name (center)
- [ ] **Running timer** (right, large, prominent):
  - Format: MM:SS or HH:MM:SS
  - Red color when < 5 minutes left
  - Update every second
  - No pause button

#### Question Info:
- [ ] Current question number: "Question 5 of 50"
- [ ] Progress bar (optional): Visual indicator

#### Question Display:
- [ ] **ONE question per page**
- [ ] Large, readable font
- [ ] Question text
- [ ] Four options (A, B, C, D):
  - Radio buttons (only one selectable)
  - Clear labels
  - Large clickable area

#### Navigation:
- [ ] "Submit Answer" button (bottom)
- [ ] **NO "Previous" button**
- [ ] **NO "Next" button without submitting**
- [ ] Confirmation: "Are you sure? You cannot change this answer."

#### End of Test:
- [ ] After last question: "Submit Test" button
- [ ] Confirmation modal: "Submit test? You cannot change answers."
- [ ] Auto-submit when timer reaches 0:00

### Phase 7: JavaScript - Timer (Day 5) ⭐ CRITICAL
**File: `app/static/js/test-timer.js`**

```javascript
// Required functionality:
- [ ] Initialize timer with test duration (e.g., 60 minutes)
- [ ] Start countdown on page load
- [ ] Update display every second
- [ ] Store remaining time in localStorage (persist on page change)
- [ ] Change color to red when < 5 minutes
- [ ] Show warning when < 1 minute
- [ ] When timer reaches 0:
  - Auto-submit test
  - Disable all inputs
  - Show "Time's up!" message
  - Redirect to results page
- [ ] Prevent timer manipulation (validate server-side too)
```

### Phase 8: JavaScript - Disable Navigation (Day 5-6) ⭐ CRITICAL
**File: `app/static/js/disable-back.js`**

```javascript
// Disable browser back button:
- [ ] Use history.pushState() to prevent back navigation
- [ ] Show confirmation if user tries to leave page
- [ ] window.onbeforeunload = "Test in progress. Leave?"
```

**File: `app/static/js/prevent-navigation.js`**

```javascript
// Disable all navigation during test:
- [ ] Disable browser back/forward buttons
- [ ] Disable F5 (refresh)
- [ ] Disable Ctrl+R (refresh)
- [ ] Disable right-click context menu
- [ ] Disable keyboard shortcuts (Ctrl+W, Alt+F4)
- [ ] Show warning on any navigation attempt
- [ ] Use window.history.pushState() repeatedly
```

**File: `app/static/js/auto-submit.js`**

```javascript
// Auto-submit test:
- [ ] Listen to timer reaching 0
- [ ] Collect all submitted answers
- [ ] Call submit API endpoint
- [ ] Show "Submitting..." loader
- [ ] Redirect to results page
- [ ] Handle errors gracefully
```

### Phase 9: Results Display (Day 6-7)
**File: `app/templates/student/test_result.html`**

- [ ] **Immediate Results** (show right after submission)
- [ ] Header: "Test Results"
- [ ] Results card (large, centered):
  - Student Name
  - Student ID (if applicable)
  - Test Name
  - Total Questions
  - Correct Answers
  - Percentage Score (large font, colored)
    - Green if ≥ 80%
    - Orange if 50-79%
    - Red if < 50%
  - Time Taken
- [ ] Message: "Congratulations!" or "Keep practicing!"
- [ ] **Two buttons**:
  - "Review Answers" → go to review_answers.html
  - "Close" or "Back to Dashboard" → dismiss page
- [ ] **IMPORTANT**: After dismissing, results should NOT be shown again (requirement)

### Phase 10: Answer Review (Day 7)
**File: `app/templates/student/review_answers.html`**

- [ ] Header: "Answer Review - [Test Name]"
- [ ] Summary card: Score, Total, Percentage
- [ ] **For each question**:
  - Question number
  - Question text
  - All options (A, B, C, D)
  - Your answer (highlighted in blue or red)
  - Correct answer (highlighted in green)
  - ✓ or ✗ icon
  - Explanation text
- [ ] Filter options:
  - Show All
  - Show Correct Only
  - Show Incorrect Only
- [ ] "Back to Dashboard" button

### Phase 11: Styling (Day 7-8)
**File: `app/static/css/student.css`**

#### Dashboard:
- [ ] Clean, card-based layout
- [ ] Test cards with hover effects
- [ ] Status badges (Pending, Completed)

#### Test Instructions:
- [ ] Large, readable text
- [ ] Terms & Conditions in bordered box
- [ ] Prominent checkbox and button

#### Take Test:
- [ ] **Timer**: Large, top-right, bold, colored
- [ ] Question: Large font, centered
- [ ] Options: Large clickable areas, radio buttons
- [ ] Minimal distractions (white background, simple design)
- [ ] Focus on readability

#### Results:
- [ ] Large centered card
- [ ] Colored percentage (green/orange/red)
- [ ] Icons (✓ for pass, ✗ for fail)

#### Review:
- [ ] Question cards with borders
- [ ] Color-coding:
  - Green for correct
  - Red for incorrect
  - Blue for your answer
- [ ] Clear typography

#### Responsive:
- [ ] Mobile-friendly (students may use phones)
- [ ] Readable on tablets

### Phase 12: Form Validation (Day 8)
**File: `app/static/js/form-validator.js`**

- [ ] Validate an option is selected before submit
- [ ] Show error if no option selected: "Please select an answer"
- [ ] Confirm before submitting answer: "Submit this answer?"
- [ ] Confirm before submitting test: "Submit test? Final submission."

### Phase 13: Testing (Day 8-9) ⭐ CRITICAL
- [ ] Test timer starts correctly
- [ ] Test timer counts down accurately
- [ ] Test timer auto-submits at 0:00
- [ ] Test timer persists across questions (doesn't reset)
- [ ] Test back button is disabled
- [ ] Test refresh page shows warning
- [ ] Test closing browser shows warning
- [ ] Test questions display correctly (decrypted)
- [ ] Test answer submission works
- [ ] Test cannot go back to previous question
- [ ] Test immediate results display correctly
- [ ] Test percentage calculation is accurate
- [ ] Test answer review shows correct/incorrect clearly
- [ ] Test on Chrome, Firefox, Edge
- [ ] Test on mobile devices
- [ ] Test on slow internet (timer should still work)

### Phase 14: Edge Cases (Day 9)
- [ ] Handle internet disconnection during test:
  - Save answers locally
  - Sync when connection restored
- [ ] Handle page refresh (accidental):
  - Show warning
  - Resume test at same question
  - Timer continues from where it was
- [ ] Handle browser crash:
  - Recover session on re-login
- [ ] Handle test already completed:
  - Redirect to results, not test page
- [ ] Handle test not yet available:
  - Show "Test not available yet" message

---

## 🔐 Security Checklist

- [ ] All student routes protected with `@role_required('student')`
- [ ] Students can only access their own tests
- [ ] Cannot access other students' results
- [ ] Server-side timer validation (don't trust client timer alone)
- [ ] Verify test session is valid before accepting answers
- [ ] Prevent answer tampering (validate on server)
- [ ] Log suspicious activities (multiple tabs, timer manipulation)
- [ ] CSRF protection on all forms
- [ ] Rate limit answer submissions
- [ ] Audit log test starts and submissions

---

## 📤 What You Need from Part 1

✅ **Before you start**:
- [ ] Assignment model (to get assigned tests)
- [ ] Result model (to save results)
- [ ] encryption_service (to decrypt questions)
- [ ] Role-based decorator: `@role_required('student')`
- [ ] Student user created for testing

---

## 📤 What You Need from Part 3

✅ **Before you start**:
- [ ] Questions uploaded and encrypted
- [ ] Terms & Conditions uploaded
- [ ] Test structure (duration, name, subject)
- [ ] Question decryption working

---

## 📥 What Other Parts Need from You

### For Teacher Module (Member 3):
- Result submission format (they need to display results)

### For Testing (Member 5):
- Test session flow
- Answer submission API

---

## 🎯 Critical Requirements (From Professor)

✅ **Must implement**:
- [x] Running clock with NO provision to stop ⏱️
- [x] Provision to submit test at any point ✓
- [x] Only ONE question per page 📄
- [x] NO provision to go back (disable back button) 🚫
- [x] Every submission is final for each question ✓
- [x] Interface shows: org name, test name, total questions, current question number, running clock
- [x] Immediate results after submission 📊
- [x] Results dismissed by button and never shown again ❌
- [x] Student can review answers after test ✓

---

## 🆘 Common Issues & Solutions

**Issue**: Timer resets when moving to next question  
**Solution**: Store timer in localStorage, restore on each page load

**Issue**: Back button still works  
**Solution**: Use history.pushState() repeatedly, add window.onpopstate handler

**Issue**: Student refreshes page, timer resets  
**Solution**: Store start_time on server, calculate remaining time on each request

**Issue**: Auto-submit not working  
**Solution**: Check timer listener, ensure submit function is called

**Issue**: Results not displaying percentage correctly  
**Solution**: Verify calculation: (correct / total) * 100

**Issue**: Cannot decrypt questions  
**Solution**: Coordinate with Member 1 and Member 3 for encryption API

**Issue**: Timer continues after test submitted  
**Solution**: Clear timer interval on submit, disable all interactions

---

## 📞 Communication

**Coordinate with**:
- **Member 1**: Get authentication, encryption working
- **Member 3**: Get questions, terms, test structure
- **Member 2**: Understand assignment structure
- **Member 5**: Provide test flow for integration testing

**Daily Updates**:
- Timer working
- Navigation disabled
- Test submission working
- Any blockers

---

## 🧪 Test Scenario Walkthrough

### Happy Path:
1. Student logs in
2. Sees dashboard with today's test
3. Clicks "Start Test"
4. Reads Terms & Conditions
5. Checks "I agree", clicks "Start Test"
6. Test page loads, timer starts at 60:00
7. Reads Question 1, selects option B, clicks "Submit Answer"
8. Confirmation: "Are you sure?" → Clicks "Yes"
9. Question 2 loads, timer now at 59:45
10. Continues answering all 50 questions
11. After Question 50, clicks "Submit Test"
12. Results page: "You scored 45/50 (90%)"
13. Clicks "Review Answers"
14. Sees all questions with correct/incorrect marking
15. Clicks "Back to Dashboard"
16. Dashboard shows test as "Completed"

### Edge Case: Timer Expires
1. Student on Question 30
2. Timer reaches 0:00
3. Alert: "Time's up!"
4. Test auto-submits with 30 answered questions
5. Results: "You scored 25/30 (83%). 20 questions unanswered."
6. Can still review answered questions

---

## 🏆 Success Criteria

At the end of your part, student should be able to:
- [ ] Log in as student
- [ ] See dashboard with today's assigned tests
- [ ] View test instructions and Terms & Conditions
- [ ] Start test and see timer running
- [ ] Answer questions one by one
- [ ] Cannot go back to previous questions
- [ ] Submit answers successfully
- [ ] See timer counting down accurately
- [ ] Auto-submit when timer expires
- [ ] See immediate results after submission
- [ ] View results with name, total, correct, percentage
- [ ] Review all answers with correct answers and explanations
- [ ] Close results and not see them again
- [ ] Back button is disabled during test
- [ ] Cannot refresh or leave page during test
- [ ] UI is clean, focused, and distraction-free

**Good luck! You're building the test-taking experience! 📝✨**
