import React, { useState, FormEvent } from 'react';
import { Helmet } from 'react-helmet';
import { useTranslation } from 'react-i18next';
import './Login.css';

const Login: React.FC = () => {
  const { t } = useTranslation('Login'); // Specify the namespace
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (event: FormEvent) => {
    event.preventDefault();
    // Handle login logic here
  };

  return (
    <div>
      <Helmet>
        <title>{t('loginTitle')} - Kairos</title>
        <meta name="description" content={t('loginDescription')} />
        <meta name="keywords" content={t('loginKeywords')} />
      </Helmet>
      <form onSubmit={handleSubmit} className="login-form">
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder={t('username')}
          className="login-input"
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder={t('password')}
          className="login-input"
        />
        <button type="submit" className="login-button">{t('loginButton')}</button>
      </form>
    </div>
  );
}

export default Login;
