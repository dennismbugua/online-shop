// JavaScript to fix Django admin product list width issues
document.addEventListener('DOMContentLoaded', function() {
    // Only adjust small behavioral niceties; leave sizing to CSS
    if (!(document.body.classList.contains('app-shop') &&
          document.body.classList.contains('model-product'))) return;

    // Example: ensure results container can scroll horizontally if needed
    const results = document.querySelector('#changelist .results');
    if (results) {
        results.style.overflowX = results.style.overflowX || 'auto';
    }
});
