/* ============================================
   RESULTS RENDERER
   Displays the analysis results
   ============================================ */

class ResultsRenderer {
    constructor() {
        this.overallScoreCard = document.getElementById('overall-score');
        this.voiceResult = document.getElementById('voice-result');
        this.imageResult = document.getElementById('image-result');
        this.textResult = document.getElementById('text-result');
        this.analysisDate = document.getElementById('analysis-date');
        this.downloadBtn = document.getElementById('download-report-btn');
        
        this.init();
    }
    
    init() {
        if (this.downloadBtn) {
            this.downloadBtn.addEventListener('click', () => this.downloadReport());
        }
    }
    
    displayResults(results) {
        // Set analysis date
        if (this.analysisDate) {
            const now = new Date();
            this.analysisDate.textContent = now.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        }
        
        // Calculate overall score
        const overallScore = this.calculateOverallScore(results);
        
        // Display overall score
        this.displayOverallScore(overallScore);
        
        // Display individual results
        this.displayIndividualResult('voice', results.voice);
        this.displayIndividualResult('image', results.image);
        this.displayIndividualResult('text', results.text);
    }
    
    calculateOverallScore(results) {
        const values = Object.values(results).filter(r => r !== null);
        
        if (values.length === 0) {
            return { confidence: 0, status: 'fraudulent' };
        }
        
        const avgConfidence = values.reduce((sum, r) => sum + r.confidence, 0) / values.length;
        const thresholds = APP_CONFIG.analysis.thresholds;
        
        let status;
        if (avgConfidence >= thresholds.authentic) {
            status = 'authentic';
        } else if (avgConfidence >= thresholds.suspicious) {
            status = 'suspicious';
        } else {
            status = 'fraudulent';
        }
        
        return {
            confidence: Math.round(avgConfidence),
            status,
            details: values
        };
    }
    
    displayOverallScore(overallScore) {
        if (!this.overallScoreCard) return;
        
        const statusLabels = {
            authentic: 'Likely Authentic',
            suspicious: 'Requires Review',
            fraudulent: 'High Risk'
        };
        
        const statusDescriptions = {
            authentic: 'All submitted materials passed authenticity verification',
            suspicious: 'Some inconsistencies detected - manual review recommended',
            fraudulent: 'Significant fraud indicators detected'
        };
        
        // Create SVG circle
        const radius = 90;
        const circumference = 2 * Math.PI * radius;
        const offset = circumference - (overallScore.confidence / 100) * circumference;
        
        this.overallScoreCard.innerHTML = `
            <div class="score-header">
                <h2>Overall Assessment</h2>
                <p class="score-label">${statusDescriptions[overallScore.status]}</p>
            </div>
            <div class="score-circle-container">
                <div class="score-circle">
                    <svg viewBox="0 0 200 200">
                        <circle class="score-circle-bg" cx="100" cy="100" r="${radius}"></circle>
                        <circle 
                            class="score-circle-fill" 
                            cx="100" 
                            cy="100" 
                            r="${radius}"
                            stroke-dasharray="${circumference}"
                            stroke-dashoffset="${offset}"
                        ></circle>
                    </svg>
                    <div class="score-text">
                        <div class="score-percentage">${overallScore.confidence}%</div>
                        <div class="score-description">Confidence</div>
                    </div>
                </div>
            </div>
            <div class="overall-status ${overallScore.status}">
                ${statusLabels[overallScore.status]}
            </div>
        `;
        
        // Animate the circle
        setTimeout(() => {
            const circle = this.overallScoreCard.querySelector('.score-circle-fill');
            if (circle) {
                circle.style.strokeDashoffset = offset;
            }
        }, 100);
    }
    
    displayIndividualResult(type, result) {
        const container = this[`${type}Result`];
        if (!container || !result) return;
        
        const contentDiv = container.querySelector('.result-content');
        if (!contentDiv) return;
        
        const statusLabels = {
            authentic: 'Authentic',
            suspicious: 'Suspicious',
            fraudulent: 'Fraudulent'
        };
        
        // Add status class to card
        container.classList.add(result.status);
        
        // Build indicators HTML
        const indicatorsHTML = result.indicators && result.indicators.length > 0
            ? `
                <div class="result-row">
                    <div class="result-label">Key Findings:</div>
                </div>
                <ul class="indicators-list">
                    ${result.indicators.map(indicator => `<li>${indicator}</li>`).join('')}
                </ul>
            `
            : '';
        
        contentDiv.innerHTML = `
            <div class="result-row">
                <span class="result-label">Status</span>
                <span class="result-value status-badge ${result.status}">${statusLabels[result.status]}</span>
            </div>
            <div class="confidence-bar-container">
                <div class="confidence-label">
                    <span>Confidence Score</span>
                    <span>${result.confidence}%</span>
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill ${result.status}" style="width: 0%"></div>
                </div>
            </div>
            ${indicatorsHTML}
        `;
        
        // Animate confidence bar
        setTimeout(() => {
            const fill = contentDiv.querySelector('.confidence-fill');
            if (fill) {
                fill.style.width = `${result.confidence}%`;
            }
        }, 200);
    }
    
    downloadReport() {
        const results = window.analysisSimulator?.getResults();
        if (!results) {
            alert('No results available to download');
            return;
        }
        
        const overallScore = this.calculateOverallScore(results);
        
        // Create a formatted report
        const report = this.generateReportText(results, overallScore);
        
        // Create blob and download
        const blob = new Blob([report], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `InsureGuard-Report-${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
    
    generateReportText(results, overallScore) {
        const date = new Date().toLocaleString();
        
        let report = `INSUREGUARD AI - AUTHENTICITY REPORT
${'='.repeat(60)}

Generated: ${date}
Report ID: ${this.generateReportId()}

OVERALL ASSESSMENT
${'-'.repeat(60)}
Confidence Score: ${overallScore.confidence}%
Status: ${overallScore.status.toUpperCase()}

`;
        
        // Add individual results
        Object.keys(results).forEach(type => {
            const result = results[type];
            if (result) {
                report += `
${type.toUpperCase()} ANALYSIS
${'-'.repeat(60)}
Status: ${result.status.toUpperCase()}
Confidence: ${result.confidence}%

Key Findings:
${result.indicators.map(ind => `  • ${ind}`).join('\n')}

`;
            }
        });
        
        report += `
${'='.repeat(60)}
DISCLAIMER: This report is generated by AI and should be used 
as one factor in decision-making, not as the sole determinant.
Manual review is recommended for all claims.
`;
        
        return report;
    }
    
    generateReportId() {
        return 'IG-' + Date.now().toString(36).toUpperCase() + '-' + Math.random().toString(36).substr(2, 5).toUpperCase();
    }
}

// Initialize results renderer when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.resultsRenderer = new ResultsRenderer();
    });
} else {
    window.resultsRenderer = new ResultsRenderer();
}
