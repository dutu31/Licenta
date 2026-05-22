import React, { useState } from 'react';
import axios from 'axios';
import './Login.css'; 

function Login({ onLoginSuccess }) {
  const [authMode, setAuthMode] = useState('login'); // 'login' sau 'register'
  const [authUsername, setAuthUsername] = useState('');
  const [authPassword, setAuthPassword] = useState('');
  const [authMessage, setAuthMessage] = useState({ text: '', type: '' });
  const [isAuthLoading, setIsAuthLoading] = useState(false);

  const handleAuthSubmit = async (e) => {
    e.preventDefault();
    setIsAuthLoading(true);
    setAuthMessage({ text: '', type: '' });

    const endpoint = authMode === 'login' ? '/api/auth/login' : '/api/auth/register';

    try {
      const response = await axios.post(`http://localhost:8080${endpoint}`, {
        username: authUsername,
        password: authPassword
      });

      if (authMode === 'login') {
        onLoginSuccess(response.data); 
      } else {
        setAuthMessage({ text: 'Registration successful! Please login.', type: 'success' });
        setAuthMode('login');
        setAuthPassword(''); 
      }
    } catch (error) {
      const errorMsg = error.response?.data || 'An error occurred connecting to the server.';
      setAuthMessage({ text: errorMsg, type: 'error' });
    } finally {
      setIsAuthLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h2 className="auth-title">{authMode === 'login' ? 'System Access' : 'Create Account'}</h2>
        <p className="auth-subtitle">COLMAP Localization System</p>
        
        <form onSubmit={handleAuthSubmit} className="auth-form">
          <input 
            type="text" 
            placeholder="Username" 
            value={authUsername}
            onChange={(e) => setAuthUsername(e.target.value)}
            required
            className="form-input auth-input"
          />
          <input 
            type="password" 
            placeholder="Password" 
            value={authPassword}
            onChange={(e) => setAuthPassword(e.target.value)}
            required
            className="form-input auth-input"
          />
          
          {authMessage.text && (
            <div className={`auth-msg ${authMessage.type}`}>
              {authMessage.text}
            </div>
          )}

          <button type="submit" className="submit-button" disabled={isAuthLoading}>
            {isAuthLoading ? 'Processing...' : (authMode === 'login' ? 'Login' : 'Register')}
          </button>
        </form>

        <div className="auth-toggle">
          {authMode === 'login' ? (
            <p>New user? <span onClick={() => {setAuthMode('register'); setAuthMessage({text:'', type:''})}}>Create an account</span></p>
          ) : (
            <p>Already have an account? <span onClick={() => {setAuthMode('login'); setAuthMessage({text:'', type:''})}}>Login here</span></p>
          )}
        </div>
      </div>
    </div>
  );
}

export default Login;