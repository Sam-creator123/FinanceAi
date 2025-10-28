/* ============================================
   MAIN APPLICATION
   Initializes the application and handles global functions
   ============================================ */

class Application {
    constructor() {
        this.initialized = false;
        this.init();
    }
    
    init() {
        if (this.initialized) return;
        
        console.log(`${APP_CONFIG.appName} v${APP_CONFIG.appVersion} initialized`);
        
        // Populate landing page features
        this.populateFeatures();
        
        // Set up smooth scrolling for navigation links
        this.setupSmoothScrolling();
        
        // Listen for page changes
        document.addEventListener('pageChange', (e) => {
            this.handlePageChange(e.detail);
        });
        
        this.initialized = true;
    }
    
    populateFeatures() {
        const featuresContainer = document.getElementById('features-container');
        if (!featuresContainer) return;
        
        // Clear existing content
        featuresContainer.innerHTML = '';
        
        // Add features from config
        FEATURES_CONFIG.forEach(feature => {
            const featureCard = this.createFeatureCard(feature);
            featuresContainer.appendChild(featureCard);
        });
    }
    
    createFeatureCard(feature) {
        const card = document.createElement('div');
        card.className = 'feature-card';
        card.setAttribute('data-feature-id', feature.id);
        
        card.innerHTML = `
            <div class="feature-icon">
                <span class="material-icons">${feature.icon}</span>
            </div>
            <h3>${feature.title}</h3>
            <p>${feature.description}</p>
        `;
        
        // Add click animation
        card.addEventListener('click', () => {
            card.style.transform = 'scale(0.95)';
            setTimeout(() => {
                card.style.transform = '';
            }, 200);
        });
        
        return card;
    }
    
    setupSmoothScrolling() {
        const navLinks = document.querySelectorAll('.nav-links a');
        
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                const href = link.getAttribute('href');
                
                // Only handle anchor links
                if (href && href.startsWith('#')) {
                    e.preventDefault();
                    const targetId = href.substring(1);
                    const targetElement = document.getElementById(targetId);
                    
                    if (targetElement) {
                        targetElement.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                }
            });
        });
    }
    
    handlePageChange(detail) {
        console.log(`Navigated to: ${detail.page} at ${detail.timestamp}`);
        
        // You can add page-specific logic here
        // For example, analytics tracking, page-specific initialization, etc.
    }
    
    // Utility function to show notifications (if you want to add this feature)
    showNotification(message, type = 'info') {
        if (!APP_CONFIG.ui.showNotifications) return;
        
        // You can implement a toast notification system here
        console.log(`[${type.toUpperCase()}] ${message}`);
    }
}

// Initialize the application when DOM is fully loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.app = new Application();
    });
} else {
    window.app = new Application();
}

// Global error handler (optional but recommended)
window.addEventListener('error', (event) => {
    console.error('Global error caught:', event.error);
    // You could send this to an error tracking service
});

// Global unhandled promise rejection handler (optional but recommended)
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    // You could send this to an error tracking service
});
