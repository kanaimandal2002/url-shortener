document.getElementById('shorten-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const urlInput = document.getElementById('url-input');
    const customCode = document.getElementById('custom-code');
    const resultDiv = document.getElementById('result');
    const shortUrlLink = document.getElementById('short-url');
    
    const data = {
        url: urlInput.value,
        custom_code: customCode.value || undefined
    };
    
    try {
        const response = await fetch('/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to shorten URL');
        }
        
        const result = await response.json();
        shortUrlLink.textContent = result.short_url;
        shortUrlLink.href = result.short_url;
        resultDiv.classList.remove('hidden');
        
    } catch (error) {
        alert(error.message);
    }
});

document.getElementById('copy-btn').addEventListener('click', () => {
    const shortUrl = document.getElementById('short-url').textContent;
    navigator.clipboard.writeText(shortUrl)
        .then(() => alert('URL copied to clipboard!'))
        .catch(() => alert('Failed to copy URL'));
});
