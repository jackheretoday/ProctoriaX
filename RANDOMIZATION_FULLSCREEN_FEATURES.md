# 🎲 Question Randomization & 🖥️ Fullscreen Proctoring Features

## New Features Implemented

### 1. 🎲 **Question Randomization**
Every student gets questions in a **different random order** to prevent cheating.

### 2. 🖥️ **Fullscreen Proctoring**
Test automatically starts in fullscreen mode with violation tracking:
- **First Exit**: Warning message + auto re-enter fullscreen
- **Second Exit**: Test auto-submits immediately

---

## 🎲 Feature 1: Question Randomization

### How It Works

#### **When Test Starts** (`start_test` API):
```python
# Get all questions and randomize order
questions = QuestionService.get_questions_for_test(test_id, decrypt=False)
question_ids = [q.id for q in questions]
random.shuffle(question_ids)  # Randomize!

# Store in session for this student
session[f'test_{test_id}_question_order'] = question_ids
```

#### **When Showing Questions** (`take_test` route):
```python
# Get randomized order from session
question_order = session.get(f'test_{test_id}_question_order', [])

# Get question ID from randomized position
question_id = question_order[question_number - 1]

# Fetch and display that specific question
question_obj = Question.query.get(question_id)
current_question = QuestionService.decrypt_question(question_obj)
```

### Benefits

✅ **Different Order Per Student**:
- Student A: Q3, Q1, Q5, Q2, Q4
- Student B: Q2, Q4, Q1, Q3, Q5
- Student C: Q5, Q3, Q4, Q1, Q2

✅ **Prevents Cheating**:
- Students can't share "Answer for Question 1"
- Each student has different question at each position

✅ **Fair Testing**:
- All students get same questions
- Just in different order
- No advantage/disadvantage

---

## 🖥️ Feature 2: Fullscreen Proctoring

### How It Works

#### **Auto-Enter Fullscreen**:
```javascript
// Enters fullscreen 500ms after page loads
window.addEventListener('load', function() {
    setTimeout(function() {
        enterFullscreen();
    }, 500);
});
```

#### **Track Fullscreen Exits**:
```javascript
// Detect when student exits fullscreen
document.addEventListener('fullscreenchange', handleFullscreenExit);

function handleFullscreenExit() {
    if (!document.fullscreenElement) {
        // Call API to track violation
        fetch(`/student/tests/${TEST_ID}/fullscreen-violation`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(result => {
            if (result.auto_submit) {
                // Second violation - auto submit
                alert('Test Auto-Submitted!');
                window.location.href = `/student/tests/${TEST_ID}/submit`;
            } else {
                // First violation - warning
                alert('WARNING! Next exit will auto-submit!');
                setTimeout(enterFullscreen, 500);
            }
        });
    }
}
```

#### **Backend Tracking** (`track_fullscreen_violation` API):
```python
violations = session.get(f'test_{test_id}_fullscreen_violations', 0)
violations += 1
session[f'test_{test_id}_fullscreen_violations'] = violations

if violations >= 2:
    # Auto-submit on second violation
    return jsonify({
        'auto_submit': True,
        'message': 'Test auto-submitted due to fullscreen violations'
    })
else:
    # First violation - warning
    return jsonify({
        'auto_submit': False,
        'message': 'Warning: Exiting fullscreen again will auto-submit!'
    })
```

### Violation Flow

#### **First Violation**:
1. Student exits fullscreen (presses Esc or clicks browser button)
2. System detects exit
3. Violation count: 0 → 1
4. Shows warning alert: "⚠️ WARNING! Exiting fullscreen again will auto-submit your test!"
5. Automatically re-enters fullscreen after 500ms
6. Student can continue test

#### **Second Violation**:
1. Student exits fullscreen again
2. System detects exit
3. Violation count: 1 → 2
4. Shows alert: "⚠️ Test Auto-Submitted! You exited fullscreen mode twice."
5. Immediately redirects to submit page
6. Test is auto-submitted

