// Advanced Admin Dashboard Interactions
(function() {
    'use strict';

    // Initialize advanced features when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        initAdvancedFeatures();
    });

    function initAdvancedFeatures() {
        setupIntersectionObserver();
        initSmoothScrolling();
        addKeyframeCSSAnimations();
        enhanceAccessibility();
        setupDragAndDrop();
        addVirtualScrolling();
        initLazyLoading();
        addShortcutBar();
        initializeSearchEnhancements();
        setupAutoSave();
        addContextMenus();
    }

    // Intersection Observer for reveal animations
    function setupIntersectionObserver() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    
                    // Add stagger effect for lists
                    if (entry.target.matches('table tbody')) {
                        const rows = entry.target.querySelectorAll('tr');
                        rows.forEach((row, index) => {
                            setTimeout(() => {
                                row.style.animationDelay = `${index * 0.05}s`;
                                row.classList.add('reveal-up', 'revealed');
                            }, index * 50);
                        });
                    }
                }
            });
        }, observerOptions);

        // Observe elements for reveal animations
        document.querySelectorAll('.grp-module, .module, table').forEach(el => {
            el.classList.add('reveal-up');
            observer.observe(el);
        });
    }

    // Enhanced smooth scrolling with easing
    function initSmoothScrolling() {
        function easeInOutCubic(t) {
            return t < 0.5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
        }

        function smoothScrollTo(targetY, duration = 800) {
            const startY = window.pageYOffset;
            const difference = targetY - startY;
            const startTime = performance.now();

            function step(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const eased = easeInOutCubic(progress);
                
                window.scrollTo(0, startY + difference * eased);
                
                if (progress < 1) {
                    requestAnimationFrame(step);
                }
            }
            
            requestAnimationFrame(step);
        }

        // Enhance anchor links
        document.addEventListener('click', function(e) {
            const link = e.target.closest('a[href^="#"]');
            if (link) {
                e.preventDefault();
                const target = document.querySelector(link.getAttribute('href'));
                if (target) {
                    smoothScrollTo(target.offsetTop - 80);
                }
            }
        });
    }

    // Dynamic CSS animations
    function addKeyframeCSSAnimations() {
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInFromBottom {
                from {
                    transform: translateY(50px);
                    opacity: 0;
                }
                to {
                    transform: translateY(0);
                    opacity: 1;
                }
            }
            
            @keyframes scaleIn {
                from {
                    transform: scale(0.8);
                    opacity: 0;
                }
                to {
                    transform: scale(1);
                    opacity: 1;
                }
            }
            
            @keyframes rotateIn {
                from {
                    transform: rotate(-180deg) scale(0);
                    opacity: 0;
                }
                to {
                    transform: rotate(0deg) scale(1);
                    opacity: 1;
                }
            }
            
            .animate-slide-in {
                animation: slideInFromBottom 0.6s ease-out both;
            }
            
            .animate-scale-in {
                animation: scaleIn 0.5s ease-out both;
            }
            
            .animate-rotate-in {
                animation: rotateIn 0.8s ease-out both;
            }
        `;
        document.head.appendChild(style);

        // Apply animations to different elements
        setTimeout(() => {
            document.querySelectorAll('.grp-button, .button').forEach(btn => {
                btn.classList.add('animate-scale-in');
            });
            
            document.querySelectorAll('h1, h2, h3').forEach((heading, index) => {
                setTimeout(() => {
                    heading.classList.add('animate-slide-in');
                }, index * 100);
            });
        }, 300);
    }

    // Enhanced accessibility features
    function enhanceAccessibility() {
        // Add skip link
        const skipLink = document.createElement('a');
        skipLink.href = '#grp-content';
        skipLink.textContent = 'Skip to main content';
        skipLink.className = 'skip-link';
        skipLink.style.cssText = `
            position: absolute;
            top: -40px;
            left: 6px;
            background: #667eea;
            color: white;
            padding: 8px;
            border-radius: 4px;
            text-decoration: none;
            z-index: 10000;
            transition: top 0.3s;
        `;
        
        skipLink.addEventListener('focus', () => {
            skipLink.style.top = '6px';
        });
        
        skipLink.addEventListener('blur', () => {
            skipLink.style.top = '-40px';
        });
        
        document.body.insertBefore(skipLink, document.body.firstChild);

        // Enhanced focus management
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                document.body.classList.add('keyboard-navigation');
            }
        });

        document.addEventListener('mousedown', function() {
            document.body.classList.remove('keyboard-navigation');
        });

        // ARIA live region for notifications
        const liveRegion = document.createElement('div');
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.style.cssText = `
            position: absolute;
            left: -10000px;
            width: 1px;
            height: 1px;
            overflow: hidden;
        `;
        document.body.appendChild(liveRegion);

        window.announceToScreenReader = function(message) {
            liveRegion.textContent = message;
            setTimeout(() => {
                liveRegion.textContent = '';
            }, 1000);
        };
    }

    // Drag and drop functionality for reordering
    function setupDragAndDrop() {
        let draggedElement = null;

        document.addEventListener('dragstart', function(e) {
            if (e.target.draggable) {
                draggedElement = e.target;
                e.target.style.opacity = '0.5';
                e.dataTransfer.effectAllowed = 'move';
            }
        });

        document.addEventListener('dragend', function(e) {
            if (e.target.draggable) {
                e.target.style.opacity = '';
                draggedElement = null;
            }
        });

        document.addEventListener('dragover', function(e) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
        });

        document.addEventListener('drop', function(e) {
            e.preventDefault();
            if (draggedElement && e.target !== draggedElement) {
                const container = e.target.closest('tbody, .grp-module');
                if (container && container.contains(draggedElement)) {
                    if (e.target.tagName === 'TR' || e.target.closest('tr')) {
                        const targetRow = e.target.closest('tr') || e.target;
                        container.insertBefore(draggedElement, targetRow.nextSibling);
                        
                        // Show success notification
                        showToast('Item reordered successfully', 'success');
                        
                        // Announce to screen readers
                        if (window.announceToScreenReader) {
                            window.announceToScreenReader('Item has been reordered');
                        }
                    }
                }
            }
        });

        // Make table rows draggable
        document.querySelectorAll('table tbody tr').forEach(row => {
            row.draggable = true;
            row.style.cursor = 'grab';
        });
    }

    // Virtual scrolling for large tables
    function addVirtualScrolling() {
        const largeTables = document.querySelectorAll('table tbody');
        
        largeTables.forEach(tbody => {
            const rows = Array.from(tbody.children);
            if (rows.length > 50) {
                implementVirtualScrolling(tbody, rows);
            }
        });
    }

    function implementVirtualScrolling(container, items) {
        const itemHeight = 50;
        const visibleItems = Math.ceil(window.innerHeight / itemHeight) + 5;
        let startIndex = 0;
        
        const virtualContainer = document.createElement('div');
        virtualContainer.style.height = `${items.length * itemHeight}px`;
        virtualContainer.style.position = 'relative';
        
        const viewport = document.createElement('div');
        viewport.style.cssText = `
            height: ${visibleItems * itemHeight}px;
            overflow-y: auto;
            position: relative;
        `;
        
        function renderVisibleItems() {
            const endIndex = Math.min(startIndex + visibleItems, items.length);
            const fragment = document.createDocumentFragment();
            
            for (let i = startIndex; i < endIndex; i++) {
                const item = items[i].cloneNode(true);
                item.style.position = 'absolute';
                item.style.top = `${i * itemHeight}px`;
                item.style.width = '100%';
                fragment.appendChild(item);
            }
            
            virtualContainer.innerHTML = '';
            virtualContainer.appendChild(fragment);
        }
        
        viewport.addEventListener('scroll', function() {
            const newStartIndex = Math.floor(this.scrollTop / itemHeight);
            if (newStartIndex !== startIndex) {
                startIndex = newStartIndex;
                renderVisibleItems();
            }
        });
        
        container.parentNode.replaceChild(viewport, container);
        viewport.appendChild(virtualContainer);
        renderVisibleItems();
    }

    // Lazy loading for images and content
    function initLazyLoading() {
        const lazyObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.classList.add('loaded');
                        lazyObserver.unobserve(img);
                    }
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            lazyObserver.observe(img);
        });
    }

    // Quick action shortcut bar
    function addShortcutBar() {
        const shortcutBar = document.createElement('div');
        shortcutBar.className = 'shortcut-bar';
        shortcutBar.style.cssText = `
            position: fixed;
            bottom: 2rem;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 50px;
            padding: 0.5rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            display: flex;
            gap: 0.5rem;
            z-index: 1000;
            transition: all 0.3s ease;
            opacity: 0;
            visibility: hidden;
        `;

        const shortcuts = [
            { icon: '➕', action: 'add', title: 'Add New (Ctrl+N)' },
            { icon: '💾', action: 'save', title: 'Save (Ctrl+S)' },
            { icon: '🔍', action: 'search', title: 'Search (Ctrl+/)' },
            { icon: '⚙️', action: 'settings', title: 'Settings' },
            { icon: '📊', action: 'stats', title: 'Statistics' }
        ];

        shortcuts.forEach(shortcut => {
            const btn = document.createElement('button');
            btn.innerHTML = shortcut.icon;
            btn.title = shortcut.title;
            btn.style.cssText = `
                background: none;
                border: none;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                font-size: 1.2rem;
                cursor: pointer;
                transition: all 0.3s ease;
                display: flex;
                align-items: center;
                justify-content: center;
            `;
            
            btn.addEventListener('click', () => executeShortcut(shortcut.action));
            btn.addEventListener('mouseenter', () => {
                btn.style.background = 'rgba(102, 126, 234, 0.1)';
                btn.style.transform = 'scale(1.1)';
            });
            btn.addEventListener('mouseleave', () => {
                btn.style.background = 'none';
                btn.style.transform = 'scale(1)';
            });
            
            shortcutBar.appendChild(btn);
        });

        document.body.appendChild(shortcutBar);

        // Show/hide shortcut bar on Alt key
        document.addEventListener('keydown', function(e) {
            if (e.altKey && !e.repeat) {
                shortcutBar.style.opacity = '1';
                shortcutBar.style.visibility = 'visible';
                shortcutBar.style.transform = 'translateX(-50%) translateY(-10px)';
            }
        });

        document.addEventListener('keyup', function(e) {
            if (!e.altKey) {
                shortcutBar.style.opacity = '0';
                shortcutBar.style.visibility = 'hidden';
                shortcutBar.style.transform = 'translateX(-50%) translateY(0)';
            }
        });
    }

    function executeShortcut(action) {
        switch (action) {
            case 'add':
                const addButton = document.querySelector('.addlink');
                if (addButton) addButton.click();
                break;
            case 'save':
                const saveButton = document.querySelector('input[type="submit"]');
                if (saveButton) saveButton.click();
                break;
            case 'search':
                const searchField = document.querySelector('input[type="search"], input[name="q"]');
                if (searchField) searchField.focus();
                break;
            case 'settings':
                showToast('Settings panel coming soon!', 'info');
                break;
            case 'stats':
                showToast('Statistics panel coming soon!', 'info');
                break;
        }
    }

    // Enhanced search functionality
    function initializeSearchEnhancements() {
        const searchInputs = document.querySelectorAll('input[type="search"], input[name="q"]');
        
        searchInputs.forEach(input => {
            // Add search suggestions
            const suggestionsContainer = document.createElement('div');
            suggestionsContainer.className = 'search-suggestions';
            suggestionsContainer.style.cssText = `
                position: absolute;
                top: 100%;
                left: 0;
                right: 0;
                background: white;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                max-height: 200px;
                overflow-y: auto;
                z-index: 1000;
                display: none;
            `;
            
            input.parentElement.style.position = 'relative';
            input.parentElement.appendChild(suggestionsContainer);
            
            // Debounced search
            let searchTimeout;
            input.addEventListener('input', function() {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    performSearch(this.value, suggestionsContainer);
                }, 300);
            });
        });
    }

    function performSearch(query, container) {
        if (query.length < 2) {
            container.style.display = 'none';
            return;
        }

        // Mock search suggestions (replace with actual search logic)
        const suggestions = [
            'Recent searches...',
            `Search for "${query}" in Products`,
            `Search for "${query}" in Orders`,
            `Search for "${query}" in Users`
        ];

        container.innerHTML = suggestions.map(suggestion => 
            `<div class="suggestion-item" style="padding: 0.75rem 1rem; cursor: pointer; border-bottom: 1px solid #e2e8f0;">${suggestion}</div>`
        ).join('');
        
        container.style.display = 'block';
        
        // Add click handlers for suggestions
        container.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', function() {
                // Handle suggestion click
                container.style.display = 'none';
                showToast(`Searching: ${this.textContent}`, 'info');
            });
        });
    }

    // Auto-save functionality
    function setupAutoSave() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, textarea, select');
            let saveTimeout;
            
            inputs.forEach(input => {
                input.addEventListener('input', function() {
                    clearTimeout(saveTimeout);
                    saveTimeout = setTimeout(() => {
                        autoSaveForm(form);
                    }, 5000); // Auto-save after 5 seconds of inactivity
                });
            });
        });
    }

    function autoSaveForm(form) {
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        // Save to localStorage as backup
        localStorage.setItem(`autosave_${form.id || 'form'}`, JSON.stringify(data));
        
        // Show auto-save indicator
        showToast('Draft saved automatically', 'success');
        
        if (window.announceToScreenReader) {
            window.announceToScreenReader('Form auto-saved');
        }
    }

    // Context menus for enhanced interactions
    function addContextMenus() {
        document.addEventListener('contextmenu', function(e) {
            const target = e.target.closest('tr, .grp-module');
            if (target) {
                e.preventDefault();
                showContextMenu(e.clientX, e.clientY, target);
            }
        });

        // Hide context menu on click elsewhere
        document.addEventListener('click', function() {
            const existingMenu = document.querySelector('.context-menu');
            if (existingMenu) {
                existingMenu.remove();
            }
        });
    }

    function showContextMenu(x, y, target) {
        const menu = document.createElement('div');
        menu.className = 'context-menu';
        menu.style.cssText = `
            position: fixed;
            top: ${y}px;
            left: ${x}px;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            z-index: 10000;
            min-width: 150px;
            animation: scaleIn 0.2s ease-out;
        `;

        const menuItems = [
            { text: 'Edit', action: () => console.log('Edit clicked') },
            { text: 'Delete', action: () => console.log('Delete clicked') },
            { text: 'Duplicate', action: () => console.log('Duplicate clicked') },
            { text: 'Export', action: () => console.log('Export clicked') }
        ];

        menuItems.forEach(item => {
            const menuItem = document.createElement('div');
            menuItem.textContent = item.text;
            menuItem.style.cssText = `
                padding: 0.75rem 1rem;
                cursor: pointer;
                transition: background 0.2s ease;
                border-bottom: 1px solid #e2e8f0;
            `;
            
            menuItem.addEventListener('click', item.action);
            menuItem.addEventListener('mouseenter', () => {
                menuItem.style.background = '#f3f4f6';
            });
            menuItem.addEventListener('mouseleave', () => {
                menuItem.style.background = 'white';
            });
            
            menu.appendChild(menuItem);
        });

        document.body.appendChild(menu);

        // Adjust position if menu goes off-screen
        const rect = menu.getBoundingClientRect();
        if (rect.right > window.innerWidth) {
            menu.style.left = (x - rect.width) + 'px';
        }
        if (rect.bottom > window.innerHeight) {
            menu.style.top = (y - rect.height) + 'px';
        }
    }

    // Utility function to show toast notifications (reused from main script)
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
        
        toast.style.cssText = `
            position: fixed;
            top: 2rem;
            right: 2rem;
            background: white;
            color: #333;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
            border-left: 4px solid ${getToastColor(type)};
            transform: translateX(100%);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 1001;
            max-width: 300px;
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => toast.style.transform = 'translateX(0)', 100);
        setTimeout(() => {
            if (toast.parentElement) {
                toast.style.transform = 'translateX(100%)';
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

    function getToastColor(type) {
        const colors = {
            success: '#48bb78',
            error: '#f56565',
            warning: '#ed8936',
            info: '#667eea'
        };
        return colors[type] || colors.info;
    }

})();
