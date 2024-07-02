import React, { useState } from 'react';
import axios from 'axios';

const RequestPasswordReset: React.FC = () => {
  const [email, setEmail] = useState<string>('');
  const [message, setMessage] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('/request_password_reset/', { email });
      setMessage(response.data.message);
    } catch (error: any) {
      setMessage(error.response?.data?.detail || 'Error requesting password reset');
    }
  };

  return (
    <div>
      <h2>Request Password Reset</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <button type="submit">Request</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default RequestPasswordReset;
