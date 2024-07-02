import React, { useState } from 'react';
import axios from 'axios';

const TextPromptVideoGenerator: React.FC = () => {
  const [textPrompt, setTextPrompt] = useState<string>('');
  const [videoUrl, setVideoUrl] = useState<string>('');
  const [message, setMessage] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('/text_prompt/', { text: textPrompt });
      setVideoUrl(response.data.video_url);
      setMessage('');
    } catch (error: any) {
      setMessage(error.response?.data?.detail || 'Error generating video');
      setVideoUrl('');
    }
  };

  return (
    <div>
      <h2>Generate Video from Text Prompt</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={textPrompt}
          onChange={(e) => setTextPrompt(e.target.value)}
          placeholder="Enter text prompt"
          required
        />
        <button type="submit">Generate Video</button>
      </form>
      {message && <p>{message}</p>}
      {videoUrl && (
        <div>
          <h3>Generated Video</h3>
          <video src={videoUrl} controls />
        </div>
      )}
    </div>
  );
};

export default TextPromptVideoGenerator;
