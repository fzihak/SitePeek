// Configuration
// For production, update this to your deployed backend URL
const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000' 
    : 'https://your-backend-url.railway.app'; // Update this after deploying backend

// Global state
let currentData = null;
let currentUrl = null;

// DOM Elements
const urlInput = document.getElementById('urlInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingSection = document.getElementById('loadingSection');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const retryBtn = document.getElementById('retryBtn');
const resultsSection = document.getElementById('resultsSection');
const sourceModal = document.getElementById('sourceModal');
const downloadAllBtn = document.getElementById('downloadAllBtn');

// Event Listeners
analyzeBtn.addEventListener('click', analyzeWebsite);
retryBtn.addEventListener('click', () => {
    errorSection.classList.add('hidden');
    urlInput.focus();
});
downloadAllBtn.addEventListener('click', downloadAllFiles);

urlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        analyzeWebsite();
    }
});

// Initialize accordion functionality
document.querySelectorAll('.accordion-header').forEach(header => {
    header.addEventListener('click', () => {
        const target = header.dataset.target;
        const content = document.getElementById(target);
        
        header.classList.toggle('active');
        content.classList.toggle('active');
    });
});

// Main analyze function
async function analyzeWebsite() {
    const url = urlInput.value.trim();
    
    if (!url) {
        showError('Please enter a valid URL');
        return;
    }
    
    // Basic URL validation
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
        showError('URL must start with http:// or https://');
        return;
    }
    
    currentUrl = url;
    
    // Hide previous results/errors
    resultsSection.classList.add('hidden');
    errorSection.classList.add('hidden');
    
    // Show loading
    loadingSection.classList.remove('hidden');
    
    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to analyze website');
        }
        
        const data = await response.json();
        currentData = data;
        
        // Hide loading and show results
        loadingSection.classList.add('hidden');
        displayResults(data);
        
    } catch (error) {
        loadingSection.classList.add('hidden');
        showError(error.message || 'Failed to analyze website. Please check the URL and try again.');
    }
}

