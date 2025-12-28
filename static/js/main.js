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
   * Validate registration form
   * @param {HTMLFormElement} form - The registration form
   * @returns {boolean} - Whether the form is valid
   */
  function validateRegistrationForm(form) {
    let isValid = true;
    
    const username = form.querySelector('#username');
    const email = form.querySelector('#email');
    const password = form.querySelector('#password');
    
    // Validate username
    if (!username.value.trim()) {
      showFieldError(username, 'Username is required');
      isValid = false;
    } else if (username.value.length < 3 || username.value.length > 30) {
      showFieldError(username, 'Username must be 3-30 characters');
      isValid = false;
    } else if (!/^[a-zA-Z0-9_]+$/.test(username.value)) {
      showFieldError(username, 'Username can only contain letters, numbers, and underscores');
      isValid = false;
    } else {
      clearFieldError(username);
    }
    
    // Validate email
    if (!email.value.trim()) {
      showFieldError(email, 'Email is required');
      isValid = false;
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
      showFieldError(email, 'Please enter a valid email address');
      isValid = false;
    } else {
      clearFieldError(email);
    }
    
    // Validate password
    if (!password.value.trim()) {
      showFieldError(password, 'Password is required');
      isValid = false;
    } else if (password.value.length < 8) {
      showFieldError(password, 'Password must be at least 8 characters');
      isValid = false;
    } else {
      clearFieldError(password);
    }
    
    return isValid;
  }

  /**
   * Validate login form
   * @param {HTMLFormElement} form - The login form
   * @returns {boolean} - Whether the form is valid
   */
  function validateLoginForm(form) {
    let isValid = true;
    
    const username = form.querySelector('#username');
    const password = form.querySelector('#password');
    
    if (!username.value.trim()) {
      showFieldError(username, 'Username is required');
      isValid = false;
    } else {
      clearFieldError(username);
    }
    
    if (!password.value.trim()) {
      showFieldError(password, 'Password is required');
      isValid = false;
    } else {
      clearFieldError(password);
    }
    
    return isValid;
  }

  /**
   * Show error message for a form field
   * @param {HTMLInputElement} input - The input element
   * @param {string} message - Error message
   */
  function showFieldError(input, message) {
    const errorId = input.getAttribute('aria-describedby');
    const errorSpan = document.getElementById(errorId.split(' ').find(id => id.endsWith('-error')));
    
    if (errorSpan) {
      errorSpan.textContent = message;
      errorSpan.hidden = false;
    }
    
    input.classList.add('error');
    input.setAttribute('aria-invalid', 'true');
  }

  /**
   * Clear error message for a form field
   * @param {HTMLInputElement} input - The input element
   */
  function clearFieldError(input) {
    const errorId = input.getAttribute('aria-describedby');
    if (errorId) {
      const errorSpan = document.getElementById(errorId.split(' ').find(id => id.endsWith('-error')));
      if (errorSpan) {
        errorSpan.textContent = '';
        errorSpan.hidden = true;
      }
    }
    
    input.classList.remove('error');
    input.removeAttribute('aria-invalid');
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
  // FORM HANDLERS
  // ============================================

  /**
   * Handle registration form submission
   * @param {Event} e - Submit event
   */
  async function handleRegistrationSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const messageEl = form.querySelector('#form-message');
    
    // Client-side validation
    if (!validateRegistrationForm(form)) {
      return;
    }
    
    // Show loading state
    showLoading(submitBtn);
    
    try {
      const formData = new FormData(form);
      const data = {
        username: formData.get('username'),
        email: formData.get('email'),
        password: formData.get('password'),
      };
      
      await apiRequest('/api/auth/register', {
        method: 'POST',
        body: JSON.stringify(data),
      });
      
      // Success - redirect to home
      showMessage('Registration successful! Redirecting...', 'success');
      setTimeout(() => {
        window.location.href = '/';
      }, 1000);
      
    } catch (error) {
      // Show error message
      messageEl.textContent = error.message || 'Registration failed. Please try again.';
      messageEl.className = 'form-message error';
      messageEl.hidden = false;
    } finally {
      hideLoading(submitBtn);
    }
  }

  /**
   * Handle login form submission
   * @param {Event} e - Submit event
   */
  async function handleLoginSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const messageEl = form.querySelector('#form-message');
    
    // Client-side validation
    if (!validateLoginForm(form)) {
      return;
    }
    
    // Show loading state
    showLoading(submitBtn);
    
    try {
      const formData = new FormData(form);
      const data = {
        username: formData.get('username'),
        password: formData.get('password'),
      };
      
      await apiRequest('/api/auth/login', {
        method: 'POST',
        body: JSON.stringify(data),
      });
      
      // Success - redirect to home
      showMessage('Login successful! Redirecting...', 'success');
      setTimeout(() => {
        window.location.href = '/';
      }, 1000);
      
    } catch (error) {
      // Show error message
      messageEl.textContent = error.message || 'Login failed. Please check your credentials.';
      messageEl.className = 'form-message error';
      messageEl.hidden = false;
    } finally {
      hideLoading(submitBtn);
    }
  }

  // ============================================
  // INITIALIZATION
  // ============================================

  /**
   * Initialize registration form
   */
  function initRegisterForm() {
    const form = document.getElementById('register-form');
    if (form) {
      form.addEventListener('submit', handleRegistrationSubmit);
      
      // Add real-time validation on blur
      const inputs = form.querySelectorAll('input');
      inputs.forEach(input => {
        input.addEventListener('blur', () => {
          if (input.value.trim()) {
            validateRegistrationForm(form);
          }
        });
      });
    }
  }

  /**
   * Initialize login form
   */
  function initLoginForm() {
    const form = document.getElementById('login-form');
    if (form) {
      form.addEventListener('submit', handleLoginSubmit);
      
      // Add real-time validation on blur
      const inputs = form.querySelectorAll('input');
      inputs.forEach(input => {
        input.addEventListener('blur', () => {
          if (input.value.trim()) {
            validateLoginForm(form);
          }
        });
      });
    }
  }

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

  window.FormValidation = {
    initRegisterForm,
    initLoginForm,
  };
})();

