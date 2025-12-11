/**
 * Prevent Navigation - Enhanced Protection
 * Multiple layers of protection against navigation during test
 */

(function() {
    'use strict';
    
    let navigationBlocked = false;
    
    /**
     * Advanced back button prevention
     */
    function preventBackNavigation() {
        // Method 1: History manipulation
        window.history.pushState(null, '', window.location.href);
        window.onpopstate = function() {
            window.history.pushState(null, '', window.location.href);
        };
        
        // Method 2: Continuous history pushing
        setInterval(function() {
            if (navigationBlocked) {
                window.history.pushState(null, '', window.location.href);
            }
        }, 500);
    }
    
    /**
     * Prevent all forms of page reload
     */
    function preventReload() {
        // Disable all refresh attempts
        window.addEventListener('beforeunload', function(e) {
            if (navigationBlocked) {
                const message = 'Test in progress! Do not leave this page.';
                e.preventDefault();
                e.returnValue = message;
                return message;
            }
        });
        
        // Intercept form submissions that might navigate away
        document.addEventListener('submit', function(e) {
            if (e.target.id !== 'answerForm' && e.target.id !== 'testSubmitForm') {
                if (navigationBlocked) {
                    e.preventDefault();
                    alert('Form submission blocked during test.');
                }
            }
        });
    }
    
    /**
     * Prevent all navigation links
     */
    function preventLinkNavigation() {
        document.addEventListener('click', function(e) {
            if (navigationBlocked && e.target.tagName === 'A') {
                // Allow only specific test-related links
                const allowedPaths = ['/student/tests/', '/submit'];
                const href = e.target.getAttribute('href') || '';
                
                let isAllowed = false;
                for (let path of allowedPaths) {
                    if (href.includes(path)) {
                        isAllowed = true;
                        break;
                    }
                }
                
                if (!isAllowed) {
                    e.preventDefault();
                    alert('Navigation blocked during test.');
                }
            }
        });
    }
    
    /**
     * Disable developer tools (best effort)
     */
    function discourageDevTools() {
        // Detect if DevTools is open (not foolproof)
        const devToolsOpen = () => {
            const threshold = 160;
            return window.outerWidth - window.innerWidth > threshold ||
                   window.outerHeight - window.innerHeight > threshold;
        };
        
        setInterval(function() {
            if (navigationBlocked && devToolsOpen()) {
                console.log('Developer tools detected during test');
                // Log this event - could be suspicious activity
            }
        }, 1000);
        
        // Disable common dev tool shortcuts
        document.addEventListener('keydown', function(e) {
            // F12
            if (e.keyCode === 123) {
                e.preventDefault();
                return false;
            }
            // Ctrl+Shift+I
            if (e.ctrlKey && e.shiftKey && e.keyCode === 73) {
                e.preventDefault();
                return false;
            }
            // Ctrl+Shift+J
            if (e.ctrlKey && e.shiftKey && e.keyCode === 74) {
                e.preventDefault();
                return false;
            }
            // Ctrl+U (view source)
            if (e.ctrlKey && e.keyCode === 85) {
                e.preventDefault();
                return false;
            }
        });
    }
    
    /**
     * Prevent tab switching detection (visibility API)
     */
    function monitorTabVisibility() {
        document.addEventListener('visibilitychange', function() {
            if (navigationBlocked && document.hidden) {
                console.log('Student switched tabs/windows during test');
                // This could be logged as suspicious activity
                // For now, just log it
            }
        });
    }
    
    /**
     * Enable all navigation protection
     */
    function enableNavigationProtection() {
        navigationBlocked = true;
        preventBackNavigation();
        preventReload();
        preventLinkNavigation();
        discourageDevTools();
        monitorTabVisibility();
        
        console.log('Navigation protection enabled');
    }
    
    /**
     * Disable navigation protection (when test ends)
     */
    function disableNavigationProtection() {
        navigationBlocked = false;
        window.onbeforeunload = null;
        window.onpopstate = null;
        
        console.log('Navigation protection disabled');
    }
    
    // Auto-enable on page load
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', enableNavigationProtection);
    } else {
        enableNavigationProtection();
    }
    
    // Expose globally
    window.enableNavigationProtection = enableNavigationProtection;
    window.disableNavigationProtection = disableNavigationProtection;
    
})();
