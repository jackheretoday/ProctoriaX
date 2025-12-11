/**
 * Main JavaScript - Common Utilities
 */

// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(400px)';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// Confirm deletion
function confirmDelete(message) {
    return confirm(message || 'Are you sure you want to delete this? This action cannot be undone.');
}

// Show loading spinner
function showLoading(button) {
    const originalText = button.textContent;
    button.disabled = true;
    button.innerHTML = '<span class="spinner"></span> Loading...';
    return originalText;
}

// Hide loading spinner
function hideLoading(button, originalText) {
    button.disabled = false;
    button.textContent = originalText;
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(err => {
        console.error('Failed to copy:', err);
        showToast('Failed to copy', 'error');
    });
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type}`;
    toast.textContent = message;
    toast.style.position = 'fixed';
    toast.style.top = '70px';
    toast.style.right = '20px';
    toast.style.zIndex = '9999';
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Validate form
function validateForm(formId, rules) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    let isValid = true;
    
    for (const [fieldName, validators] of Object.entries(rules)) {
        const field = form.elements[fieldName];
        if (!field) continue;
        
        for (const validator of validators) {
            if (!validator.test(field.value)) {
                showToast(validator.message, 'error');
                field.focus();
                isValid = false;
                break;
            }
        }
        
        if (!isValid) break;
    }
    
    return isValid;
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// AJAX helper
async function fetchJSON(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }
        
        return data;
    } catch (error) {
        console.error('Fetch error:', error);
        showToast(error.message, 'error');
        throw error;
    }
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        confirmDelete,
        showLoading,
        hideLoading,
        formatDate,
        copyToClipboard,
        showToast,
        validateForm,
        debounce,
        fetchJSON
    };
}