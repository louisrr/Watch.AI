import React from 'react';

interface VideoResultProps {
  processedVideoUrl: string;
}

const VideoResult: React.FC<VideoResultProps> = ({ processedVideoUrl }) => {
  return (
    <div>
      <h2>Processed Video</h2>
      <video controls>
        <source src={processedVideoUrl} type="video/mp4" />
        Your browser does not support the video tag.
      </video>
      <a href={processedVideoUrl} download="processed_video.mp4">
        Download Processed Video
      </a>
    </div>
  );
};

export default VideoResult;