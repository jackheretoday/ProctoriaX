# PART 3: Teacher Module
**Team Member**: 3  
**Complexity**: High (File parsing + Encryption)  
**Priority**: High  
**Dependencies**: Part 1 (Core Infrastructure must be complete)  
**Estimated Time**: 7-8 days

---

## 🎯 Your Responsibilities
- Upload questions from Word/PowerPoint files
- Parse questions with proper formatting
- Upload Terms & Conditions (max 10 bullets)
- View student results
- Export results to encrypted Excel
- Manage tests

---

## 📁 Your Files (17 files)

### Backend - API & Services (6 files)
```
✓ app/api/v1/teacher.py
✓ app/services/question_service.py
✓ app/services/file_parser_service.py
✓ app/services/excel_service.py
✓ app/services/terms_service.py
✓ app/services/test_service.py
✓ app/services/result_service.py
```

### Frontend - Templates (7 files)
```
✓ app/templates/teacher/base_teacher.html
✓ app/templates/teacher/dashboard.html
✓ app/templates/teacher/upload_questions.html
✓ app/templates/teacher/manage_tests.html
✓ app/templates/teacher/view_results.html
✓ app/templates/teacher/export_results.html
✓ app/templates/teacher/upload_terms.html
```

### Styling (1 file)
```
✓ app/static/css/teacher.css
```

### JavaScript (Optional - 3 files)
```
✓ app/static/js/file-upload.js
✓ app/static/js/question-preview.js
✓ app/static/js/results-table.js
```

---

## ✅ Task Checklist

### Phase 1: File Parser Service (Day 1-3) ⭐ MOST CRITICAL
**File: `app/services/file_parser_service.py`**

#### Word Document Parser
- [ ] **`parse_word_document(file_path)`**:
  - Use `python-docx` library
  - Read .docx file
  - Find questions by pattern: "Question 1", "Question 2", etc.
  - Each question format:
    ```
    Question 1: What is Python?
    A) A snake
    B) A programming language
    C) A game
    D) None of the above
    Answer: B
    Explanation: Python is a programming language.
    ```
  - Parse into structured data:
    ```python
    {
        'question_number': 1,
        'question_text': 'What is Python?',
        'options': {
            'A': 'A snake',
            'B': 'A programming language',
            'C': 'A game',
            'D': 'None of the above'
        },
        'correct_answer': 'B',
        'explanation': 'Python is a programming language.'
    }
    ```
  - Return list of question dictionaries
  - Handle errors: missing questions, malformed format

#### PowerPoint Parser
- [ ] **`parse_powerpoint(file_path)`**:
  - Use `python-pptx` library
  - Read .pptx file
  - **One question per slide**
  - Extract text from each slide
  - Same question format as Word
  - Parse into same structured data
  - Return list of question dictionaries
  - Handle errors: empty slides, no text

#### Terms & Conditions Parser
- [ ] **`parse_terms_conditions(file_path, file_type)`**:
  - Support Word or PowerPoint
  - Extract bullet points
  - **Validate: Maximum 10 bullets**
  - Return list of terms (max 10)
  - Raise error if more than 10 bullets

#### Helper Functions
- [ ] **`validate_question_format(question_dict)`**:
  - Check all required fields present
  - Check options A, B, C, D exist
  - Check correct_answer is one of A, B, C, D
  - Return True/False

- [ ] **`sanitize_question_text(text)`**:
  - Remove extra whitespace
  - Strip special characters that may break encryption
  - Return clean text

### Phase 2: Question Service (Day 3-4)
**File: `app/services/question_service.py`**

- [ ] **`create_question(test_id, question_data)`**:
  - Encrypt question text using encryption_service
  - Encrypt answer using encryption_service
  - Encrypt explanation using encryption_service
  - Save to Question model
  - Return question object

- [ ] **`bulk_create_questions(test_id, questions_list)`**:
  - Loop through questions list
  - Create each question using create_question()
  - Use database transaction (all or nothing)
  - Return count of created questions

- [ ] **`get_questions_for_test(test_id, decrypt=False)`**:
  - Fetch all questions for a test
  - If decrypt=True: decrypt question, answer, explanation
  - Return list of questions

- [ ] **`update_question(question_id, question_data)`**:
  - Update question (re-encrypt if changed)
  - Return updated question

- [ ] **`delete_question(question_id)`**:
  - Delete question from database

- [ ] **`get_question_count(test_id)`**:
  - Return total questions for a test

