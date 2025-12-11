# Teacher View Results - Error Fix

## Problem
Teacher's "View Results" page was showing error:
```
Error loading results: 'Result' object has no attribute 'wrong_answers'
```

## Root Cause
The Result model uses different attribute names than what the code was expecting:
- Model has: `incorrect_answers` and `unanswered`
- Code was using: `wrong_answers` and `unattempted`

## Files Fixed

### 1. `app/services/result_service.py`
**Changed in 3 methods:**

#### `get_results_for_test()` - Line 42-43
```python
# Before
'wrong_answers': result.wrong_answers,
'unattempted': result.unattempted,

# After
'incorrect_answers': result.incorrect_answers,
'unanswered': result.unanswered,
```

#### `get_result_by_id()` - Line 88-89
```python
# Before
'wrong_answers': result.wrong_answers,
'unattempted': result.unattempted,

# After
'incorrect_answers': result.incorrect_answers,
'unanswered': result.unanswered,
```

#### `get_results_by_student()` - Line 185-186
```python
# Before
'wrong_answers': result.wrong_answers,
'unattempted': result.unattempted,

# After
'incorrect_answers': result.incorrect_answers,
'unanswered': result.unanswered,
```

### 2. `app/templates/teacher/view_results.html`
**Updated table headers and data:**

```html
<!-- Before -->
<th>Wrong</th>
...
<td class="text-danger">{{ result.wrong_answers }}</td>

<!-- After -->
<th>Incorrect</th>
<th>Unanswered</th>
...
<td class="text-danger">❌ {{ result.incorrect_answers }}</td>
<td class="text-muted">⚪ {{ result.unanswered }}</td>
```

## What's Fixed

✅ **View Results Page**:
- No more attribute errors
- Displays all student results correctly
- Shows correct/incorrect/unanswered counts
- Added emoji indicators for better UX

✅ **Export to Excel**:
- Uses the same fixed ResultService
- Will export with correct column names

✅ **Statistics Cards**:
- Total attempts
- Average score
- Highest/lowest scores
- All working correctly

## Result Model Attributes (Reference)

The correct attributes in the Result model are:
```python
class Result:
    total_questions       # Total number of questions
    correct_answers       # Number of correct answers
    incorrect_answers     # Number of incorrect answers (NOT wrong_answers)
    unanswered           # Number of unanswered questions (NOT unattempted)
    score                # Numeric score
    percentage           # Percentage score
    passed               # Boolean pass/fail
    time_taken           # Time in minutes
    completed_at         # Completion timestamp
```

## Testing Checklist

✅ Teacher can view results page
✅ Select a test from dropdown
✅ See statistics cards
✅ View results table with all columns
✅ Export results to Excel
✅ No attribute errors

## Date: November 1, 2025
