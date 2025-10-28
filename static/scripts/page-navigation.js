/* ============================================
   PAGE NAVIGATION
   Handles navigation between different pages
   ============================================ */

class PageNavigation {
    constructor() {
        this.pages = {
            landing: document.getElementById('landing-page'),
            submission: document.getElementById('submission-page'),
            loading: document.getElementById('loading-page'),
            results: document.getElementById('results-page'),
        };
        
        this.currentPage = 'landing';
        this.init();
    }
    
    init() {
        // Landing page buttons
        const startClaimBtn = document.getElementById('start-claim-btn');
        if (startClaimBtn) {
            startClaimBtn.addEventListener('click', () => this.navigateTo('submission'));
        }
        
        // Submission page buttons
        const backToHomeBtn = document.getElementById('back-to-home');
        if (backToHomeBtn) {
            backToHomeBtn.addEventListener('click', () => this.navigateTo('landing'));
        }
        
        // Results page buttons
        const newClaimBtn = document.getElementById('new-claim-btn');
        if (newClaimBtn) {
            newClaimBtn.addEventListener('click', () => {
                this.resetSubmission();
                this.navigateTo('submission');
            });
        }
    }
    
    navigateTo(pageName) {
        // Validate page name
        if (!this.pages[pageName]) {
            console.error(`Page "${pageName}" not found`);
            return;
        }
        
        // Hide current page
        if (this.pages[this.currentPage]) {
            this.pages[this.currentPage].classList.remove('active');
        }
        
        // Show new page
        this.pages[pageName].classList.add('active');
        this.currentPage = pageName;
        
        // Scroll to top if configured
        if (APP_CONFIG.ui.autoScrollToTop) {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        
        // Trigger custom event for other scripts to listen to
        this.dispatchNavigationEvent(pageName);
    }
    
    dispatchNavigationEvent(pageName) {
        const event = new CustomEvent('pageChange', {
            detail: {
                page: pageName,
                timestamp: new Date().toISOString()
            }
        });
        document.dispatchEvent(event);
    }
    
    getCurrentPage() {
        return this.currentPage;
    }
    
    resetSubmission() {
        // This will be called by file upload handler to reset the form
        const event = new CustomEvent('resetSubmission');
        document.dispatchEvent(event);
    }
}

// Initialize page navigation when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.pageNavigation = new PageNavigation();
    });
} else {
    window.pageNavigation = new PageNavigation();
}
