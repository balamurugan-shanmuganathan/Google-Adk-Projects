document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('url-form');
    const input = document.getElementById('youtube-url');
    const resultSection = document.getElementById('result-section');
    const videoWrapper = document.getElementById('video-wrapper');
    const analysisOutput = document.getElementById('analysis-output');
    const statusIndicator = document.getElementById('status');
    const statusText = document.getElementById('status')?.querySelector('.status-text');
    const submitBtn = document.getElementById('submit-btn');

    let fullMarkdown = "";
    const converter = new showdown.Converter({
        tables: true,
        strikethrough: true,
        tasklists: true,
        simpleLineBreaks: true
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const url = input.value.trim();
        if (!url) return;

        // 1. Reset UI (Keep Hero as is)
        fullMarkdown = "";
        analysisOutput.innerHTML = `
            <div class="skeleton-text"></div>
            <div class="skeleton-text" style="width: 80%"></div>
            <div class="skeleton-text" style="width: 90%"></div>
        `;
        videoWrapper.innerHTML = '<div class="skeleton-media"></div>';
        
        statusIndicator.classList.add('loading');
        if (statusText) statusText.textContent = 'Thinking...';
        
        resultSection.classList.remove('hidden');
        setTimeout(() => resultSection.classList.add('visible'), 50);
        submitBtn.disabled = true;

        // 2. Embed Video Immediately
        const videoId = extractYouTubeId(url);
        if (videoId) {
            videoWrapper.innerHTML = `<iframe src="https://www.youtube.com/embed/${videoId}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
        } else {
            videoWrapper.innerHTML = '<div class="placeholder-content"><p>Invalid YouTube URL</p></div>';
        }

        // 3. Start Streaming
        try {
            const eventSource = new EventSource(`/stream?url=${encodeURIComponent(url)}`);

            eventSource.onmessage = (event) => {
                if (event.data === "[DONE]") {
                    eventSource.close();
                    statusIndicator.classList.remove('loading');
                    if (statusText) statusText.textContent = 'Complete';
                    submitBtn.disabled = false;
                    return;
                }

                let chunk = event.data;
                
                // Smart streaming: detect if the chunk is a delta or the full message
                if (chunk.length > fullMarkdown.length && chunk.startsWith(fullMarkdown)) {
                    fullMarkdown = chunk; 
                } else if (fullMarkdown.endsWith(chunk) || fullMarkdown.includes(chunk)) {
                    // Skip duplicate
                } else {
                    fullMarkdown += chunk;
                }

                if (fullMarkdown.trim() !== "") {
                    let displayMarkdown = fullMarkdown.trim()
                        .replace(/^```markdown\n?/gi, '')
                        .replace(/```$/g, '');

                    analysisOutput.innerHTML = converter.makeHtml(displayMarkdown);
                }
                
                // Auto-scroll the analysis container specifically
                analysisOutput.scrollTop = analysisOutput.scrollHeight;
            };

            eventSource.onerror = (err) => {
                eventSource.close();
                statusIndicator.classList.remove('loading');
                if (statusText) statusText.textContent = 'Error';
                submitBtn.disabled = false;
            };

        } catch (err) {
            console.error("Stream initialization error:", err);
            submitBtn.disabled = false;
        }
    });

    function extractYouTubeId(url) {
        const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
        const match = url.match(regExp);
        return (match && match[2].length === 11) ? match[2] : null;
    }
});
