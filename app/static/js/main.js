// Cohortly - Enhanced UI Interactions

document.addEventListener('DOMContentLoaded', function() {
    
    // Smooth scroll to top button
    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    scrollTopBtn.className = 'fixed bottom-8 right-8 bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-4 rounded-full shadow-2xl hover:shadow-3xl transform hover:scale-110 transition-all duration-300 opacity-0 pointer-events-none z-50';
    scrollTopBtn.id = 'scrollTopBtn';
    document.body.appendChild(scrollTopBtn);
    
    // Show/hide scroll to top button
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollTopBtn.classList.remove('opacity-0', 'pointer-events-none');
            scrollTopBtn.classList.add('opacity-100');
        } else {
            scrollTopBtn.classList.add('opacity-0', 'pointer-events-none');
            scrollTopBtn.classList.remove('opacity-100');
        }
    });
    
    // Scroll to top on button click
    scrollTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('[class*="animate-slide-down"]');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-20px)';
            setTimeout(function() {
                alert.remove();
            }, 300);
        }, 5000);
    });
    
    // Add loading state to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i>Processing...';
            }
        });
    });
    
    // Add ripple effect to buttons
    document.querySelectorAll('.btn-ripple').forEach(function(button) {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = button.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple-effect');
            
            button.appendChild(ripple);
            
            setTimeout(function() {
                ripple.remove();
            }, 600);
        });
    });
    
    // Lazy load images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(function(img) {
            imageObserver.observe(img);
        });
    }
    
    // Add animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.animate-on-scroll').forEach(function(el) {
        observer.observe(el);
    });
    
    // Tooltip functionality
    document.querySelectorAll('[data-tooltip]').forEach(function(el) {
        el.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.textContent = el.getAttribute('data-tooltip');
            tooltip.className = 'absolute bg-gray-900 text-white text-xs rounded py-1 px-2 z-50 -top-8 left-1/2 transform -translate-x-1/2 whitespace-nowrap';
            el.style.position = 'relative';
            el.appendChild(tooltip);
        });
        
        el.addEventListener('mouseleave', function() {
            const tooltip = el.querySelector('.absolute');
            if (tooltip) tooltip.remove();
        });
    });
    
    // Copy to clipboard functionality
    document.querySelectorAll('[data-copy]').forEach(function(el) {
        el.addEventListener('click', function() {
            const text = el.getAttribute('data-copy');
            navigator.clipboard.writeText(text).then(function() {
                const originalHTML = el.innerHTML;
                el.innerHTML = '<i class="fas fa-check mr-2"></i>Copied!';
                setTimeout(function() {
                    el.innerHTML = originalHTML;
                }, 2000);
            });
        });
    });
    
    // Enhanced form validation feedback
    document.querySelectorAll('input, textarea, select').forEach(function(input) {
        input.addEventListener('blur', function() {
            if (this.validity.valid) {
                this.classList.remove('border-red-500');
                this.classList.add('border-green-500');
            } else if (this.value) {
                this.classList.remove('border-green-500');
                this.classList.add('border-red-500');
            }
        });
        
        input.addEventListener('input', function() {
            this.classList.remove('border-red-500', 'border-green-500');
        });
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for search (if search exists)
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="search"]');
            if (searchInput) searchInput.focus();
        }
    });
    
    // Mobile menu toggle (if needed in future)
    const mobileMenuBtn = document.querySelector('[data-mobile-menu]');
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            const menu = document.querySelector('[data-mobile-menu-content]');
            if (menu) {
                menu.classList.toggle('hidden');
            }
        });
    }
    
    // Add loading skeleton for dynamic content
    window.showLoadingSkeleton = function(container) {
        container.innerHTML = `
            <div class="skeleton-loader h-8 w-full rounded mb-4"></div>
            <div class="skeleton-loader h-8 w-3/4 rounded mb-4"></div>
            <div class="skeleton-loader h-8 w-1/2 rounded"></div>
        `;
    };
    
    // Performance: Debounce function
    window.debounce = function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = function() {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    };
    
    console.log('🚀 Cohortly UI Enhanced - Ready!');
});

// Service Worker Registration (for PWA in future)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        // navigator.serviceWorker.register('/sw.js');
    });
}
