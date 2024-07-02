import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import axios from 'axios';
import RequestPasswordReset from './RequestPasswordReset';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('RequestPasswordReset', () => {
  test('renders form input and submit button', () => {
    render(<RequestPasswordReset />);
    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
    expect(screen.getByText('Request')).toBeInTheDocument();
  });

  test('submits form and displays success message', async () => {
    mockedAxios.post.mockResolvedValue({ data: { message: 'Password reset requested' } });
    
    render(<RequestPasswordReset />);
    
    fireEvent.change(screen.getByPlaceholderText('Email'), { target: { value: 'test@example.com' } });
    fireEvent.click(screen.getByText('Request'));
    
    expect(await screen.findByText('Password reset requested')).toBeInTheDocument();
  });

  test('displays error message on form submission failure', async () => {
    mockedAxios.post.mockRejectedValue({ response: { data: { detail: 'Error requesting password reset' } } });
    
    render(<RequestPasswordReset />);
    
    fireEvent.change(screen.getByPlaceholderText('Email'), { target: { value: 'test@example.com' } });
    fireEvent.click(screen.getByText('Request'));
    
    expect(await screen.findByText('Error requesting password reset')).toBeInTheDocument();
  });
});
