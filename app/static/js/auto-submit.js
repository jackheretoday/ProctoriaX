/**
 * Auto-Submit Functionality
 * Automatically submits test when timer expires
 */

class AutoSubmit {
    constructor(testId) {
        this.testId = testId;
        this.submitInProgress = false;
    }
    
    /**
     * Submit test automatically
     */
    async submit() {
        if (this.submitInProgress) {
            console.log('Submit already in progress');
            return;
        }
        
        this.submitInProgress = true;
        
        // Show loading indicator
        this.showLoadingIndicator();
        
        try {
            // Call submit endpoint
            const response = await fetch(`/student/tests/${this.testId}/submit`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.redirected) {
                // Follow redirect
                window.location.href = response.url;
            } else if (response.ok) {
                // Redirect to results
                window.location.href = `/student/tests/${this.testId}/result`;
            } else {
                throw new Error('Submit failed');
            }
            
        } catch (error) {
            console.error('Auto-submit error:', error);
            this.hideLoadingIndicator();
            alert('Error submitting test. Please try again.');
            this.submitInProgress = false;
        }
    }
    
    /**
     * Show loading indicator
     */
    showLoadingIndicator() {
        const loader = document.createElement('div');
        loader.id = 'autoSubmitLoader';
        loader.innerHTML = `
            <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                        background: rgba(0,0,0,0.7); display: flex; align-items: center; 
                        justify-content: center; z-index: 9999;">
                <div style="background: white; padding: 30px; border-radius: 10px; text-align: center;">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p style="margin-top: 15px; font-size: 18px;">Submitting your test...</p>
                </div>
            </div>
        `;
        document.body.appendChild(loader);
    }
    
    /**
     * Hide loading indicator
     */
    hideLoadingIndicator() {
        const loader = document.getElementById('autoSubmitLoader');
        if (loader) {
            loader.remove();
        }
    }
    
    /**
     * Handle timer expiration
     */
    onTimerExpire() {
        alert('Time is up! Your test will be submitted automatically.');
        
        // Disable all inputs
        const inputs = document.querySelectorAll('input, button, textarea, select');
        inputs.forEach(input => input.disabled = true);
        
        // Submit after brief delay
        setTimeout(() => {
            this.submit();
        }, 1000);
    }
}

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AutoSubmit;
}
