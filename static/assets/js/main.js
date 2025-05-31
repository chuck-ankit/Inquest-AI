// Main JavaScript file for InquestAI

// Initialize all components when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initializeUI();
    setupFormValidation();
    setupFileUpload();
    setupAnimations();
    setupAccessibility();
});

// UI Initialization
function initializeUI() {
    // Initialize tooltips
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(tooltip => {
        new Tooltip(tooltip);
    });

    // Initialize modals
    const modals = document.querySelectorAll('[data-modal]');
    modals.forEach(modal => {
        new Modal(modal);
    });

    // Setup dark mode toggle
    setupDarkMode();
}

// Form Validation
function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (validateForm(form)) {
                await submitForm(form);
            }
        });
    });
}

function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input, textarea, select');
    
    inputs.forEach(input => {
        if (input.hasAttribute('required') && !input.value.trim()) {
            showError(input, 'This field is required');
            isValid = false;
        } else if (input.type === 'email' && !validateEmail(input.value)) {
            showError(input, 'Please enter a valid email address');
            isValid = false;
        }
    });
    
    return isValid;
}

async function submitForm(form) {
    try {
        const formData = new FormData(form);
        const response = await fetch(form.action, {
            method: form.method,
            body: formData
        });
        
        if (!response.ok) throw new Error('Form submission failed');
        
        showSuccess('Form submitted successfully!');
        form.reset();
    } catch (error) {
        showError(null, 'An error occurred. Please try again.');
        console.error('Form submission error:', error);
    }
}

// File Upload Handling
function setupFileUpload() {
    const dropZone = document.getElementById('drop-zone');
    if (!dropZone) return;

    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    dropZone.addEventListener('drop', handleDrop, false);
}

// Animations
function setupAnimations() {
    const animatedElements = document.querySelectorAll('[data-animate]');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animated');
                observer.unobserve(entry.target);
            }
        });
    });

    animatedElements.forEach(element => {
        observer.observe(element);
    });
}

// Accessibility
function setupAccessibility() {
    // Add keyboard navigation
    setupKeyboardNav();
    
    // Add ARIA labels where missing
    addAriaLabels();
    
    // Ensure proper focus management
    setupFocusManagement();
}

// Dark Mode
function setupDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (!darkModeToggle) return;

    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    document.documentElement.classList.toggle('dark-mode', isDarkMode);
    
    darkModeToggle.addEventListener('click', () => {
        document.documentElement.classList.toggle('dark-mode');
        localStorage.setItem('darkMode', 
            document.documentElement.classList.contains('dark-mode')
        );
    });
}

// Utility Functions
function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

function highlight(e) {
    this.classList.add('drag-over');
}

function unhighlight(e) {
    this.classList.remove('drag-over');
}

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function showError(element, message) {
    const errorElement = document.createElement('div');
    errorElement.className = 'error-message';
    errorElement.textContent = message;
    
    if (element) {
        element.classList.add('error');
        element.parentNode.appendChild(errorElement);
    } else {
        document.querySelector('.global-messages').appendChild(errorElement);
    }
}

function showSuccess(message) {
    const successElement = document.createElement('div');
    successElement.className = 'success-message';
    successElement.textContent = message;
    document.querySelector('.global-messages').appendChild(successElement);
    
    setTimeout(() => {
        successElement.remove();
    }, 3000);
}

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        validateForm,
        validateEmail,
        showError,
        showSuccess
    };
}