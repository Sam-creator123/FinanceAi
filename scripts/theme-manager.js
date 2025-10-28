/* ============================================
   THEME MANAGER
   Handles theme switching and color customization
   ============================================ */

class ThemeManager {
    constructor() {
        this.themeToggle = document.getElementById('theme-toggle');
        this.colorPickerToggle = document.getElementById('color-picker-toggle');
        this.colorPickerMenu = document.getElementById('color-picker-menu');
        this.colorOptions = document.querySelectorAll('.color-option');
        
        this.currentTheme = this.loadTheme();
        this.currentAccent = this.loadAccentColor();
        
        this.init();
    }
    
    init() {
        // Apply saved theme and accent
        this.applyTheme(this.currentTheme);
        this.applyAccentColor(this.currentAccent);
        
        // Set up event listeners
        this.themeToggle.addEventListener('click', () => this.toggleTheme());
        this.colorPickerToggle.addEventListener('click', (e) => this.toggleColorPicker(e));
        
        this.colorOptions.forEach(option => {
            option.addEventListener('click', () => {
                const color = option.dataset.color;
                this.changeAccentColor(color);
            });
        });
        
        // Close color picker when clicking outside
        document.addEventListener('click', (e) => {
            if (!this.colorPickerToggle.contains(e.target) && 
                !this.colorPickerMenu.contains(e.target)) {
                this.closeColorPicker();
            }
        });
        
        this.updateActiveColorOption();
    }
    
    toggleTheme() {
        this.currentTheme = this.currentTheme === 'dark' ? 'light' : 'dark';
        this.applyTheme(this.currentTheme);
        this.saveTheme(this.currentTheme);
    }
    
    applyTheme(theme) {
        if (theme === 'light') {
            document.body.classList.add('light-theme');
            this.themeToggle.querySelector('.material-icons').textContent = 'light_mode';
        } else {
            document.body.classList.remove('light-theme');
            this.themeToggle.querySelector('.material-icons').textContent = 'dark_mode';
        }
    }
    
    toggleColorPicker(e) {
        e.stopPropagation();
        this.colorPickerMenu.classList.toggle('hidden');
    }
    
    closeColorPicker() {
        this.colorPickerMenu.classList.add('hidden');
    }
    
    changeAccentColor(color) {
        this.currentAccent = color;
        this.applyAccentColor(color);
        this.saveAccentColor(color);
        this.updateActiveColorOption();
        this.closeColorPicker();
    }
    
    applyAccentColor(color) {
        document.body.setAttribute('data-accent', color);
    }
    
    updateActiveColorOption() {
        this.colorOptions.forEach(option => {
            if (option.dataset.color === this.currentAccent) {
                option.classList.add('active');
            } else {
                option.classList.remove('active');
            }
        });
    }
    
    saveTheme(theme) {
        localStorage.setItem('insureGuard-theme', theme);
    }
    
    loadTheme() {
        const saved = localStorage.getItem('insureGuard-theme');
        return saved || APP_CONFIG.theme.defaultTheme;
    }
    
    saveAccentColor(color) {
        localStorage.setItem('insureGuard-accent', color);
    }
    
    loadAccentColor() {
        const saved = localStorage.getItem('insureGuard-accent');
        return saved || APP_CONFIG.theme.defaultAccentColor;
    }
}

// Initialize theme manager when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.themeManager = new ThemeManager();
    });
} else {
    window.themeManager = new ThemeManager();
}
