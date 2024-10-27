// extension.js

// Listen for messages from the content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.links) {
        console.log("Received links:", request.links);

        // You can now use the links as needed in your extension logic
        // For example, updating allowed URLs or any other logic
        allowedURLs.push(...request.links); // Add received links to allowedURLs
    }
});

// Alternatively, you can retrieve the links from localStorage if stored
const storedLinks = JSON.parse(localStorage.getItem('links'));
if (storedLinks) {
    console.log("Links from localStorage:", storedLinks);
    allowedURLs.push(...storedLinks); // Add to allowed URLs if needed
}

// Initialize the allowed URLs array
const allowedURLs = ["https://chess.com"];  // Use the base URL without a trailing slash
const redirectCooldown = 3000; // 3 seconds cooldown between redirects

// Track the last redirection time per tab
const lastRedirectTime = {};

// Function to check if the URL is allowed
function isAllowed(url) {
    return allowedURLs.some(allowedURL => {
        // Normalize URLs for comparison
        const normalizedAllowedURL = allowedURL.endsWith('/') ? allowedURL : allowedURL + '/';
        const normalizedURL = url.endsWith('/') ? url : url + '/';
        return normalizedURL.startsWith(normalizedAllowedURL);
    });
}

// Listen for navigation events
chrome.webNavigation.onCommitted.addListener((details) => {
    const currentUrl = details.url;
    const tabId = details.tabId;
    const currentTime = Date.now();

    // Only redirect if the current URL is not allowed
    if (!isAllowed(currentUrl)) {
        // Check if enough time has passed since the last redirect
        if (!lastRedirectTime[tabId] || currentTime - lastRedirectTime[tabId] > redirectCooldown) {
            // Update the last redirect time for this tab
            lastRedirectTime[tabId] = currentTime;

            // Redirect to the first allowed URL (or choose another logic to select a link)
            chrome.tabs.update(tabId, { url: allowedURLs[0] });
        }
    }
}, { url: [{ schemes: ["http", "https"] }] });
