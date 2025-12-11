/**
 * Test Timer - Critical Component
 * Handles countdown timer for test with auto-submit
 */

class TestTimer {
    constructor(durationSeconds, onExpire) {
        this.totalSeconds = durationSeconds;
        this.remainingSeconds = durationSeconds;
        this.onExpire = onExpire;
        this.timerInterval = null;
        this.timerElement = null;
    }
    
    /**
     * Initialize timer with display element
     */
    init(timerElementId) {
        this.timerElement = document.getElementById(timerElementId);
        if (!this.timerElement) {
            console.error('Timer element not found');
            return;
        }
        
        // Load saved time from localStorage if exists
        const savedTime = localStorage.getItem('test_timer_remaining');
        if (savedTime) {
            this.remainingSeconds = parseInt(savedTime);
        }
        
        this.start();
    }
    
    /**
     * Start the countdown
     */
    start() {
        this.updateDisplay();
        
        this.timerInterval = setInterval(() => {
            this.remainingSeconds--;
            
            // Save to localStorage
            localStorage.setItem('test_timer_remaining', this.remainingSeconds);
            
            this.updateDisplay();
            
            // Check if time expired
            if (this.remainingSeconds <= 0) {
                this.stop();
                if (this.onExpire) {
                    this.onExpire();
                }
            }
        }, 1000);
    }
    
    /**
     * Stop the timer
     */
    stop() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
        localStorage.removeItem('test_timer_remaining');
    }
    
    /**
     * Update timer display
     */
    updateDisplay() {
        if (!this.timerElement) return;
        
        const hours = Math.floor(this.remainingSeconds / 3600);
        const minutes = Math.floor((this.remainingSeconds % 3600) / 60);
        const seconds = this.remainingSeconds % 60;
        
        let display = '';
        if (hours > 0) {
            display = `${hours}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        } else {
            display = `${minutes}:${String(seconds).padStart(2, '0')}`;
        }
        
        this.timerElement.textContent = display;
        
        // Color coding
        const parentElement = this.timerElement.parentElement;
        if (this.remainingSeconds < 60) {
            // Less than 1 minute - RED
            parentElement.className = 'timer-display danger';
        } else if (this.remainingSeconds < 300) {
            // Less than 5 minutes - YELLOW/WARNING
            parentElement.className = 'timer-display warning';
        } else {
            // Normal - GREEN
            parentElement.className = 'timer-display';
        }
        
        // Warning alerts
        if (this.remainingSeconds === 60) {
            alert('Warning: Only 1 minute remaining!');
        } else if (this.remainingSeconds === 300) {
            alert('Warning: 5 minutes remaining!');
        }
    }
    
    /**
     * Get remaining time
     */
    getRemainingSeconds() {
        return this.remainingSeconds;
    }
    
    /**
     * Get formatted remaining time
     */
    getFormattedTime() {
        const hours = Math.floor(this.remainingSeconds / 3600);
        const minutes = Math.floor((this.remainingSeconds % 3600) / 60);
        const seconds = this.remainingSeconds % 60;
        
        if (hours > 0) {
            return `${hours}h ${minutes}m ${seconds}s`;
        } else if (minutes > 0) {
            return `${minutes}m ${seconds}s`;
        } else {
            return `${seconds}s`;
        }
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TestTimer;
}
