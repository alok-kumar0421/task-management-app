import React from 'react';
import { GoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import { loginWithGoogle } from '../services/api';

function Login({ setUser }) {
  const navigate = useNavigate();

  const handleLoginSuccess = async (credentialResponse) => {
    try {
      const result = await loginWithGoogle(credentialResponse.credential);
      // Save user to localStorage and state
      localStorage.setItem('user', JSON.stringify(result.user));
      setUser(result.user);
      navigate('/dashboard');
    } catch (error) {
      console.error("Login failed:", error);
      alert("Failed to login with Google.");
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <h1>Task Manager</h1>
        <p>Please login to continue</p>
        <div className="google-btn-wrapper">
          <GoogleLogin
            onSuccess={handleLoginSuccess}
            onError={() => {
              console.log('Login Failed');
              alert('Google Login Failed');
            }}
          />
        </div>
      </div>
    </div>
  );
}

export default Login;
