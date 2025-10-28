/* ============================================
   ANALYSIS SIMULATOR
   Simulates the AI analysis process
   ============================================ */

class AnalysisSimulator {
    constructor() {
        this.stages = {
            voice: document.getElementById('voice-analysis'),
            image: document.getElementById('image-analysis'),
            text: document.getElementById('text-analysis'),
        };
        
        this.results = {
            voice: null,
            image: null,
            text: null,
        };
        
        this.uploadedFiles = null;
    }
    
    startAnalysis(files) {
        this.uploadedFiles = files;
        this.results = { voice: null, image: null, text: null };
        
        // Reset all stages
        this.resetStages();
        
        // Start sequential analysis
        this.analyzeSequentially();
    }
    
    resetStages() {
        Object.keys(this.stages).forEach(type => {
            const stage = this.stages[type];
            if (stage) {
                stage.className = 'analysis-stage waiting';
                this.updateStageStatus(type, 'Waiting...', 'schedule');
                this.updateProgress(type, 0);
            }
        });
    }
    
    async analyzeSequentially() {
        // Analyze voice first
        const voiceResult = await this.analyzeStage('voice');
        
        if (!voiceResult.isAuthentic) {
            // If voice fails, stop here and show results
            this.completeAnalysis();
            return;
        }
        
        // Analyze image second
        const imageResult = await this.analyzeStage('image');
        
        if (!imageResult.isAuthentic) {
            // If image fails, stop here and show results
            this.completeAnalysis();
            return;
        }
        
        // Analyze text last
        await this.analyzeStage('text');
        
        // All done
        this.completeAnalysis();
    }
    
    async analyzeStage(type) {
        const stage = this.stages[type];
        const config = APP_CONFIG.analysis;
        const messages = config.messages[type];
        const analysisTime = config[`${type}AnalysisTime`];
        
        // Set to processing state
        stage.className = 'analysis-stage processing';
        
        // Simulate analysis with progressive updates
        const steps = messages.length;
        const timePerStep = analysisTime / steps;
        
        for (let i = 0; i < steps; i++) {
            this.updateStageStatus(type, messages[i], 'autorenew');
            this.updateProgress(type, ((i + 1) / steps) * 100);
            await this.delay(timePerStep);
        }
        
        // Generate result (or use mock API)
        const result = APP_CONFIG.api.useMockAPI 
            ? this.generateMockResult(type)
            : await this.callRealAPI(type);
        
        this.results[type] = result;
        
        // Update stage based on result
        if (result.isAuthentic) {
            stage.className = 'analysis-stage completed';
            this.updateStageStatus(type, 'Analysis complete - Authentic', 'check_circle');
            this.updateProgress(type, 100);
        } else {
            stage.className = 'analysis-stage failed';
            this.updateStageStatus(type, 'Analysis complete - Issues detected', 'error');
            this.updateProgress(type, 100);
        }
        
        return result;
    }
    
    updateStageStatus(type, message, icon) {
        const stage = this.stages[type];
        if (!stage) return;
        
        const statusElement = stage.querySelector('.stage-status');
        const indicatorElement = stage.querySelector('.stage-indicator .material-icons');
        
        if (statusElement) {
            statusElement.textContent = message;
        }
        
        if (indicatorElement) {
            indicatorElement.textContent = icon;
        }
    }
    
    updateProgress(type, percentage) {
        const stage = this.stages[type];
        if (!stage) return;
        
        const progressFill = stage.querySelector('.progress-fill');
        if (progressFill) {
            progressFill.style.width = `${percentage}%`;
        }
    }
    
    generateMockResult(type) {
        // Generate realistic mock results
        // You can customize this to generate different scenarios
        
        const confidence = Math.random() * 100;
        const thresholds = APP_CONFIG.analysis.thresholds;
        
        let status;
        if (confidence >= thresholds.authentic) {
            status = 'authentic';
        } else if (confidence >= thresholds.suspicious) {
            status = 'suspicious';
        } else {
            status = 'fraudulent';
        }
        
        const isAuthentic = status === 'authentic' || status === 'suspicious';
        
        // Generate specific indicators based on type
        const indicators = this.generateIndicators(type, status);
        
        return {
            type,
            confidence: Math.round(confidence),
            status,
            isAuthentic,
            indicators,
            timestamp: new Date().toISOString(),
        };
    }
    
    generateIndicators(type, status) {
        const allIndicators = {
            voice: {
                authentic: [
                    'Natural speech patterns detected',
                    'Consistent acoustic signatures',
                    'No signs of voice synthesis',
                    'Background noise matches recording environment',
                ],
                suspicious: [
                    'Minor inconsistencies in speech patterns',
                    'Slight audio quality variations detected',
                    'Possible editing in some segments',
                ],
                fraudulent: [
                    'Synthetic voice characteristics detected',
                    'Multiple audio sources identified',
                    'Evidence of deepfake technology',
                    'Unnatural prosody patterns',
                ],
            },
            image: {
                authentic: [
                    'Metadata consistent with capture device',
                    'No pixel-level manipulation detected',
                    'Natural lighting and shadows',
                    'EXIF data verified',
                ],
                suspicious: [
                    'Minor metadata inconsistencies',
                    'Image may have been edited',
                    'Some compression artifacts detected',
                ],
                fraudulent: [
                    'Clear evidence of photo manipulation',
                    'Metadata tampered or missing',
                    'Inconsistent lighting patterns',
                    'Copy-paste regions detected',
                ],
            },
            text: {
                authentic: [
                    'Consistent writing style throughout',
                    'Natural language patterns',
                    'Details align with timeline',
                    'No contradictions found',
                ],
                suspicious: [
                    'Some inconsistencies in narrative',
                    'Unusual phrasing in certain sections',
                    'Timeline gaps detected',
                ],
                fraudulent: [
                    'Multiple writing styles detected',
                    'Fabricated details identified',
                    'Contradictory information found',
                    'AI-generated content signatures',
                ],
            },
        };
        
        return allIndicators[type][status] || [];
    }
    
    async callRealAPI(type) {
        // This function would call your actual backend API
        // Replace this with your real API integration
        
        try {
            const formData = new FormData();
            formData.append(type, this.uploadedFiles[type]);
            
            const response = await fetch(
                `${APP_CONFIG.api.baseUrl}${APP_CONFIG.api.endpoints.submitClaim}`,
                {
                    method: 'POST',
                    body: formData,
                }
            );
            
            if (!response.ok) {
                throw new Error('API request failed');
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('API call failed:', error);
            // Fall back to mock data if API fails
            return this.generateMockResult(type);
        }
    }
    
    completeAnalysis() {
        // Wait a moment before showing results
        setTimeout(() => {
            window.pageNavigation.navigateTo('results');
            if (window.resultsRenderer) {
                window.resultsRenderer.displayResults(this.results);
            }
        }, 1000);
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    getResults() {
        return this.results;
    }
}

// Initialize analysis simulator when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.analysisSimulator = new AnalysisSimulator();
    });
} else {
    window.analysisSimulator = new AnalysisSimulator();
}
