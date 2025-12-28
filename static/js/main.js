/**
 * Blog Application Platform - Main JavaScript
 * 
 * Progressive enhancement for forms, async operations, and user feedback.
 */

(function() {
  'use strict';

  // ============================================
  // UTILITY FUNCTIONS
  // ============================================

  /**
   * Create and display a message to the user
   * @param {string} message - The message text
   * @param {string} type - Message type: 'success', 'error', 'info', 'warning'
   */
  function showMessage(message, type = 'info') {
    const messageEl = document.createElement('div');
    messageEl.className = `message message-${type}`;
    messageEl.textContent = message;
    messageEl.setAttribute('role', 'alert');
    
    document.body.appendChild(messageEl);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
      messageEl.remove();
    }, 5000);
  }

  /**
   * Show loading indicator
   * @param {HTMLElement} element - Element to show loading on
   */
  function showLoading(element) {
    element.classList.add('loading');
    element.disabled = true;
  }

  /**
   * Hide loading indicator
   * @param {HTMLElement} element - Element to hide loading on
   */
  function hideLoading(element) {
    element.classList.remove('loading');
    element.disabled = false;
  }

  // ============================================
  // FORM VALIDATION
  // ============================================

  /**
   * Validate form fields client-side
   * @param {HTMLFormElement} form - The form to validate
   * @returns {boolean} - Whether the form is valid
   */
  function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    let isValid = true;

    inputs.forEach(input => {
      if (!input.value.trim()) {
        showFieldError(input, 'This field is required');
        isValid = false;
      } else {
        clearFieldError(input);
      }
    });

    return isValid;
  }

  /**
   * Show error message for a form field
   * @param {HTMLInputElement} input - The input element
   * @param {string} message - Error message
   */
  function showFieldError(input, message) {
    clearFieldError(input);
    
    const errorEl = document.createElement('div');
    errorEl.className = 'field-error';
    errorEl.textContent = message;
    errorEl.setAttribute('role', 'alert');
    
    input.classList.add('error');
    input.parentElement.appendChild(errorEl);
  }

  /**
   * Clear error message for a form field
   * @param {HTMLInputElement} input - The input element
   */
  function clearFieldError(input) {
    input.classList.remove('error');
    const errorEl = input.parentElement.querySelector('.field-error');
    if (errorEl) {
      errorEl.remove();
    }
  }

  // ============================================
  // API HELPERS
  // ============================================

  /**
   * Make an API request with proper error handling
   * @param {string} url - API endpoint URL
   * @param {object} options - Fetch options
   * @returns {Promise} - Response data or error
   */
  async function apiRequest(url, options = {}) {
    const defaultOptions = {
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const mergedOptions = { ...defaultOptions, ...options };

    try {
      const response = await fetch(url, mergedOptions);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'An error occurred');
      }

      return data;
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // ============================================
  // INITIALIZATION
  // ============================================

  document.addEventListener('DOMContentLoaded', function() {
    console.log('Blog Application initialized');

    // Add form validation to all forms
    const forms = document.querySelectorAll('form[data-validate]');
    forms.forEach(form => {
      form.addEventListener('submit', function(e) {
        if (!validateForm(form)) {
          e.preventDefault();
        }
      });
    });
  });

  // Export to global scope for use in templates
  window.blogApp = {
    showMessage,
    showLoading,
    hideLoading,
    validateForm,
    apiRequest,
  };
})();

