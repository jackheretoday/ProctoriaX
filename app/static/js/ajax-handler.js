/**
 * AJAX Handler - Simplify AJAX requests
 */

class AjaxHandler {
    constructor(baseURL = '') {
        this.baseURL = baseURL;
        this.defaultHeaders = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        };
    }

    /**
     * GET request
     */
    async get(url, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const fullURL = queryString ? `${this.baseURL}${url}?${queryString}` : `${this.baseURL}${url}`;
        
        try {
            const response = await fetch(fullURL, {
                method: 'GET',
                headers: this.defaultHeaders
            });
            
            return await this.handleResponse(response);
        } catch (error) {
            return this.handleError(error);
        }
    }

    /**
     * POST request
     */
    async post(url, data = {}) {
        try {
            const response = await fetch(`${this.baseURL}${url}`, {
                method: 'POST',
                headers: this.defaultHeaders,
                body: JSON.stringify(data)
            });
            
            return await this.handleResponse(response);
        } catch (error) {
            return this.handleError(error);
        }
    }

    /**
     * PUT request
     */
    async put(url, data = {}) {
        try {
            const response = await fetch(`${this.baseURL}${url}`, {
                method: 'PUT',
                headers: this.defaultHeaders,
                body: JSON.stringify(data)
            });
            
            return await this.handleResponse(response);
        } catch (error) {
            return this.handleError(error);
        }
    }

    /**
     * DELETE request
     */
    async delete(url) {
        try {
            const response = await fetch(`${this.baseURL}${url}`, {
                method: 'DELETE',
                headers: this.defaultHeaders
            });
            
            return await this.handleResponse(response);
        } catch (error) {
            return this.handleError(error);
        }
    }

    /**
     * Upload file
     */
    async uploadFile(url, file, additionalData = {}) {
        try {
            const formData = new FormData();
            formData.append('file', file);
            
            // Add additional data
            for (const [key, value] of Object.entries(additionalData)) {
                formData.append(key, value);
            }
            
            const response = await fetch(`${this.baseURL}${url}`, {
                method: 'POST',
                body: formData
                // Don't set Content-Type header - browser will set it with boundary
            });
            
            return await this.handleResponse(response);
        } catch (error) {
            return this.handleError(error);
        }
    }

    /**
     * Handle response
     */
    async handleResponse(response) {
        const contentType = response.headers.get('content-type');
        
        let data;
        if (contentType && contentType.includes('application/json')) {
            data = await response.json();
        } else {
            data = await response.text();
        }
        
        if (!response.ok) {
            throw {
                status: response.status,
                statusText: response.statusText,
                data: data
            };
        }
        
        return {
            success: true,
            status: response.status,
            data: data
        };
    }

    /**
     * Handle error
     */
    handleError(error) {
        console.error('AJAX Error:', error);
        
        return {
            success: false,
            error: error.data?.error || error.statusText || 'Request failed',
            status: error.status || 500,
            details: error.data?.details || null
        };
    }

    /**
     * Set custom header
     */
    setHeader(key, value) {
        this.defaultHeaders[key] = value;
    }

    /**
     * Remove header
     */
    removeHeader(key) {
        delete this.defaultHeaders[key];
    }
}

// Create global instance
const ajax = new AjaxHandler();

// Export for use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { AjaxHandler, ajax };
}