// Display results
function displayResults(data) {
    // Update summary cards
    document.getElementById('totalCSS').textContent = data.summary.total_css;
    document.getElementById('totalJS').textContent = data.summary.total_js;
    document.getElementById('totalImages').textContent = data.summary.total_images;
    document.getElementById('totalOthers').textContent = data.summary.total_others;
    
    // Display source code preview
    displaySourceCode(data.html_source);
    
    // Display file lists
    displayFileList('cssFiles', data.css_files, 'CSS');
    displayFileList('jsFiles', data.js_files, 'JS');
    displayFileList('imageFiles', data.images, 'IMG');
    displayFileList('otherFiles', data.others, 'FILE');
    
    // Display colors
    displayColors(data.colors);
    
    // Display fonts
    displayFonts(data.fonts);
    
    // Display file structure
    displayFileStructure(data.structure);
    
    // Show results section
    resultsSection.classList.remove('hidden');
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Display source code
function displaySourceCode(source) {
    const preview = document.getElementById('sourcePreview').querySelector('code');
    const lines = source.split('\n');
    const previewLines = lines.slice(0, 20).join('\n');
    preview.textContent = previewLines + (lines.length > 20 ? '\n\n... (truncated)' : '');
}

// Display file lists
function displayFileList(containerId, files, iconText) {
    const container = document.getElementById(containerId);
    
    if (!files || files.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="12" y1="8" x2="12" y2="12"></line>
                    <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                <p>No files found</p>
            </div>
        `;
        return;
    }
    
    const fileListHTML = files.map(file => `
        <div class="file-item">
            <div class="file-info">
                <div class="file-icon">${iconText}</div>
                <div class="file-name">${escapeHtml(getFileName(file))}</div>
            </div>
            <div class="file-actions">
                <button class="file-btn" onclick="viewFile('${escapeHtml(file)}')">View</button>
                <button class="file-btn" onclick="downloadFile('${escapeHtml(file)}')">Download</button>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = `<div class="file-list">${fileListHTML}</div>`;
}

// Display colors
function displayColors(colors) {
    const container = document.getElementById('colorsUsed');
    
    if (!colors || colors.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10"></circle>
                    <path d="M12 2a7 7 0 0 0 0 20"></path>
                </svg>
                <p>No colors detected</p>
            </div>
        `;
        return;
    }
    
    // Remove duplicates
    const uniqueColors = [...new Set(colors)];
    
    const colorHTML = uniqueColors.slice(0, 24).map(color => `
        <div class="color-item">
            <div class="color-swatch" style="background: ${escapeHtml(color)}" title="${escapeHtml(color)}"></div>
            <div class="color-value">${escapeHtml(color)}</div>
        </div>
    `).join('');
    
    container.innerHTML = `<div class="color-grid">${colorHTML}</div>`;
}

// Display fonts
function displayFonts(fonts) {
    const container = document.getElementById('fontsUsed');
    
    if (!fonts || fonts.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <polyline points="4 7 4 4 20 4 20 7"></polyline>
                    <line x1="9" y1="20" x2="15" y2="20"></line>
                    <line x1="12" y1="4" x2="12" y2="20"></line>
                </svg>
                <p>No fonts detected</p>
            </div>
        `;
        return;
    }
    
    // Remove duplicates
    const uniqueFonts = [...new Set(fonts)];
    
    const fontHTML = uniqueFonts.map(font => `
        <div class="font-item">
            <div class="font-name" style="font-family: ${escapeHtml(font)}">${escapeHtml(font)}</div>
            <div class="font-preview" style="font-family: ${escapeHtml(font)}">
                The quick brown fox jumps over the lazy dog
            </div>
        </div>
    `).join('');
    
    container.innerHTML = `<div class="font-list">${fontHTML}</div>`;
}

// Display file structure
function displayFileStructure(structure) {
    const container = document.getElementById('fileStructure');
    
    if (!structure || Object.keys(structure).length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
                </svg>
                <p>No structure available</p>
            </div>
        `;
        return;
    }
    
    const treeHTML = buildTreeHTML(structure);
    container.innerHTML = `<div class="tree">${treeHTML}</div>`;
}

// Build tree HTML recursively
function buildTreeHTML(obj, prefix = '') {
    let html = '';
    const entries = Object.entries(obj);
    
    entries.forEach(([key, value], index) => {
        const isLast = index === entries.length - 1;
        const connector = isLast ? '└── ' : '├── ';
        
        if (typeof value === 'object' && value !== null) {
            html += `<div class="tree-item">${prefix}${connector}<span class="tree-folder">${escapeHtml(key)}/</span></div>`;
            const newPrefix = prefix + (isLast ? '    ' : '│   ');
            html += buildTreeHTML(value, newPrefix);
        } else {
            html += `<div class="tree-item">${prefix}${connector}<span class="tree-file">${escapeHtml(key)}</span></div>`;
        }
    });
    
    return html;
}

// View source in modal
function viewSource() {
    if (!currentData) return;
    
    const fullSourceCode = document.getElementById('fullSourceCode').querySelector('code');
    fullSourceCode.textContent = currentData.html_source;
    
    sourceModal.classList.remove('hidden');
}

// Download source
function downloadSource() {
    if (!currentData) return;
    
    const blob = new Blob([currentData.html_source], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'source.html';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// View file
async function viewFile(fileUrl) {
    window.open(fileUrl, '_blank');
}

// Download single file
async function downloadFile(fileUrl) {
    try {
        const response = await fetch(`${API_BASE_URL}/download?file_url=${encodeURIComponent(fileUrl)}`);
        
        if (!response.ok) {
            throw new Error('Failed to download file');
        }
        
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = getFileName(fileUrl);
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    } catch (error) {
        showError('Failed to download file: ' + error.message);
    }
}

// Download all files as ZIP
async function downloadAllFiles() {
    if (!currentUrl) return;
    
    try {
        downloadAllBtn.disabled = true;
        downloadAllBtn.textContent = 'Preparing ZIP...';
        
        const response = await fetch(`${API_BASE_URL}/download-all`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: currentUrl })
        });
        
        if (!response.ok) {
            throw new Error('Failed to create ZIP file');
        }
        
        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'website_assets.zip';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
    } catch (error) {
        showError('Failed to download ZIP: ' + error.message);
    } finally {
        downloadAllBtn.disabled = false;
        downloadAllBtn.innerHTML = `
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                <polyline points="7 10 12 15 17 10"></polyline>
                <line x1="12" y1="15" x2="12" y2="3"></line>
            </svg>
            Download All as ZIP
        `;
    }
}

// Close modal
function closeModal() {
    sourceModal.classList.add('hidden');
}

// Click outside modal to close
sourceModal.addEventListener('click', (e) => {
    if (e.target === sourceModal) {
        closeModal();
    }
});

// Show error message
function showError(message) {
    errorMessage.textContent = message;
    errorSection.classList.remove('hidden');
}

// Utility functions
function getFileName(url) {
    try {
        const urlObj = new URL(url);
        const pathname = urlObj.pathname;
        const filename = pathname.substring(pathname.lastIndexOf('/') + 1);
        return filename || 'file';
    } catch {
        return 'file';
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}