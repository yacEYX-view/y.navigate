class YNavApp {
    constructor() {
        this.textInput = document.getElementById('textInput');
        this.contextSelect = document.getElementById('contextSelect');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        this.chatBtn = document.getElementById('chatBtn');
        this.resultDiv = document.getElementById('result');
        this.errorDiv = document.getElementById('error');
        this.loadingDiv = document.getElementById('loading');
        
        this.initEventListeners();
    }
    
    initEventListeners() {
        this.analyzeBtn.addEventListener('click', () => this.analyze());
        this.chatBtn.addEventListener('click', () => this.chat());
    }
    
    showLoading() {
        this.loadingDiv.classList.remove('hidden');
        this.resultDiv.classList.add('hidden');
        this.errorDiv.classList.add('hidden');
        this.analyzeBtn.disabled = true;
        this.chatBtn.disabled = true;
    }
    
    hideLoading() {
        this.loadingDiv.classList.add('hidden');
        this.analyzeBtn.disabled = false;
        this.chatBtn.disabled = false;
    }
    
    showError(message) {
        this.errorDiv.textContent = message;
        this.errorDiv.classList.remove('hidden');
        this.hideLoading();
    }
    
    showResult(result, riskLevel = null) {
        this.resultDiv.textContent = result;
        this.resultDiv.classList.remove('hidden');
        this.resultDiv.className = 'result';
        if (riskLevel) {
            this.resultDiv.classList.add(`risk-${riskLevel.toLowerCase()}`);
        }
        this.hideLoading();
    }
    
    async analyze() {
        const text = this.textInput.value.trim();
        if (!text) {
            this.showError('Please enter some text to analyze');
            return;
        }
        
        this.showLoading();
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    context: this.contextSelect.value
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            this.showResult(data.analysis, data.risk_level);
            
        } catch (error) {
            this.showError(`Error: ${error.message}`);
        }
    }
    
    async chat() {
        const text = this.textInput.value.trim();
        if (!text) {
            this.showError('Please enter a message to chat');
            return;
        }
        
        this.showLoading();
        
        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            this.showResult(data.response);
            
        } catch (error) {
            this.showError(`Error: ${error.message}`);
        }
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new YNavApp();
});
