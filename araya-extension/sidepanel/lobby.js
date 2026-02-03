// Araya Lobby - 7 Domains Controller
// IndexedDB for local storage

const DB_NAME = 'ArayaLobby';
const DB_VERSION = 1;
let db = null;

// Domain routing rules
const DOMAIN_RULES = {
    '1_COMMAND': ['calendar', 'notion', 'trello', 'asana', 'monday', 'todoist'],
    '2_BUILD': ['github', 'gitlab', 'figma', 'codepen', 'replit', 'vercel', 'netlify'],
    '3_CONNECT': ['linkedin', 'twitter', 'facebook', 'discord', 'slack', 'mail', 'gmail'],
    '4_PROTECT': ['court', 'gov', 'legal', 'health', 'insurance', 'bank'],
    '5_GROW': ['stripe', 'paypal', 'shopify', 'analytics', 'finance', 'invest'],
    '6_LEARN': ['wikipedia', 'youtube', 'medium', 'substack', 'coursera', 'udemy'],
    '7_TRANSCEND': ['meditation', 'headspace', 'calm', 'journal', 'wellness']
};

// Initialize IndexedDB
function initDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, DB_VERSION);

        request.onerror = () => reject(request.error);
        request.onsuccess = () => {
            db = request.result;
            resolve(db);
        };

        request.onupgradeneeded = (event) => {
            const db = event.target.result;

            // Create stores for each domain
            ['1_COMMAND', '2_BUILD', '3_CONNECT', '4_PROTECT', '5_GROW', '6_LEARN', '7_TRANSCEND'].forEach(domain => {
                if (!db.objectStoreNames.contains(domain)) {
                    const store = db.createObjectStore(domain, { keyPath: 'id', autoIncrement: true });
                    store.createIndex('created', 'created');
                    store.createIndex('type', 'type');
                }
            });
        };
    });
}

// Save item to domain
async function saveItem(domain, item) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(domain, 'readwrite');
        const store = transaction.objectStore(domain);

        const data = {
            ...item,
            created: new Date().toISOString(),
            id: Date.now()
        };

        const request = store.add(data);
        request.onsuccess = () => resolve(data);
        request.onerror = () => reject(request.error);
    });
}

// Get items from domain
async function getItems(domain, limit = 100) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(domain, 'readonly');
        const store = transaction.objectStore(domain);
        const request = store.getAll();

        request.onsuccess = () => resolve(request.result.slice(-limit));
        request.onerror = () => reject(request.error);
    });
}

// Count items in domain
async function countItems(domain) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(domain, 'readonly');
        const store = transaction.objectStore(domain);
        const request = store.count();

        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

// Update all counts
async function updateCounts() {
    const domains = ['1_COMMAND', '2_BUILD', '3_CONNECT', '4_PROTECT', '5_GROW', '6_LEARN', '7_TRANSCEND'];
    let total = 0;

    for (let i = 0; i < domains.length; i++) {
        const count = await countItems(domains[i]);
        document.getElementById(`count-${i + 1}`).textContent = `${count} items`;
        total += count;
    }

    document.getElementById('total-items').textContent = `${total} total items`;
}

// Detect domain from URL
function detectDomain(url) {
    const urlLower = url.toLowerCase();

    for (const [domain, keywords] of Object.entries(DOMAIN_RULES)) {
        if (keywords.some(kw => urlLower.includes(kw))) {
            return domain;
        }
    }

    return '6_LEARN'; // Default to Learn
}

// Open domain view
function openDomain(domain) {
    // Navigate to domain detail page
    window.location.href = `domains/${domain.toLowerCase()}.html`;
}

// Capture item from input
async function captureItem() {
    const input = document.getElementById('capture-input');
    const select = document.getElementById('domain-select');

    const text = input.value.trim();
    if (!text) return;

    const domain = select.value;

    await saveItem(domain, {
        type: 'note',
        content: text,
        source: 'manual'
    });

    input.value = '';
    await updateCounts();

    // Visual feedback
    const card = document.querySelector(`[data-domain="${domain}"]`);
    card.style.transform = 'scale(1.1)';
    setTimeout(() => card.style.transform = '', 300);
}

// Open Araya chat
function openChat() {
    // Will connect to Araya chat panel
    chrome.tabs.create({ url: 'https://conciousnessrevolution.io/araya-chat.html' });
}

// Listen for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'PAGE_DATA') {
        const suggestedDomain = detectDomain(message.url);
        const suggestion = document.getElementById('suggestion');
        const suggestionText = document.getElementById('suggestion-text');

        suggestionText.textContent = `Save this page to ${suggestedDomain}?`;
        suggestion.classList.add('active');

        // Auto-select domain in dropdown
        document.getElementById('domain-select').value = suggestedDomain;
    }

    if (message.type === 'SAVE_TO_DOMAIN') {
        saveItem(message.domain, message.data).then(() => {
            updateCounts();
            sendResponse({ success: true });
        });
        return true;
    }
});

// Initialize on load
document.addEventListener('DOMContentLoaded', async () => {
    await initDB();
    await updateCounts();

    // Get current tab info
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs[0]) {
            const suggestedDomain = detectDomain(tabs[0].url);
            document.getElementById('domain-select').value = suggestedDomain;
        }
    });
});
