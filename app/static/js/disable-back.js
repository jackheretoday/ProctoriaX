/**
 * Disable Back Button
 * Prevents browser back navigation during test
 */

(function() {
    'use strict';
    
    /**
     * Disable browser back button
     */
    function disableBackButton() {
        // Push a dummy state to prevent back navigation
        history.pushState(null, null, location.href);
        
        // Handle popstate event (when user clicks back)
        window.onpopstate = function() {
            history.go(1);
        };
    }
    
    /**
     * Show warning when trying to leave page
     */
    function preventNavigation() {
        window.onbeforeunload = function(e) {
            const message = 'Test in progress. Are you sure you want to leave? Your progress may be lost.';
            e.returnValue = message;
            return message;
        };
    }
    
    /**
     * Disable keyboard shortcuts that can navigate away
     */
    function disableKeyboardShortcuts(e) {
        // Disable F5 (refresh)
        if (e.key === 'F5' || e.keyCode === 116) {
            e.preventDefault();
            alert('Page refresh is disabled during the test.');
            return false;
        }
        
        // Disable Ctrl+R (refresh)
        if ((e.ctrlKey || e.metaKey) && (e.key === 'r' || e.keyCode === 82)) {
            e.preventDefault();
            alert('Page refresh is disabled during the test.');
            return false;
        }
        
        // Disable Ctrl+W (close tab)
        if ((e.ctrlKey || e.metaKey) && (e.key === 'w' || e.keyCode === 87)) {
            e.preventDefault();
            alert('Cannot close tab during test.');
            return false;
        }
        
        // Disable Alt+F4 (close window)
        if (e.altKey && e.keyCode === 115) {
            e.preventDefault();
            alert('Cannot close window during test.');
            return false;
        }
        
        // Disable Backspace as navigation (except in input fields)
        if (e.keyCode === 8 && e.target.tagName !== 'INPUT' && e.target.tagName !== 'TEXTAREA') {
            e.preventDefault();
            return false;
        }
    }
    
    /**
     * Disable right-click context menu
     */
    function disableContextMenu(e) {
        e.preventDefault();
        return false;
    }
    
    /**
     * Initialize all navigation restrictions
     */
    function initNavigationBlock() {
        disableBackButton();
        preventNavigation();
        
        // Add keyboard event listeners
        document.addEventListener('keydown', disableKeyboardShortcuts);
        
        // Disable right-click
        document.addEventListener('contextmenu', disableContextMenu);
        
        console.log('Navigation blocking initialized');
    }
    
    /**
     * Remove navigation restrictions (call when test is complete)
     */
    function removeNavigationBlock() {
        window.onbeforeunload = null;
        window.onpopstate = null;
        document.removeEventListener('keydown', disableKeyboardShortcuts);
        document.removeEventListener('contextmenu', disableContextMenu);
        
        console.log('Navigation blocking removed');
    }
    
    // Auto-initialize when script loads
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initNavigationBlock);
    } else {
        initNavigationBlock();
    }
    
    // Expose functions globally
    window.disableBackButton = disableBackButton;
    window.removeNavigationBlock = removeNavigationBlock;
    
})();