### Phase 3: Test Service (Day 4)
**File: `app/services/test_service.py`**

- [ ] **`create_test(name, subject, duration, teacher_id)`**:
  - Create Test record
  - Duration in minutes
  - Return test object

- [ ] **`get_tests_by_teacher(teacher_id)`**:
  - Fetch all tests created by teacher
  - Return list of tests

- [ ] **`get_test_by_id(test_id)`**:
  - Fetch single test
  - Include question count
  - Return test object

- [ ] **`update_test(test_id, **kwargs)`**:
  - Update test details
  - Return updated test

- [ ] **`delete_test(test_id)`**:
  - Delete test and all its questions (cascade)
  - Return success

### Phase 4: Terms Service (Day 4)
**File: `app/services/terms_service.py`**

- [ ] **`create_terms(test_id, terms_list)`**:
  - Validate: max 10 bullets
  - Convert list to JSON string
  - Encrypt entire JSON using encryption_service
  - Save to TermsConditions model
  - Return terms object

- [ ] **`get_terms_for_test(test_id, decrypt=True)`**:
  - Fetch terms for test
  - If decrypt=True: decrypt and parse JSON
  - Return list of terms

- [ ] **`update_terms(test_id, terms_list)`**:
  - Validate: max 10 bullets
  - Re-encrypt and update
  - Return updated terms

- [ ] **`delete_terms(test_id)`**:
  - Delete terms for test

### Phase 5: Result Service (Day 5)
**File: `app/services/result_service.py`**

- [ ] **`get_results_for_test(test_id)`**:
  - Fetch all results for a test
  - Include student name, ID
  - Calculate percentage
  - Return list of results with:
    ```python
    {
        'student_name': 'John Doe',
        'student_id': 'STU001',
        'total_questions': 50,
        'correct_answers': 40,
        'percentage': 80.0,
        'completed_at': '2025-10-29 14:30:00'
    }
    ```

- [ ] **`get_result_statistics(test_id)`**:
  - Calculate: Average score, highest score, lowest score
  - Count: Total attempts, pass count, fail count
  - Return statistics dict

### Phase 6: Excel Service (Day 5-6) ⭐ CRITICAL
**File: `app/services/excel_service.py`**

- [ ] **`generate_results_excel(test_id, results_data)`**:
  - Use `openpyxl` library
  - Create new Excel workbook
  - Add worksheet "Results"
  - Headers: Student Name | Student ID | Total Questions | Correct Answers | Percentage
  - Add data rows from results_data
  - Format cells:
    - Bold headers
    - Percentage with % symbol
    - Auto-adjust column widths
  - Save to temporary file
  - **Encrypt Excel file** using encryption_service.encrypt_file()
  - Move encrypted file to `storage/encrypted/results/`
  - Return encrypted file path

- [ ] **`decrypt_and_download_excel(encrypted_file_path)`**:
  - Decrypt file using encryption_service.decrypt_file()
  - Return decrypted file for download

### Phase 7: Teacher API Endpoints (Day 6-7)
**File: `app/api/v1/teacher.py`**

- [ ] **`GET /api/v1/teacher/dashboard`**:
  - Return teacher statistics: total tests, total students, recent activity
  - Requires `@role_required('teacher')`

- [ ] **`POST /api/v1/teacher/tests`**:
  - Create new test
  - Body: {name, subject, duration}
  - Return created test

- [ ] **`GET /api/v1/teacher/tests`**:
  - List all tests by logged-in teacher
  - Return tests list

- [ ] **`GET /api/v1/teacher/tests/<test_id>`**:
  - Get test details with question count
  - Return test object

- [ ] **`PUT /api/v1/teacher/tests/<test_id>`**:
  - Update test
  - Body: {name, subject, duration}

- [ ] **`DELETE /api/v1/teacher/tests/<test_id>`**:
  - Delete test

- [ ] **`POST /api/v1/teacher/tests/<test_id>/questions/upload`**:
  - Upload Word/PowerPoint file
  - Parse file using file_parser_service
  - Bulk create questions using question_service
  - Return: {success: true, questions_count: 50}

- [ ] **`GET /api/v1/teacher/tests/<test_id>/questions`**:
  - Get all questions (encrypted or decrypted)
  - Query param: ?decrypt=true
  - Return questions list

- [ ] **`POST /api/v1/teacher/tests/<test_id>/terms`**:
  - Upload Terms & Conditions
  - Parse file
  - Validate max 10 bullets
  - Encrypt and save
  - Return terms

