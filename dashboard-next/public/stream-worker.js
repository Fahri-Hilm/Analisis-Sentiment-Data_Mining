// Background service worker for persistent streaming
let streamInterval = null;
let isStreaming = false;

self.addEventListener('message', (event) => {
  const { type, data } = event.data;

  switch (type) {
    case 'START_STREAM':
      if (!isStreaming) {
        isStreaming = true;
        streamInterval = setInterval(() => {
          // Simulate data collection
          self.postMessage({
            type: 'STREAM_DATA',
            data: {
              timestamp: Date.now(),
              sentiment: Math.random() > 0.5 ? 'positive' : 'negative',
              comment: 'Sample comment data'
            }
          });
        }, 2000);
        
        self.postMessage({ type: 'STREAM_STARTED' });
      }
      break;

    case 'STOP_STREAM':
      if (isStreaming) {
        isStreaming = false;
        if (streamInterval) {
          clearInterval(streamInterval);
          streamInterval = null;
        }
        self.postMessage({ type: 'STREAM_STOPPED' });
      }
      break;

    case 'GET_STATUS':
      self.postMessage({ 
        type: 'STREAM_STATUS', 
        data: { isStreaming } 
      });
      break;
  }
});
