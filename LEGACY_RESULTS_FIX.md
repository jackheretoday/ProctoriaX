# Legacy Results Fix - wrong_answers Error

## Problem
Error: `'Result' object has no attribute 'wrong_answers'`

This error occurred for tests that had results created BEFORE the attribute name was changed from `wrong_answers` to `incorrect_answers`.

## Root Causes
1. **Old database records**: Results created before the fix still use old attribute names
2. **Incorrect calculation**: The `incorrect_answers` calculation didn't account for `unanswered` questions
3. **No backward compatibility**: Code didn't handle legacy data gracefully

## Solutions Implemented

### 1. Fixed Result Model Calculation (`app/models/result.py`)

**Problem**: Calculation was wrong
```python
# Before
self.incorrect_answers = total_questions - correct_answers  # Wrong!
self.unanswered = kwargs.get('unanswered', 0)
```

**Solution**: Fixed order and calculation
```python
# After
self.unanswered = kwargs.get('unanswered', 0)
# Calculate incorrect answers (total - correct - unanswered)
self.incorrect_answers = total_questions - correct_answers - self.unanswered
```

### 2. Added Backward Compatibility (`app/services/result_service.py`)

Added safety checks in all methods to handle legacy results:

```python
# Handle legacy results that might not have incorrect_answers
incorrect_answers = getattr(result, 'incorrect_answers', None)
if incorrect_answers is None:
    # Calculate from total - correct - unanswered
    unanswered = getattr(result, 'unanswered', 0)
    incorrect_answers = result.total_questions - result.correct_answers - unanswered

unanswered = getattr(result, 'unanswered', 0)
```

**Methods Updated**:
1. `get_results_for_test()` - Used by teacher view results
2. `get_result_by_id()` - Used for individual result lookup
3. `get_results_by_student()` - Used for student dashboard

### 3. Created Data Fix Script (`fix_results_data.py`)

Optional script to permanently fix old records in database:
```python
python fix_results_data.py
```

This will:
- Find all results with missing/incorrect `incorrect_answers`
- Calculate correct values
- Update database
- Commit changes

## How It Works Now

### For New Results:
✅ Created with correct `incorrect_answers` value
✅ Properly accounts for unanswered questions
✅ Formula: `incorrect = total - correct - unanswered`

### For Old Results:
✅ Automatically calculated on-the-fly using `getattr()`
✅ No database changes needed
✅ Backward compatible
✅ No errors thrown

## Testing

### Test Cases:
1. ✅ View results for test with old data → Works
2. ✅ View results for test with new data → Works
3. ✅ View results for test with mixed data → Works
4. ✅ Export results with old data → Works
5. ✅ Student views their old results → Works

### Verification:
```python
# Old result (legacy)
result.incorrect_answers  # Might not exist
# Solution: getattr() calculates it dynamically

# New result
result.incorrect_answers  # Always exists and correct
```

## Migration Path (Optional)

If you want to permanently fix old records:

### Option 1: Run Fix Script
```bash
cd testing-platform
python fix_results_data.py
```

### Option 2: Let It Auto-Fix
- Current code handles legacy data automatically
- No manual intervention needed
- Works seamlessly

## Summary

✅ **Fixed**: Result model calculation
✅ **Added**: Backward compatibility for legacy data
✅ **Created**: Optional fix script
✅ **Tested**: All result viewing scenarios
✅ **Result**: No more `wrong_answers` errors!

## Date: November 1, 2025
