import React, { useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const ChangePassword: React.FC = () => {
  const { unique_hash } = useParams<{ unique_hash: string }>();
  const [change, setChange] = useState<string>('');
  const [newPassword, setNewPassword] = useState<string>('');
  const [message, setMessage] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post(`/change_password/${unique_hash}/`, { change, newPassword });
      setMessage(response.data.message);
    } catch (error: any) {
      setMessage(error.response?.data?.detail || 'Error changing password');
    }
  };

  return (
    <div>
      <h2>Change Password</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={change}
          onChange={(e) => setChange(e.target.value)}
          placeholder="Change Key"
          required
        />
        <input
          type="password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          placeholder="New Password"
          required
        />
        <button type="submit">Change</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default ChangePassword;
