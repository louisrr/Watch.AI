import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import axios from 'axios';
import { BrowserRouter as Router } from 'react-router-dom';
import ChangePassword from './ChangePassword';

jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('ChangePassword', () => {
  test('renders form inputs and submit button', () => {
    render(
      <Router>
        <ChangePassword />
      </Router>
    );
    expect(screen.getByPlaceholderText('Change Key')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('New Password')).toBeInTheDocument();
    expect(screen.getByText('Change')).toBeInTheDocument();
  });

  test('submits form and displays success message', async () => {
    mockedAxios.post.mockResolvedValue({ data: { message: 'Password successfully updated' } });
    
    render(
      <Router>
        <ChangePassword />
      </Router>
    );
    
    fireEvent.change(screen.getByPlaceholderText('Change Key'), { target: { value: 'change_key' } });
    fireEvent.change(screen.getByPlaceholderText('New Password'), { target: { value: 'new_password' } });
    fireEvent.click(screen.getByText('Change'));
    
    expect(await screen.findByText('Password successfully updated')).toBeInTheDocument();
  });

  test('displays error message on form submission failure', async () => {
    mockedAxios.post.mockRejectedValue({ response: { data: { detail: 'Error changing password' } } });
    
    render(
      <Router>
        <ChangePassword />
      </Router>
    );
    
    fireEvent.change(screen.getByPlaceholderText('Change Key'), { target: { value: 'change_key' } });
    fireEvent.change(screen.getByPlaceholderText('New Password'), { target: { value: 'new_password' } });
    fireEvent.click(screen.getByText('Change'));
    
    expect(await screen.findByText('Error changing password')).toBeInTheDocument();
  });
});

