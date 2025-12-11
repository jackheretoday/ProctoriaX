/**
 * Form Validator for Test Interface
 * Validates answer selection and confirms submissions
 */

class TestFormValidator {
    /**
     * Validate answer form before submission
     */
    static validateAnswerForm(formElement) {
        const selectedAnswer = formElement.querySelector('input[name="selected_answer"]:checked');
        
        if (!selectedAnswer) {
            alert('Please select an answer before submitting.');
            return false;
        }
        
        return true;
    }
    
    /**
     * Confirm answer submission
     */
    static confirmAnswerSubmission(questionNumber, totalQuestions) {
        let message = 'Are you sure you want to submit this answer? You cannot change it later.';
        
        if (questionNumber === totalQuestions) {
            message = 'This is the last question. After submitting, you will be asked to submit the entire test.';
        }
        
        return confirm(message);
    }
    
    /**
     * Confirm final test submission
     */
    static confirmTestSubmission(answeredCount, totalQuestions) {
        let message = `You have answered ${answeredCount} out of ${totalQuestions} questions.\n\n`;
        message += 'Are you sure you want to submit the test? This action cannot be undone.';
        
        if (answeredCount < totalQuestions) {
            const unanswered = totalQuestions - answeredCount;
            message += `\n\nWarning: ${unanswered} question(s) will be marked as unanswered.`;
        }
        
        return confirm(message);
    }
    
    /**
     * Validate and submit answer
     */
    static handleAnswerSubmit(formElement, questionNumber, totalQuestions, callback) {
        // Prevent default form submission
        const submitHandler = function(e) {
            e.preventDefault();
            
            // Validate
            if (!TestFormValidator.validateAnswerForm(formElement)) {
                return false;
            }
            
            // Confirm
            if (!TestFormValidator.confirmAnswerSubmission(questionNumber, totalQuestions)) {
                return false;
            }
            
            // Call callback
            if (callback) {
                callback(formElement);
            }
            
            return false;
        };
        
        formElement.addEventListener('submit', submitHandler);
    }
    
    /**
     * Add visual feedback for selected option
     */
    static highlightSelectedOption() {
        const options = document.querySelectorAll('input[name="selected_answer"]');
        
        options.forEach(option => {
            option.addEventListener('change', function() {
                // Remove highlight from all labels
                document.querySelectorAll('.option-label').forEach(label => {
                    label.classList.remove('selected');
                });
                
                // Add highlight to selected label
                if (this.checked) {
                    this.closest('.option-label').classList.add('selected');
                }
            });
        });
    }
    
    /**
     * Prevent accidental double submission
     */
    static preventDoubleSubmit(buttonElement) {
        buttonElement.addEventListener('click', function() {
            if (this.disabled) {
                return false;
            }
            
            // Disable after first click
            setTimeout(() => {
                this.disabled = true;
                this.textContent = 'Submitting...';
            }, 100);
        });
    }
    
    /**
     * Initialize all validators
     */
    static init() {
        TestFormValidator.highlightSelectedOption();
        
        // Find submit button and prevent double-submit
        const submitBtn = document.querySelector('button[type="submit"]');
        if (submitBtn) {
            TestFormValidator.preventDoubleSubmit(submitBtn);
        }
    }
}

// Auto-initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => TestFormValidator.init());
} else {
    TestFormValidator.init();
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TestFormValidator;
}
