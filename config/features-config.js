/* ============================================
   FEATURES CONFIGURATION
   Modify these features to update landing page content
   ============================================ */

const FEATURES_CONFIG = [
    {
        id: 'voice-analysis',
        icon: 'record_voice_over',
        title: 'Advanced Voice Analysis',
        description: 'Deep learning algorithms detect voice deepfakes, manipulation, and synthetic speech with 99.2% accuracy.',
    },
    {
        id: 'image-verification',
        icon: 'fact_check',
        title: 'Image Authenticity Verification',
        description: 'AI-powered forensic analysis identifies photo manipulation, metadata tampering, and digital forgeries.',
    },
    {
        id: 'text-authentication',
        icon: 'spellcheck',
        title: 'Text Pattern Recognition',
        description: 'Natural language processing detects inconsistencies, fabricated narratives, and suspicious claim patterns.',
    },
    {
        id: 'multimodal-fusion',
        icon: 'merge_type',
        title: 'Multimodal Fusion',
        description: 'Combines insights from voice, image, and text analysis for comprehensive fraud detection.',
    },
    {
        id: 'real-time-processing',
        icon: 'speed',
        title: 'Real-Time Processing',
        description: 'Get results in seconds with our optimized AI infrastructure and parallel processing pipeline.',
    },
    {
        id: 'explainable-ai',
        icon: 'psychology',
        title: 'Explainable AI',
        description: 'Transparent reasoning and detailed reports show exactly why each decision was made.',
    },
    {
        id: 'continuous-learning',
        icon: 'model_training',
        title: 'Continuous Learning',
        description: 'Models constantly improve by learning from new fraud patterns and emerging techniques.',
    },
    {
        id: 'compliance-ready',
        icon: 'verified',
        title: 'Compliance Ready',
        description: 'Built to meet regulatory requirements including GDPR, CCPA, and industry-specific standards.',
    },
    {
        id: 'scalable-infrastructure',
        icon: 'cloud_upload',
        title: 'Scalable Infrastructure',
        description: 'Cloud-native architecture handles thousands of concurrent analyses without performance degradation.',
    },
];

// You can easily add, remove, or modify features
// Each feature object should have: id, icon (Material Icons name), title, and description

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FEATURES_CONFIG;
}
