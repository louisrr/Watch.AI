import React, { useState } from 'react';
import VideoUpload from './components/VideoUpload';
import VideoProcessing from './components/VideoProcessing';
import VideoResult from './components/VideoResult';

const App: React.FC = () => {
  const [videoId, setVideoId] = useState<string | null>(null);
  const [processedVideoUrl, setProcessedVideoUrl] = useState<string | null>(null);

  const handleUpload = (videoId: string) => {
    setVideoId(videoId);
  };

  const handleProcessingComplete = (processedVideoUrl: string) => {
    setProcessedVideoUrl(processedVideoUrl);
  };

  return (
    <div>
      <h1>Video Generator App</h1>
      {!videoId && <VideoUpload onUpload={handleUpload} />}
      {videoId && !processedVideoUrl && (
        <VideoProcessing videoId={videoId} onProcessingComplete={handleProcessingComplete} />
      )}
      {processedVideoUrl && <VideoResult processedVideoUrl={processedVideoUrl} />}
    </div>
  );
};

export default App;