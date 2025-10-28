/* ============================================
   FILE UPLOAD HANDLER
   Manages file uploads and validation
   ============================================ */

class FileUploadHandler {
    constructor() {
        this.uploadedFiles = {
            voice: null,
            image: null,
            text: null,
        };
        
        this.inputs = {
            voice: document.getElementById('voice-input'),
            image: document.getElementById('image-input'),
            text: document.getElementById('text-input'),
        };
        
        this.cards = {
            voice: document.getElementById('voice-upload-card'),
            image: document.getElementById('image-upload-card'),
            text: document.getElementById('text-upload-card'),
        };
        
        this.statuses = {
            voice: document.getElementById('voice-status'),
            image: document.getElementById('image-status'),
            text: document.getElementById('text-status'),
        };
        
        this.termsCheckbox = document.getElementById('terms-checkbox');
        this.submitButton = document.getElementById('submit-claim-btn');
        
        this.init();
    }
    
    init() {
        // Set up file input listeners
        Object.keys(this.inputs).forEach(type => {
            if (this.inputs[type]) {
                this.inputs[type].addEventListener('change', (e) => {
                    this.handleFileUpload(type, e.target.files[0]);
                });
            }
        });
        
        // Terms checkbox listener
        if (this.termsCheckbox) {
            this.termsCheckbox.addEventListener('change', () => {
                this.updateSubmitButton();
            });
        }
        
        // Submit button listener
        if (this.submitButton) {
            this.submitButton.addEventListener('click', () => {
                this.submitClaim();
            });
        }
        
        // Listen for reset event
        document.addEventListener('resetSubmission', () => {
            this.resetForm();
        });
        
        // Terms modal handling
        this.setupTermsModal();
    }
    
    handleFileUpload(type, file) {
        if (!file) return;
        
        const config = APP_CONFIG.fileUpload[type];
        const validation = this.validateFile(file, config);
        
        if (validation.valid) {
            this.uploadedFiles[type] = file;
            this.updateFileStatus(type, 'success', `✓ ${file.name}`);
            this.cards[type].classList.add('has-file');
            this.cards[type].classList.remove('error');
        } else {
            this.uploadedFiles[type] = null;
            this.updateFileStatus(type, 'error', `✗ ${validation.error}`);
            this.cards[type].classList.add('error');
            this.cards[type].classList.remove('has-file');
            this.inputs[type].value = ''; // Clear the input
        }
        
        this.updateSubmitButton();
    }
    
    validateFile(file, config) {
        // Check file size
        if (file.size > config.maxSize) {
            return {
                valid: false,
                error: `File too large (max ${this.formatFileSize(config.maxSize)})`
            };
        }
        
        // Check file type
        const extension = '.' + file.name.split('.').pop().toLowerCase();
        const mimeType = file.type;
        
        const validExtension = config.acceptedFormats.includes(extension);
        const validMimeType = config.acceptedMimeTypes.includes(mimeType);
        
        if (!validExtension || !validMimeType) {
            return {
                valid: false,
                error: `Invalid file type. Accepted: ${config.acceptedFormats.join(', ')}`
            };
        }
        
        return { valid: true };
    }
    
    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }
    
    updateFileStatus(type, statusClass, message) {
        const status = this.statuses[type];
        if (!status) return;
        
        status.className = `file-status ${statusClass}`;
        
        if (statusClass === 'success') {
            status.innerHTML = `
                <span class="material-icons">check_circle</span>
                <span class="file-name">${message}</span>
            `;
        } else if (statusClass === 'error') {
            status.innerHTML = `
                <span class="material-icons">error</span>
                <span>${message}</span>
            `;
        } else {
            status.textContent = message;
        }
    }
    
    updateSubmitButton() {
        const allFilesUploaded = Object.values(this.uploadedFiles).every(file => file !== null);
        const termsAccepted = this.termsCheckbox && this.termsCheckbox.checked;
        
        if (allFilesUploaded && termsAccepted) {
            this.submitButton.disabled = false;
        } else {
            this.submitButton.disabled = true;
        }
    }
    
    submitClaim() {
        if (!this.submitButton.disabled) {
            // Trigger the analysis
            window.pageNavigation.navigateTo('loading');
            
            // Start analysis with uploaded files
            if (window.analysisSimulator) {
                window.analysisSimulator.startAnalysis(this.uploadedFiles);
            }
        }
    }
    
    setupTermsModal() {
        const termsLink = document.getElementById('terms-link');
        const modal = document.getElementById('terms-modal');
        const closeBtn = modal?.querySelector('.modal-close');
        const acceptBtn = modal?.querySelector('.modal-accept');
        
        if (termsLink) {
            termsLink.addEventListener('click', (e) => {
                e.preventDefault();
                modal.classList.add('active');
            });
        }
        
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                modal.classList.remove('active');
            });
        }
        
        if (acceptBtn) {
            acceptBtn.addEventListener('click', () => {
                this.termsCheckbox.checked = true;
                this.updateSubmitButton();
                modal.classList.remove('active');
            });
        }
        
        // Close modal on outside click
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    modal.classList.remove('active');
                }
            });
        }
    }
    
    resetForm() {
        // Clear uploaded files
        this.uploadedFiles = {
            voice: null,
            image: null,
            text: null,
        };
        
        // Reset inputs
        Object.values(this.inputs).forEach(input => {
            if (input) input.value = '';
        });
        
        // Reset cards
        Object.values(this.cards).forEach(card => {
            if (card) {
                card.classList.remove('has-file', 'error');
            }
        });
        
        // Reset statuses
        Object.values(this.statuses).forEach(status => {
            if (status) {
                status.className = 'file-status';
                status.textContent = '';
            }
        });
        
        // Reset checkbox
        if (this.termsCheckbox) {
            this.termsCheckbox.checked = false;
        }
        
        // Update submit button
        this.updateSubmitButton();
    }
    
    getUploadedFiles() {
        return this.uploadedFiles;
    }
}

// Initialize file upload handler when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.fileUploadHandler = new FileUploadHandler();
    });
} else {
    window.fileUploadHandler = new FileUploadHandler();
}
