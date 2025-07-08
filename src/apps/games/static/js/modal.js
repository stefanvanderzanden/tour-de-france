// static/js/modal.js

/**
 * Modal functionality for Django HTMX forms
 */

function openModal() {
    const modal = document.getElementById('modal');
    modal.classList.remove('hidden');
    modal.classList.add('flex');

    // Focus op zoekveld zodra modal zichtbaar is
    setTimeout(() => {
        const input = document.getElementById('search-input');
        if (input) {
            input.focus();
        }
    }, 500); // Kleine vertraging om zeker te zijn dat modal klaar is

}

function closeModal() {
    const modal = document.getElementById('modal');
    const modalContent = document.getElementById('modal-content');

    modal.classList.add('hidden');
    modal.classList.remove('flex');

    // Clear the modal content
    modalContent.innerHTML = '';
}

// Initialize modal functionality when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {

    // Close modal when clicking outside
    const modal = document.getElementById('modal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });
    }

    // Handle escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const modal = document.getElementById('modal');
            if (modal && !modal.classList.contains('hidden')) {
                closeModal();
            }
        }
    });

    // HTMX event listeners
    document.body.addEventListener('closeModal', function() {
        closeModal();
    });

    document.body.addEventListener('showMessage', function() {
        // Reload the page to show the success message
        // Alternatively, you could update just the message area
        window.location.reload();
    });

    // Optional: Add animation classes for smoother transitions
    const modalElement = document.getElementById('modal');
    if (modalElement) {
        modalElement.style.transition = 'opacity 0.3s ease-in-out';
    }
});

// Optional: Advanced modal functions

/**
 * Open modal with custom content (useful for different forms)
 * @param {string} url - The URL to fetch content from
 * @param {string} targetId - The ID of the element to load content into (default: 'modal-content')
 */
function openModalWithUrl(url, targetId = 'modal-content') {
    const modal = document.getElementById('modal');

    // Show modal first
    modal.classList.remove('hidden');
    modal.classList.add('flex');

    // Then fetch content via HTMX
    htmx.ajax('GET', url, {
        target: `#${targetId}`,
        swap: 'innerHTML'
    });
}

/**
 * Show loading state in modal
 */
function showModalLoading() {
    const modalContent = document.getElementById('modal-content');
    modalContent.innerHTML = `
        <div class="p-6 text-center">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p class="mt-2 text-gray-600">Loading...</p>
        </div>
    `;
}

/**
 * Handle form submission success
 * @param {string} message - Success message to display
 */
function handleFormSuccess(message) {
    closeModal();

    // You could implement a toast notification system here
    // For now, we'll just reload the page or update a message area
    const messageArea = document.getElementById('message-area');
    if (messageArea) {
        messageArea.innerHTML = `
            <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4" role="alert">
                <span class="block sm:inline">${message}</span>
            </div>
        `;
    } else {
        // Fallback to page reload if no message area exists
        window.location.reload();
    }
}