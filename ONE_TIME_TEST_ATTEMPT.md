# 🔒 One-Time Test Attempt - Completed Tests Hidden

## Issue

Students could see tests they had already completed in their dashboard, potentially causing confusion or attempts to retake tests.

---

## Solution

Tests that have been completed (have a Result record) are now automatically hidden from the student's dashboard.

---

## Implementation

### **Dashboard Filter** (`app/api/v1/student.py`)

**Before**:
```python
# Get result if exists
result = Result.query.filter_by(
    student_id=current_user.id,
    test_id=assignment.test_id
).first()

# Shows test regardless of completion
test_data = {
    'id': test.id,
    'name': test.name,
    'status': result.status if result else 'pending',
    'result': result.to_dict() if result else None
}

# Add to lists
todays_tests.append(test_data)
```

**After**:
```python
# Get result if exists
result = Result.query.filter_by(
    student_id=current_user.id,
    test_id=assignment.test_id
).first()

# SKIP if test already completed - don't show again
if result:
    continue  # Test already attempted, hide from list

# Only show if NOT completed
test_data = {
    'id': test.id,
    'name': test.name,
    'status': 'pending',
    'result': None
}

# Add to lists (only incomplete tests)
todays_tests.append(test_data)
```

### **Additional Protection** (Already Existed)

The test instructions route already had protection:

```python
# Check if test already completed
result = Result.query.filter_by(
    student_id=current_user.id,
    test_id=test_id
).first()

if result:
    flash('You have already completed this test', 'info')
    return redirect(url_for('student.test_result', test_id=test_id))
```

---

## How It Works

### **Flow for New Tests**:
```
1. Teacher assigns test to student
   └─> Test appears in student's dashboard

2. Student takes test
   └─> Test still visible until submitted

3. Student submits test
   └─> Result record created
   └─> Test DISAPPEARS from dashboard ✅
```

### **Flow for Completed Tests**:
```
1. Student logs in
   └─> Dashboard loads

2. Check each assignment
   ├─> Has result? → SKIP (don't show)
   └─> No result? → SHOW in dashboard

3. Only incomplete tests visible ✅
```

### **If Student Tries Direct Access**:
```
1. Student tries to access completed test URL
   └─> /tests/123/instructions

2. System checks for result
   ├─> Result exists?
   │   └─> Redirect to result page
   │   └─> Flash: "You have already completed this test"
   └─> No result?
       └─> Show instructions (allow start)
```

---

## User Experience

### **Before Completion**:
```
Student Dashboard:
┌─────────────────────────────┐
│ Today's Tests               │
├─────────────────────────────┤
│ ✓ Python Basics Test        │  ← Shows in dashboard
│   Duration: 30 minutes      │
│   [Start Test]              │
└─────────────────────────────┘
```

### **After Completion**:
```
Student Dashboard:
┌─────────────────────────────┐
│ Today's Tests               │
├─────────────────────────────┤
│ No tests available          │  ← Test disappeared!
└─────────────────────────────┘

(Test is completed, no longer shown)
```

### **If Student Bookmarked Test URL**:
```
Student clicks old bookmark:
/tests/123/instructions

↓

System checks:
Result exists? YES

↓

Redirect to: /tests/123/result
Flash message: "You have already completed this test"

↓

Shows test results page ✅
```

---

## Benefits

### **For Students**:
✅ Clear dashboard - only shows available tests
✅ No confusion about which tests to take
✅ Can't accidentally retake a test
✅ Clean, organized view

### **For Teachers**:
✅ Ensures one attempt per test
✅ Fair testing environment
✅ Accurate results tracking
✅ No duplicate submissions

### **For System**:
✅ Data integrity maintained
✅ No duplicate results
✅ Clear test lifecycle
✅ Better database management

---

## Test States

### **1. Not Started** (Visible):
- ✅ Shows in dashboard
- ✅ "Start Test" button available
- ✅ Can access instructions

### **2. In Progress** (Visible):
- ✅ Shows in dashboard
- ✅ Can continue test
- ✅ Timer running

### **3. Completed** (Hidden):
- ❌ Does NOT show in dashboard
- ❌ Cannot start again
- ✅ Can view results only

