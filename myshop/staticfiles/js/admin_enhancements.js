// Admin Dashboard Enhancement Script
(function() {
    'use strict';

    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        initializeEnhancements();
    });

    function initializeEnhancements() {
        addLoadingOverlay();
        enhanceTableInteractions();
        enhanceFormInteractions();
        addNotificationSystem();
        addKeyboardShortcuts();
        addProgressIndicators();
        enhanceNavigationAnimations();
        addParallaxEffects();
        initializeTooltips();
    }

    // Loading overlay for page transitions
    function addLoadingOverlay() {
        const overlay = document.createElement('div');
        overlay.className = 'loading-overlay';
        overlay.innerHTML = '<div class="loading-spinner"></div>';
        document.body.appendChild(overlay);

        // Show loading on form submissions and navigation
        document.addEventListener('click', function(e) {
            const target = e.target;
            if (target.type === 'submit' || target.tagName === 'A' && target.href) {
                showLoading();
            }
        });

        function showLoading() {
            overlay.classList.add('show');
            setTimeout(() => {
                overlay.classList.remove('show');
            }, 1500);
        }
    }

    // Enhanced table interactions
    function enhanceTableInteractions() {
        const tables = document.querySelectorAll('table');
        
        tables.forEach(table => {
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach((row, index) => {
                // Staggered animation entrance
                row.style.animationDelay = `${index * 0.05}s`;
                row.classList.add('table-row-animated');
                
                // Add click ripple effect
                row.addEventListener('click', function(e) {
                    createRippleEffect(e, this);
                });

                // Enhanced hover effects
                row.addEventListener('mouseenter', function() {
                    this.style.transform = 'translateX(5px)';
                    this.style.background = 'rgba(102, 126, 234, 0.1)';
                });

                row.addEventListener('mouseleave', function() {
                    this.style.transform = 'translateX(0)';
                    this.style.background = '';
                });
            });
        });
    }

    // Create ripple effect on click
    function createRippleEffect(event, element) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            pointer-events: none;
            animation: ripple 0.6s ease-out;
        `;
        
        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    // Floating Action Button
    // Enhanced form interactions
    function enhanceFormInteractions() {
        const inputs = document.querySelectorAll('input, select, textarea');
        
        inputs.forEach(input => {
            // Floating label effect
            if (input.type !== 'hidden' && input.type !== 'submit') {
                addFloatingLabel(input);
            }
            
            // Enhanced focus animations
            input.addEventListener('focus', function() {
                this.style.transform = 'scale(1.02)';
                this.style.boxShadow = '0 0 20px rgba(102, 126, 234, 0.2)';
            });
            
            input.addEventListener('blur', function() {
                this.style.transform = 'scale(1)';
                this.style.boxShadow = '';
            });
            
            // Real-time validation visual feedback
            input.addEventListener('input', function() {
                validateField(this);
            });
        });
    }

    function addFloatingLabel(input) {
        const wrapper = document.createElement('div');
        wrapper.className = 'floating-label-wrapper';
        wrapper.style.cssText = 'position: relative; margin-bottom: 1rem;';
        
        const label = input.previousElementSibling;
        if (label && label.tagName === 'LABEL') {
            label.style.cssText = `
                position: absolute;
                left: 1rem;
                top: 50%;
                transform: translateY(-50%);
                background: white;
                padding: 0 0.5rem;
                transition: all 0.3s ease;
                pointer-events: none;
                color: #6b7280;
            `;
            
            input.addEventListener('focus', () => {
                label.style.top = '0';
                label.style.fontSize = '0.75rem';
                label.style.color = '#667eea';
            });
            
            input.addEventListener('blur', () => {
                if (!input.value) {
                    label.style.top = '50%';
                    label.style.fontSize = '1rem';
                    label.style.color = '#6b7280';
                }
            });
        }
    }

    function validateField(field) {
        const isValid = field.checkValidity();
        if (isValid) {
            field.style.borderColor = '#48bb78';
            field.style.boxShadow = '0 0 0 3px rgba(72, 187, 120, 0.1)';
        } else if (field.value) {
            field.style.borderColor = '#f56565';
            field.style.boxShadow = '0 0 0 3px rgba(245, 101, 101, 0.1)';
        }
    }

    // Notification system
    function addNotificationSystem() {
        // Check for Django messages
        const messages = document.querySelectorAll('.messages li');
        messages.forEach((message, index) => {
            setTimeout(() => {
                showToast(message.textContent, getMessageType(message.className));
            }, index * 500);
        });
    }

    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span>${getToastIcon(type)}</span>
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; font-size: 1.2rem; cursor: pointer; margin-left: auto;">×</button>
            </div>
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => toast.classList.add('show'), 100);
        setTimeout(() => {
            if (toast.parentElement) {
                toast.classList.remove('show');
                setTimeout(() => toast.remove(), 300);
            }
        }, 5000);
    }

    function getToastIcon(type) {
        const icons = {
            success: '✅',
            error: '❌',
            warning: '⚠️',
            info: 'ℹ️'
        };
        return icons[type] || icons.info;
    }

    function getMessageType(className) {
        if (className.includes('success')) return 'success';
        if (className.includes('error')) return 'error';
        if (className.includes('warning')) return 'warning';
        return 'info';
    }

    // Keyboard shortcuts
    function addKeyboardShortcuts() {
        document.addEventListener('keydown', function(e) {
            // Ctrl/Cmd + S for save
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                const saveButton = document.querySelector('input[type="submit"]');
                if (saveButton) {
                    saveButton.click();
                    showToast('Saving...', 'info');
                }
            }
            
            // Escape to close modals/menus
            if (e.key === 'Escape') {
                const menu = document.querySelector('.quick-actions-menu');
                if (menu) menu.remove();
            }
            
            // Ctrl/Cmd + / for search
            if ((e.ctrlKey || e.metaKey) && e.key === '/') {
                e.preventDefault();
                const searchField = document.querySelector('input[type="search"], input[name="q"]');
                if (searchField) searchField.focus();
            }
        });
    }

    // Progress indicators for forms
    function addProgressIndicators() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            const fields = form.querySelectorAll('input:not([type="hidden"]), select, textarea');
            if (fields.length > 3) {
                addProgressBar(form, fields);
            }
        });
    }

    function addProgressBar(form, fields) {
        const progressContainer = document.createElement('div');
        progressContainer.className = 'form-progress';
        progressContainer.style.cssText = `
            position: sticky;
            top: 0;
            background: white;
            padding: 1rem;
            border-radius: 12px;
            margin-bottom: 1rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            z-index: 100;
        `;
        
        const progressBar = document.createElement('div');
        progressBar.style.cssText = `
            width: 100%;
            height: 6px;
            background: #e2e8f0;
            border-radius: 3px;
            overflow: hidden;
        `;
        
        const progressFill = document.createElement('div');
        progressFill.style.cssText = `
            height: 100%;
            background: linear-gradient(90deg, #667eea, #764ba2);
            border-radius: 3px;
            transition: width 0.3s ease;
            width: 0%;
        `;
        
        progressBar.appendChild(progressFill);
        progressContainer.appendChild(progressBar);
        form.insertBefore(progressContainer, form.firstChild);
        
        function updateProgress() {
            const filled = Array.from(fields).filter(field => field.value.trim()).length;
            const percentage = (filled / fields.length) * 100;
            progressFill.style.width = percentage + '%';
        }
        
        fields.forEach(field => {
            field.addEventListener('input', updateProgress);
        });
        
        updateProgress();
    }

    // Enhanced navigation animations
    function enhanceNavigationAnimations() {
        const navItems = document.querySelectorAll('.grp-navigation-item, .model-item');
        navItems.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.1}s`;
            item.classList.add('nav-item-animated');
        });
    }

    // Parallax effects for headers
    function addParallaxEffects() {
        const header = document.querySelector('#grp-header');
        if (header) {
            window.addEventListener('scroll', function() {
                const scrolled = window.pageYOffset;
                const rate = scrolled * -0.5;
                header.style.transform = `translateY(${rate}px)`;
            });
        }
    }

    // Tooltips for better UX
    function initializeTooltips() {
        const elements = document.querySelectorAll('[title]');
        elements.forEach(element => {
            element.addEventListener('mouseenter', showTooltip);
            element.addEventListener('mouseleave', hideTooltip);
        });
    }

    function showTooltip(e) {
        const tooltip = document.createElement('div');
        tooltip.className = 'custom-tooltip';
        tooltip.textContent = e.target.title;
        tooltip.style.cssText = `
            position: absolute;
            background: #333;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            font-size: 0.875rem;
            z-index: 1000;
            pointer-events: none;
            animation: fadeIn 0.2s ease-out;
        `;
        
        document.body.appendChild(tooltip);
        
        const rect = e.target.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
        
        e.target.setAttribute('data-original-title', e.target.title);
        e.target.removeAttribute('title');
    }

    function hideTooltip(e) {
        const tooltip = document.querySelector('.custom-tooltip');
        if (tooltip) tooltip.remove();
        
        const originalTitle = e.target.getAttribute('data-original-title');
        if (originalTitle) {
            e.target.title = originalTitle;
            e.target.removeAttribute('data-original-title');
        }
    }

    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        @keyframes slideUp {
            from {
                transform: translateY(20px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        .table-row-animated {
            animation: slideInRight 0.5s ease-out both;
        }
        
        .nav-item-animated {
            animation: slideInLeft 0.5s ease-out both;
        }
        
        .quick-action {
            padding: 0.75rem 1rem;
            cursor: pointer;
            border-radius: 8px;
            transition: background 0.2s ease;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .quick-action:hover {
            background: #f3f4f6;
        }
    `;
    document.head.appendChild(style);

})();
