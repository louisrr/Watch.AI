import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import axios from 'axios';
import TextPromptVideoGenerator from './TextPromptVideoGenerator';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('TextPromptVideoGenerator', () => {
  test('renders form input and submit button', () => {
    render(<TextPromptVideoGenerator />);
    expect(screen.getByPlaceholderText('Enter text prompt')).toBeInTheDocument();
    expect(screen.getByText('Generate Video')).toBeInTheDocument();
  });

  test('submits form and displays generated video', async () => {
    const videoUrl = 'http://example.com/video.mp4';
    mockedAxios.post.mockResolvedValue({ data: { video_url: videoUrl } });
    
    render(<TextPromptVideoGenerator />);
    
    fireEvent.change(screen.getByPlaceholderText('Enter text prompt'), { target: { value: 'example prompt' } });
    fireEvent.click(screen.getByText('Generate Video'));
    
    expect(await screen.findByText('Generated Video')).toBeInTheDocument();
    expect(screen.getByRole('video')).toHaveAttribute('src', videoUrl);
  });

  test('displays error message on form submission failure', async () => {
    mockedAxios.post.mockRejectedValue({ response: { data: { detail: 'Error generating video' } } });
    
    render(<TextPromptVideoGenerator />);
    
    fireEvent.change(screen.getByPlaceholderText('Enter text prompt'), { target: { value: 'example prompt' } });
    fireEvent.click(screen.getByText('Generate Video'));
    
    expect(await screen.findByText('Error generating video')).toBeInTheDocument();
  });
});