- [ ] **`GET /api/v1/teacher/tests/<test_id>/terms`**:
  - Get terms (decrypted)
  - Return terms list

- [ ] **`GET /api/v1/teacher/tests/<test_id>/results`**:
  - Get all results for test
  - Return results with student details

- [ ] **`GET /api/v1/teacher/tests/<test_id>/results/export`**:
  - Generate Excel file
  - Encrypt Excel
  - Return download link or file

### Phase 8: Frontend Templates - Base (Day 7)
**File: `app/templates/teacher/base_teacher.html`**

- [ ] Extend from `base.html`
- [ ] Sidebar navigation:
  - Dashboard
  - My Tests
  - Upload Questions
  - View Results
  - Logout
- [ ] Show teacher name in header
- [ ] Responsive design

### Phase 9: Dashboard (Day 7)
**File: `app/templates/teacher/dashboard.html`**

- [ ] Statistics cards:
  - Total Tests Created
  - Total Questions Uploaded
  - Total Students Assigned
  - Average Test Score
- [ ] Recent tests table (last 5 tests)
- [ ] Quick actions:
  - Create New Test button
  - Upload Questions button

### Phase 10: Manage Tests (Day 7-8)
**File: `app/templates/teacher/manage_tests.html`**

- [ ] "Create Test" button → opens modal or separate page
- [ ] Create test form:
  - Test Name
  - Subject
  - Duration (minutes)
  - Submit button
- [ ] Tests table:
  - Test Name
  - Subject
  - Duration
  - Questions Count
  - Actions (Edit, Delete, Upload Questions, View Results)
- [ ] Delete confirmation modal

### Phase 11: Upload Questions (Day 8)
**File: `app/templates/teacher/upload_questions.html`**

- [ ] Step 1: Select test (dropdown)
- [ ] Step 2: Choose file type (Word or PowerPoint)
- [ ] Step 3: Upload file
  - File input field
  - Accept only .docx or .pptx
  - Show file name after selection
- [ ] Upload button
- [ ] Progress indicator (uploading...)
- [ ] Success message: "50 questions uploaded successfully"
- [ ] Error handling: Show parsing errors
- [ ] Preview questions (optional): Show first 3 parsed questions

### Phase 12: Upload Terms & Conditions (Day 8)
**File: `app/templates/teacher/upload_terms.html`**

- [ ] Select test (dropdown)
- [ ] Choose file type (Word or PowerPoint)
- [ ] Upload file
- [ ] Validation: Show error if more than 10 bullets
- [ ] Preview terms before submitting
- [ ] Submit button
- [ ] Success message

### Phase 13: View Results (Day 8-9)
**File: `app/templates/teacher/view_results.html`**

- [ ] Select test (dropdown)
- [ ] Results statistics:
  - Total Attempts
  - Average Score
  - Highest Score
  - Lowest Score
  - Pass Rate
- [ ] Results table:
  - Student Name
  - Student ID
  - Total Questions
  - Correct Answers
  - Percentage
  - Date Completed
  - Action (View Details)
- [ ] Filter options:
  - By date
  - By percentage range
- [ ] Sort by: Name, Percentage, Date
- [ ] Pagination

**File: `app/templates/teacher/export_results.html`**

- [ ] Select test (dropdown)
- [ ] Preview results data
- [ ] "Export to Excel" button
- [ ] Download encrypted Excel file
- [ ] Message: "File is encrypted. Only you can decrypt it."

### Phase 14: Styling (Day 9)
**File: `app/static/css/teacher.css`**

- [ ] Sidebar styling (similar to admin)
- [ ] Dashboard cards with icons
- [ ] Tables styling (striped, hover)
- [ ] Upload area styling:
  - Drag-and-drop zone (optional)
  - File upload button
  - Progress bar
- [ ] Forms styling
- [ ] Results table highlighting:
  - Green for high scores (>80%)
  - Orange for medium (50-80%)
  - Red for low (<50%)
- [ ] Responsive design

### Phase 15: Testing (Day 9-10)
- [ ] Test Word document upload with 10 questions
- [ ] Test PowerPoint upload with 10 slides
- [ ] Test question parsing accuracy
- [ ] Test encryption of questions
- [ ] Test decryption when viewing
- [ ] Test Terms & Conditions upload
- [ ] Test validation: More than 10 bullets should fail
- [ ] Test results viewing
- [ ] Test Excel export
- [ ] Test Excel encryption
- [ ] Test Excel decryption and download
- [ ] Test on different browsers

