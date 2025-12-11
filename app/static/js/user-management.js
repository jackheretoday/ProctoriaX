/**
 * User Management JavaScript
 * Handles user CRUD operations via AJAX
 */

// Delete user confirmation
function confirmDelete(userId, username) {
    if (confirm(`Are you sure you want to delete user "${username}"?`)) {
        deleteUser(userId);
    }
}

// Delete user via AJAX
async function deleteUser(userId) {
    try {
        const response = await fetch(`/admin/api/users/${userId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showAlert('User deleted successfully', 'success');
            // Reload page or remove row
            setTimeout(() => window.location.reload(), 1500);
        } else {
            showAlert(data.error || 'Error deleting user', 'danger');
        }
    } catch (error) {
        showAlert('Error deleting user', 'danger');
        console.error(error);
    }
}

// Reset password
async function resetPassword(userId) {
    if (!confirm('Reset password for this user?')) {
        return;
    }
    
    try {
        const response = await fetch(`/admin/api/users/${userId}/reset-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showPasswordModal(data.new_password);
        } else {
            showAlert(data.error || 'Error resetting password', 'danger');
        }
    } catch (error) {
        showAlert('Error resetting password', 'danger');
        console.error(error);
    }
}

// Show password in modal
function showPasswordModal(password) {
    const modalHTML = `
        <div class="modal fade" id="passwordModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">New Password</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>New password (save this, it won't be shown again):</p>
                        <div class="alert alert-warning">
                            <strong>${password}</strong>
                        </div>
                        <button class="btn btn-sm btn-secondary" onclick="copyToClipboard('${password}')">
                            Copy to Clipboard
                        </button>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-primary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    const modal = new bootstrap.Modal(document.getElementById('passwordModal'));
    modal.show();
    
    // Remove modal after close
    document.getElementById('passwordModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Password copied to clipboard', 'success');
    }).catch(() => {
        showAlert('Failed to copy', 'danger');
    });
}

// Show alert
function showAlert(message, type = 'info') {
    const alertHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    const container = document.querySelector('.container') || document.body;
    container.insertAdjacentHTML('afterbegin', alertHTML);
    
    // Auto-dismiss after 3 seconds
    setTimeout(() => {
        const alert = container.querySelector('.alert');
        if (alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }
    }, 3000);
}

// Search users (debounced)
let searchTimeout;
function searchUsers(query) {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        window.location.href = `/admin/users?search=${encodeURIComponent(query)}`;
    }, 500);
}
