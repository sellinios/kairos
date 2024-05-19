import React, { useState, FormEvent } from 'react';
import { Helmet } from 'react-helmet';
import './Login.css';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    // Handle login logic here
  };

  return (
    <div>
      <Helmet>
        <title>Login - Kairos</title>
        <meta name="description" content="Login to your Kairos account to access personalized services and features." />
        <meta name="keywords" content="Kairos, login, account, personalized services" />
      </Helmet>
      <form onSubmit={handleSubmit} className="login-form">
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          className="login-input"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          className="login-input"
        />
        <button type="submit" className="login-button">Login</button>
      </form>
    </div>
  );
}

export default Login;
