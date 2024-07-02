import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import axios from 'axios';
import CreateUser from './CreateUser';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('CreateUser', () => {
  test('renders form inputs and submit button', () => {
    render(<CreateUser />);
    expect(screen.getByPlaceholderText('Email')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
    expect(screen.getByText('Create')).toBeInTheDocument();
  });

  test('submits form and displays success message', async () => {
    mockedAxios.post.mockResolvedValue({ data: { message: 'User created successfully' } });
    
    render(<CreateUser />);
    
    fireEvent.change(screen.getByPlaceholderText('Email'), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByPlaceholderText('Password'), { target: { value: 'password' } });
    fireEvent.click(screen.getByText('Create'));
    
    expect(await screen.findByText('User created successfully')).toBeInTheDocument();
  });

  test('displays error message on form submission failure', async () => {
    mockedAxios.post.mockRejectedValue({ response: { data: { detail: 'Error creating user' } } });
    
    render(<CreateUser />);
    
    fireEvent.change(screen.getByPlaceholderText('Email'), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByPlaceholderText('Password'), { target: { value: 'password' } });
    fireEvent.click(screen.getByText('Create'));
    
    expect(await screen.findByText('Error creating user')).toBeInTheDocument();
  });
});
