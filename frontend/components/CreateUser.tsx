import React, { useState } from 'react';
import axios from 'axios';

const CreateUser: React.FC = () => {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [message, setMessage] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post('/create_user/', { email, password });
      setMessage(response.data.message);
    } catch (error: any) {
      setMessage(error.response?.data?.detail || 'Error creating user');
    }
  };

  return (
    <div>
      <h2>Create User</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button type="submit">Create</button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default CreateUser;
