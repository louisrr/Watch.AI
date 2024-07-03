import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface VideoProcessingProps {
  videoId: string;
  onProcessingComplete: (processedVideoUrl: string) => void;
}

const VideoProcessing: React.FC<VideoProcessingProps> = ({ videoId, onProcessingComplete }) => {
  const [isProcessing, setIsProcessing] = useState<boolean>(true);

  useEffect(() => {
    const processVideo = async () => {
      try {
        const response = await axios.post(`/api/process/${videoId}`);
        onProcessingComplete(response.data.processedVideoUrl);
        setIsProcessing(false);
      } catch (error) {
        console.error('Error processing video:', error);
      }
    };

    processVideo();
  }, [videoId, onProcessingComplete]);

  return (
    <div>
      {isProcessing ? <p>Processing video...</p> : <p>Video processing complete.</p>}
    </div>
  );
};

export default VideoProcessing;