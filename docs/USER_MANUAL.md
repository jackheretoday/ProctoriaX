# User Manual - Testing Platform

## Table of Contents
1. [Getting Started](#getting-started)
2. [Admin Guide](#admin-guide)
3. [Teacher Guide](#teacher-guide)
4. [Student Guide](#student-guide)
5. [FAQ](#faq)

---

## Getting Started

### System Requirements
- **Browser**: Chrome 90+, Firefox 88+, Edge 90+
- **Internet**: Stable connection (minimum 2 Mbps)
- **Screen Resolution**: 1024x768 minimum

### Login
1. Navigate to the platform URL
2. Enter your username and password
3. Click "Login"
4. You'll be redirected to your role-specific dashboard

---

## Admin Guide

### Dashboard Overview
- Total users count
- Active tests statistics
- Recent user registrations
- System health indicators

### User Management

#### Creating Users
1. Click **"User Management"** in sidebar
2. Click **"Add New User"** button
3. Fill in the form:
   - Username (unique)
   - Email (unique)
   - Password (min 8 characters)
   - Full Name
   - Role (Admin/Teacher/Student)
   - Roll Number (for students only)
4. Click **"Create User"**

#### Bulk Import
1. Click **"Bulk Import"** button
2. Download CSV template
3. Fill template with user data
4. Upload filled CSV
5. Review and confirm import

#### Editing Users
1. Find user in list
2. Click **"Edit"** button
3. Modify fields
4. Click **"Save Changes"**

#### Deleting Users
1. Find user in list
2. Click **"Delete"** button
3. Confirm deletion
4. **Warning**: This action cannot be undone

### System Configuration
- **Organization Name**: Set in Settings
- **Session Timeout**: Default 30 minutes
- **File Upload Limits**: 10MB maximum

---

## Teacher Guide

### Dashboard
- My Tests: All tests you've created
- Recent Results: Latest student submissions
- Quick Actions: Create test, view reports

### Creating a Test

#### Step 1: Basic Information
1. Click **"Create New Test"**
2. Enter:
   - Test Name (e.g., "Python Midterm")
   - Subject (e.g., "Computer Science")
   - Duration in minutes (e.g., 60)
   - Description (optional)
3. Click **"Create"**

#### Step 2: Upload Questions

**From Word Document (.docx)**:
1. Click **"Upload Questions"** → **"From Word"**
2. Select your .docx file
3. **Format Requirements**:
   ```
   Q1) What is Python?
   A) A snake
   B) A programming language
   C) A database
   D) An OS
   Correct Answer: B
   Explanation: Python is a high-level programming language.

   Q2) [Next question...]
   ```
4. Click **"Upload"**
5. System parses and validates questions
6. Review imported questions
7. Click **"Confirm"**

**From PowerPoint (.pptx)**:
1. Click **"Upload Questions"** → **"From PowerPoint"**
2. Select your .pptx file
3. **Format**: One question per slide
4. Upload and review

**Manual Entry**:
1. Click **"Add Question Manually"**
2. Fill in:
   - Question Number
   - Question Text
   - Options A, B, C, D
   - Correct Answer
   - Explanation (optional)
3. Click **"Save"**
4. Repeat for all questions

#### Step 3: Terms & Conditions
1. Click **"Terms & Conditions"** tab
2. Upload .docx/.pptx file OR enter manually
3. Maximum 10 bullet points
4. Click **"Save"**

#### Step 4: Publish Test
1. Review all questions
2. Review terms & conditions
3. Click **"Publish Test"**
4. **Note**: Cannot edit after publishing

### Assigning Tests to Students

#### Individual Assignment
1. Open published test
2. Click **"Assign Students"**
3. Select students from list
4. Choose assignment date
5. Click **"Assign"**

#### Bulk Assignment
1. Click **"Bulk Assign"**
2. Select test
3. Choose class/group
4. Select date
5. Click **"Assign All"**

### Viewing Results

#### Individual Student Results
1. Click **"Results"** tab
2. Select test
3. View list of students who completed
4. Click student name to see details:
   - Score and percentage
   - Correct/Wrong/Unattempted
   - Time taken
   - Individual answers

#### Class Analytics
- **Average Score**: Class performance
- **Highest Score**: Top performer
- **Lowest Score**: Needs attention
- **Distribution Graph**: Score distribution

#### Exporting Results
1. Click **"Export to Excel"**
2. Select test
3. Choose format (Summary / Detailed)
4. Click **"Download"**
5. Encrypted Excel file downloads

**Opening Encrypted Excel**:
- Password will be displayed on screen
- Copy password
- Open Excel file
- Enter password when prompted

---

## Student Guide

### Dashboard
- **Today's Tests**: Tests assigned for today
- **Upcoming Tests**: Future assigned tests
- **Past Tests**: Completed tests with scores

### Taking a Test

#### Step 1: View Test Instructions
1. Click **"Start Test"** on assigned test
2. Read test details:
   - Subject
   - Total questions
   - Duration
3. Read **Terms & Conditions** carefully
4. Read **Important Instructions**:
   - Cannot go back to previous questions
   - Each answer is final
   - Timer cannot be stopped
   - Auto-submit when time expires
   - Immediate results after submission

#### Step 2: Agree to Terms
1. Check **"I agree to Terms & Conditions"**
2. **"Start Test"** button becomes enabled
3. Click **"Start Test"**
4. Confirm: "Ready to start?"

#### Step 3: Answer Questions

**Interface**:
- **Header**: Organization name, Test name, Timer (top-right)
- **Progress**: "Question 5 of 50"
- **Question**: Large, clear text
- **Options**: Four options (A, B, C, D)
- **Submit Button**: Bottom

**Timer**:
- Starts automatically
- **Green**: Normal (>5 minutes remaining)
- **Yellow**: Warning (<5 minutes)
- **Red**: Critical (<1 minute) - pulses
- Alerts at 5 min and 1 min
- **Auto-submits at 0:00**

**Answering**:
1. Read question carefully
2. Select one option (radio button)
3. Click **"Submit Answer"**
4. Confirm: "Are you sure? Cannot change."
5. Next question loads automatically
6. Repeat until all questions answered

**Important**:
- ❌ Cannot go back to previous questions
- ❌ Cannot change submitted answers
- ❌ Browser back button disabled
- ❌ Page refresh shows warning
- ✅ Timer persists across questions
- ✅ Answers saved immediately

#### Step 4: Final Submission
1. After last question
2. Click **"Submit Test"**
3. Final confirmation
4. Test submitted

#### Step 5: View Results
**Immediate Results Display**:
- Total questions
- Correct answers (green)
- Wrong answers (red)
- Unattempted (gray)
- **Percentage Score** (large, color-coded):
  - Green circle: ≥80% (Excellent!)
  - Orange circle: 50-79% (Good)
  - Red circle: <50% (Keep trying)
- Time taken
- Encouraging message

**Actions**:
- **"Review Answers"**: See all questions with explanations
- **"Back to Dashboard"**: Return to dashboard

### Reviewing Answers
1. Click **"Review Answers"**
2. See all questions with:
   - Your answer (blue highlight)
   - Correct answer (green highlight)
   - ✓ or ✗ icon
   - Explanation
3. **Filter Options**:
   - Show All
   - Correct Only
   - Incorrect Only
4. Learn from mistakes

### Viewing Past Results
1. Go to Dashboard
2. Scroll to **"Past Tests"**
3. Click test name
4. View result summary
5. Click **"Review Answers"** to see details

---

## FAQ

### General

**Q: I forgot my password. How do I reset it?**  
A: Contact your administrator to reset your password.

**Q: Can I change my username?**  
A: No, usernames are permanent. Contact admin if needed.

**Q: What browsers are supported?**  
A: Chrome 90+, Firefox 88+, Edge 90+, Safari 14+

### For Students

**Q: Can I pause the test?**  
A: No, the timer runs continuously and cannot be paused.

**Q: What if I accidentally refresh the page?**  
A: You'll see a warning. If you proceed, the test continues from the same question with timer still running.

**Q: Can I go back to previous questions?**  
A: No, each answer is final. This prevents cheating.

**Q: What if my internet disconnects?**  
A: Reconnect quickly. Timer continues server-side. You may lose unanswered questions if time expires.

**Q: Can I review questions before submitting?**  
A: No, each question is submitted individually and cannot be changed.

**Q: When will I see my results?**  
A: Immediately after submitting the test.

**Q: Can I retake a test?**  
A: No, tests can only be taken once. Contact your teacher if there was a technical issue.

### For Teachers

**Q: Can I edit a published test?**  
A: No, published tests are locked. Create a new version instead.

**Q: How many questions can I upload?**  
A: No hard limit, but recommended maximum is 100 questions per test.

**Q: What file formats are supported for questions?**  
A: Word (.docx) and PowerPoint (.pptx) only.

**Q: Can students see correct answers during the test?**  
A: No, answers are encrypted and only shown after test submission.

**Q: How do I unassign a test from a student?**  
A: Go to test → Assignments → Click "Remove" next to student.

**Q: Can I extend time for a specific student?**  
A: Not currently supported. All students get the same duration.

**Q: How long are results stored?**  
A: Permanently, unless manually deleted by admin.

### For Admins

**Q: How do I backup the database?**  
A: Use the automated backup script or run manually:
```bash
python scripts/backup_db.py
```

**Q: Can I bulk delete users?**  
A: Yes, select multiple users and click "Bulk Delete".

**Q: How do I view system logs?**  
A: Check `logs/` directory for application logs.

**Q: Can I customize the organization name?**  
A: Yes, in Settings → General → Organization Name.

---

## Troubleshooting

### Login Issues
- **"Invalid credentials"**: Check username/password
- **"Account locked"**: Contact admin
- **Session expired**: Login again

### Test Taking Issues
- **Timer shows wrong time**: Refresh page (shows warning)
- **Cannot select option**: Try different browser
- **Submit button disabled**: Select an answer first

### Upload Issues
- **File too large**: Maximum 10MB
- **Invalid format**: Use .docx or .pptx only
- **Parsing error**: Check document format

---

## Keyboard Shortcuts

### Global
- `Ctrl + /`: Show shortcuts help
- `Esc`: Close modal/dialog

### Admin
- `Ctrl + N`: New user
- `Ctrl + F`: Search users

### Teacher
- `Ctrl + N`: New test
- `Ctrl + U`: Upload questions

### Student
- `1-4` or `A-D`: Select option (during test)
- `Enter`: Submit answer

---

## Support

### Getting Help
- **Email**: support@example.com
- **Phone**: +1-XXX-XXX-XXXX
- **Hours**: Mon-Fri, 9AM-5PM

### Reporting Issues
1. Note exact error message
2. Screenshot if possible
3. Note what you were doing
4. Email to support with details

---

**User Manual Version**: 1.0  
**Last Updated**: 2024  
**Feedback**: manual-feedback@example.com