---

## 📦 Required Libraries

```txt
# File Parsing
python-docx==1.1.0
python-pptx==0.6.23

# Excel Generation
openpyxl==3.1.2

# File Upload
Flask-Uploads==0.2.1  # or Werkzeug's secure_filename
```

---

## 📄 Sample Question Format

### Word Document Format:
```
Question 1: What is the capital of France?
A) London
B) Paris
C) Berlin
D) Madrid
Answer: B
Explanation: Paris is the capital city of France.

Question 2: What is 2 + 2?
A) 3
B) 4
C) 5
D) 6
Answer: B
Explanation: Basic arithmetic: 2 + 2 = 4.
```

### PowerPoint Format:
```
Slide 1:
Question 1: What is the capital of France?
A) London
B) Paris
C) Berlin
D) Madrid
Answer: B
Explanation: Paris is the capital city of France.

Slide 2:
Question 2: What is 2 + 2?
A) 3
B) 4
C) 5
D) 6
Answer: B
Explanation: Basic arithmetic: 2 + 2 = 4.
```

---

## 📄 Sample Terms & Conditions Format

```
1. You must complete the test in the allotted time.
2. No use of external resources or help is allowed.
3. Once you submit an answer, you cannot go back.
4. The test will auto-submit when time expires.
5. Your results will be shown immediately after submission.
6. Do not refresh the page during the test.
7. Ensure stable internet connection.
8. No communication with other students during test.
9. Any suspicious activity will be logged.
10. By starting the test, you agree to these terms.
```

---

## 🔐 Security Checklist

- [ ] All teacher routes protected with `@role_required('teacher')`
- [ ] Teachers can only view their own tests
- [ ] Teachers can only view results for their tests
- [ ] Uploaded files validated (only .docx, .pptx)
- [ ] File size limit (max 10 MB)
- [ ] Malicious file scanning (optional but recommended)
- [ ] Questions encrypted immediately after parsing
- [ ] Excel files encrypted before storage
- [ ] Decryption only happens when viewing/downloading
- [ ] Audit log all uploads and exports

---

## 📤 What You Need from Part 1

✅ **Before you start**:
- [ ] encryption_service.py with encrypt/decrypt functions
- [ ] Test model created
- [ ] Question model created
- [ ] TermsConditions model created
- [ ] Result model created
- [ ] Role-based decorator: `@role_required('teacher')`
- [ ] Teacher user created for testing

---

## 📥 What Other Parts Need from You

### For Student Module (Member 4):
- Questions in encrypted format (they need to decrypt)
- Terms & Conditions (to show before test)
- Test structure (duration, name, subject)

### For Admin Module (Member 2):
- Test list API (admin needs to see all tests for assignment)

### For Testing (Member 5):
- Sample Word/PPT files with questions
- API documentation

---

## 🆘 Common Issues & Solutions

**Issue**: Word parser not finding questions  
**Solution**: Check regex pattern, ensure "Question 1:" format exactly

**Issue**: PowerPoint parser fails on slides with images  
**Solution**: Extract only text, ignore images

**Issue**: Encryption fails  
**Solution**: Check encryption_service, verify key is set in .env

**Issue**: Excel file corrupted after encryption  
**Solution**: Encrypt as binary, not text. Use `encryption_service.encrypt_file()`

**Issue**: More than 10 terms uploaded  
**Solution**: Add validation before saving, show error to user

**Issue**: File upload too slow  
**Solution**: Add progress indicator, or limit file size

---

## 📞 Communication

**Coordinate with**:
- **Member 1**: Get encryption API working first
- **Member 4**: Share question data structure
- **Member 5**: Provide sample test files

**Daily Updates**:
- File parsing working
- Encryption integrated
- Excel export ready
- Any blockers

---

## 🏆 Success Criteria

At the end of your part, teacher should be able to:
- [ ] Log in as teacher
- [ ] Create new test
- [ ] Upload Word document with questions
- [ ] Upload PowerPoint with questions
- [ ] Upload Terms & Conditions
- [ ] View all uploaded questions (decrypted)
- [ ] See list of their tests
- [ ] View results for their tests in table
- [ ] Export results to encrypted Excel
- [ ] Download and open decrypted Excel file
- [ ] See student names, scores, percentages in Excel
- [ ] UI is clean and intuitive

**Good luck! You're building the content creation hub! 📚**