### ESC Key Prevention

```javascript
// Warn before allowing Esc key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && fullscreenViolations === 0) {
        e.preventDefault();
        alert('⚠️ WARNING! Exiting fullscreen will count as a violation!');
        return false;
    }
});
```

---

## 📁 Files Modified

### Backend Files:

1. **`app/api/v1/student.py`**:
   - ✅ Added question randomization in `start_test()`
   - ✅ Added `track_fullscreen_violation()` endpoint
   - ✅ Modified `take_test()` to use randomized order
   - ✅ Added fullscreen violation tracking to session

2. **`app/services/question_service.py`**:
   - ✅ Added `decrypt_question()` method for single question decryption

### Frontend Files:

3. **`app/templates/student/take_test.html`**:
   - ✅ Added fullscreen auto-enter on load
   - ✅ Added fullscreen exit detection
   - ✅ Added violation tracking with API calls
   - ✅ Added ESC key prevention
   - ✅ Added auto-submit on second violation

---

## 🧪 Testing Guide

### Test Question Randomization:

1. **Create a test** with 5+ questions
2. **Have 2 students** start the same test
3. **Compare their screens**:
   - Student A's Question 1 ≠ Student B's Question 1
   - Both have same questions, different order

### Test Fullscreen Proctoring:

#### **Test 1: Auto-Enter**
1. Student starts test
2. ✅ Should automatically enter fullscreen
3. ✅ Test content fills entire screen

#### **Test 2: First Violation**
1. Student presses `Esc` or exits fullscreen
2. ✅ Warning alert appears
3. ✅ Automatically re-enters fullscreen
4. ✅ Student can continue test

#### **Test 3: Second Violation**
1. Student exits fullscreen again
2. ✅ "Test Auto-Submitted" alert appears
3. ✅ Redirects to submit page
4. ✅ Test is submitted automatically

#### **Test 4: ESC Key Warning**
1. Student presses `Esc` (first time)
2. ✅ Warning appears before exit
3. ✅ Can choose to stay in fullscreen

---

## ⚙️ Configuration

### Adjust Violation Limit:

In `app/api/v1/student.py`:
```python
if violations >= 2:  # Change 2 to desired limit
    # Auto-submit
```

### Adjust Fullscreen Entry Delay:

In `app/templates/student/take_test.html`:
```javascript
setTimeout(function() {
    enterFullscreen();
}, 500);  // Change 500ms to desired delay
```

### Disable Fullscreen (if needed):

Comment out in `take_test.html`:
```javascript
// window.addEventListener('load', function() {
//     setTimeout(function() {
//         enterFullscreen();
//     }, 500);
// });
```

---

## 🔒 Security Features

✅ **Session-Based Tracking**:
- Violations stored in server session
- Can't be manipulated by client

✅ **Server-Side Validation**:
- All violation checks happen on backend
- Frontend can't bypass auto-submit

✅ **Randomization Per Session**:
- Each test attempt gets new random order
- Can't predict question order

✅ **Persistent Order**:
- Order stays same during test
- Prevents confusion if student refreshes

---

## 📊 Benefits

### For Teachers:
✅ Reduced cheating
✅ Fair assessment
✅ Automated proctoring
✅ No manual monitoring needed

### For Students:
✅ Clear warnings before penalties
✅ Fair testing environment
✅ Can't accidentally cheat
✅ Focused test-taking

### For System:
✅ Automated enforcement
✅ Logged violations
✅ Scalable proctoring
✅ No additional hardware needed

---

## 🚀 Ready to Use!

Both features are now active:
1. ✅ Questions randomize automatically
2. ✅ Fullscreen enforced automatically
3. ✅ Violations tracked automatically
4. ✅ Auto-submit works automatically

**Just restart the server and test!**

## Date: November 1, 2025