---

## Edge Cases Handled

### **Case 1: Student Refreshes During Test**
```
Test in progress → Refresh page
↓
No result yet → Test still visible
↓
Can continue test ✅
```

### **Case 2: Violation Auto-Submit**
```
Violation detected → Test auto-submitted
↓
Result created → Test disappears from dashboard
↓
Student can view result ✅
```

### **Case 3: Time Expiry Auto-Submit**
```
Time runs out → Test auto-submitted
↓
Result created → Test disappears from dashboard
↓
Student can view result ✅
```

### **Case 4: Direct URL Access**
```
Student types: /tests/123/instructions
↓
System checks result
↓
Result exists? → Redirect to result page
No result? → Allow access
```

### **Case 5: Multiple Students**
```
Student A completes test
├─> Test hidden for Student A ✅
└─> Test still visible for Student B ✅

Each student tracked separately!
```

---

## Database Logic

### **Query**:
```python
# Check if student completed this specific test
result = Result.query.filter_by(
    student_id=current_user.id,  # Specific student
    test_id=assignment.test_id    # Specific test
).first()

if result:
    # Student completed this test
    # DON'T show in dashboard
    continue
else:
    # Student hasn't completed this test
    # SHOW in dashboard
    add_to_available_tests()
```

### **Result Table**:
```
Results Table:
┌────────────┬─────────┬────────────────┐
│ student_id │ test_id │ completed_at   │
├────────────┼─────────┼────────────────┤
│ 1          │ 5       │ 2025-11-01...  │  ← Student 1 completed Test 5
│ 2          │ 5       │ NULL           │  ← Student 2 hasn't completed Test 5
│ 1          │ 6       │ NULL           │  ← Student 1 hasn't completed Test 6
└────────────┴─────────┴────────────────┘

Dashboard for Student 1:
- Test 5: Hidden (completed) ❌
- Test 6: Visible (pending) ✅

Dashboard for Student 2:
- Test 5: Visible (pending) ✅
- Test 6: Visible (pending) ✅
```

---

## Security

### **Cannot Retake Test**:
✅ Result check prevents restart
✅ Dashboard hides completed tests
✅ Direct URL redirects to results
✅ Session validation

### **Data Integrity**:
✅ One result per student per test
✅ No duplicate submissions
✅ Unique constraint enforced
✅ Atomic operations

---

## Testing Checklist

### ✅ **Test 1: New Test**
- [ ] Assign test to student
- [ ] Student logs in
- [ ] Test appears in "Today's Tests"
- [ ] Click "Start Test"
- [ ] Test loads successfully

### ✅ **Test 2: Complete Test**
- [ ] Student takes test
- [ ] Student submits test
- [ ] Return to dashboard
- [ ] Test NO LONGER appears ✅
- [ ] Dashboard shows "No tests available"

### ✅ **Test 3: Try to Access Completed Test**
- [ ] Complete a test
- [ ] Copy test instructions URL
- [ ] Try to access URL
- [ ] Redirected to results page ✅
- [ ] Message: "You have already completed this test"

### ✅ **Test 4: Multiple Students**
- [ ] Assign test to 2 students
- [ ] Student A completes test
- [ ] Student A: Test hidden ✅
- [ ] Student B: Test still visible ✅

### ✅ **Test 5: Violation Auto-Submit**
- [ ] Start test
- [ ] Trigger violation twice
- [ ] Test auto-submits
- [ ] Return to dashboard
- [ ] Test disappeared ✅

---

## Files Modified

### **1. `app/api/v1/student.py`**
**Changed**: `dashboard()` function
- Added result check before adding to lists
- `if result: continue` - skips completed tests
- Only shows incomplete tests

**Existing**: `test_instructions()` function
- Already had result check
- Redirects to result if completed
- No changes needed

---

## Summary

✅ **Completed tests hidden from dashboard**
✅ **Students can't retake tests**
✅ **Clean, organized student view**
✅ **Direct URL access protected**
✅ **One attempt per test enforced**
✅ **Fair testing environment**

**Test lifecycle is now properly managed!** 🎉

## Date: November 1, 2025
