/* ============================================
   APP CONFIGURATION
   Modify these settings to customize the app
   ============================================ */

const APP_CONFIG = {
    // Application Information
    appName: 'InsureGuard AI',
    appVersion: '1.0.0',
    
    // API Configuration (Update these when integrating with your backend)
    api: {
        baseUrl: 'https://your-api-endpoint.com',
        endpoints: {
            submitClaim: '/api/analyze-claim',
            getResults: '/api/results',
        },
        // Set to false when you have a real API
        useMockAPI: true,
    },
    
    // File Upload Configuration
    fileUpload: {
        voice: {
            maxSize: 10 * 1024 * 1024, // 10MB
            acceptedFormats: ['.mp3', '.wav', '.ogg', '.m4a'],
            acceptedMimeTypes: ['audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/mp4'],
        },
        image: {
            maxSize: 5 * 1024 * 1024, // 5MB
            acceptedFormats: ['.jpg', '.jpeg', '.png', '.webp'],
            acceptedMimeTypes: ['image/jpeg', 'image/png', 'image/webp'],
        },
        text: {
            maxSize: 2 * 1024 * 1024, // 2MB
            acceptedFormats: ['.txt', '.pdf', '.doc', '.docx'],
            acceptedMimeTypes: [
                'text/plain',
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            ],
        },
    },
    
    // Analysis Configuration
    analysis: {
        // Time in milliseconds for each analysis stage (for simulation)
        voiceAnalysisTime: 3000,
        imageAnalysisTime: 3500,
        textAnalysisTime: 3000,
        
        // Messages displayed during analysis
        messages: {
            voice: [
                'Initializing voice analysis...',
                'Analyzing voice patterns...',
                'Detecting acoustic signatures...',
                'Checking for voice manipulation...',
                'Finalizing voice assessment...'
            ],
            image: [
                'Loading image data...',
                'Analyzing image metadata...',
                'Detecting image manipulation...',
                'Verifying image authenticity...',
                'Completing image analysis...'
            ],
            text: [
                'Processing text document...',
                'Analyzing writing patterns...',
                'Checking consistency...',
                'Detecting anomalies...',
                'Finalizing text verification...'
            ]
        },
        
        // Thresholds for authenticity classification
        thresholds: {
            authentic: 70,      // >= 70% is authentic
            suspicious: 40,     // 40-69% is suspicious
            fraudulent: 0,      // < 40% is fraudulent
        }
    },
    
    // Theme Configuration
    theme: {
        defaultTheme: 'dark',  // 'dark' or 'light'
        defaultAccentColor: 'blue',  // 'blue', 'purple', 'green', 'orange', 'red', 'teal'
        allowThemeChange: true,
        allowColorChange: true,
    },
    
    // Feature Flags
    features: {
        downloadReport: true,
        termsAndConditions: true,
        animatedLoading: true,
    },
    
    // UI Configuration
    ui: {
        animationSpeed: 300, // milliseconds
        showNotifications: true,
        autoScrollToTop: true,
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = APP_CONFIG;
}
