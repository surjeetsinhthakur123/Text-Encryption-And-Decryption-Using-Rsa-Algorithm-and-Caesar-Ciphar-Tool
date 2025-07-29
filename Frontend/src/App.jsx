import React, { useState, useEffect } from 'react';
import { Shield, Wifi, WifiOff, AlertCircle } from 'lucide-react';
import EncryptForm from './components/EncryptForm';
import DecryptForm from './components/DecryptForm';
import ResultDisplay from './components/ResultDisplay';
import { pycryptAPI } from './services/api';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('encrypt');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [apiStatus, setApiStatus] = useState('checking');

  // Check API health on component mount
  useEffect(() => {
    checkApiHealth();
  }, []);

  const checkApiHealth = async () => {
    try {
      const healthResult = await pycryptAPI.healthCheck();
      setApiStatus(healthResult.success ? 'connected' : 'disconnected');
    } catch (error) {
      setApiStatus('disconnected');
    }
  };

  const handleTabChange = (tab) => {
    setActiveTab(tab);
    setResult(null);
    setError('');
  };

  const handleResult = (newResult) => {
    setResult(newResult);
    setError('');
  };

  const handleError = (errorMessage) => {
    setError(errorMessage);
    setResult(null);
  };

  const handleLoading = (loading) => {
    setIsLoading(loading);
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo">
            <Shield size={32} />
            <h1>PyCrypt</h1>
          </div>
          <div className="subtitle">
            Secure Text Encryption & Decryption
          </div>
          <div className={`api-status ${apiStatus}`}>
            {apiStatus === 'connected' ? <Wifi size={16} /> : <WifiOff size={16} />}
            <span>
              {apiStatus === 'checking' ? 'Checking...' : 
               apiStatus === 'connected' ? 'API Connected' : 'API Disconnected'}
            </span>
          </div>
        </div>
      </header>

      <main className="app-main">
        <div className="container">
          <div className="tabs">
            <button
              className={`tab ${activeTab === 'encrypt' ? 'active' : ''}`}
              onClick={() => handleTabChange('encrypt')}
              disabled={isLoading}
            >
              🔒 Encrypt
            </button>
            <button
              className={`tab ${activeTab === 'decrypt' ? 'active' : ''}`}
              onClick={() => handleTabChange('decrypt')}
              disabled={isLoading}
            >
              🔓 Decrypt
            </button>
          </div>

          <div className="content">
            <div className="form-section">
              {activeTab === 'encrypt' ? (
                <EncryptForm
                  onResult={handleResult}
                  onLoading={handleLoading}
                  onError={handleError}
                />
              ) : (
                <DecryptForm
                  onResult={handleResult}
                  onLoading={handleLoading}
                  onError={handleError}
                />
              )}
            </div>

            <div className="result-section">
              <ResultDisplay result={result} error={error} />
            </div>
          </div>

          {apiStatus === 'disconnected' && (
            <div className="api-warning">
              <AlertCircle size={20} />
              <span>
                Cannot connect to PyCrypt API. Make sure the Flask server is running on 
                <code>http://localhost:5000</code>
              </span>
              <button onClick={checkApiHealth} className="retry-btn">
                Retry
              </button>
            </div>
          )}
        </div>
      </main>

      <footer className="app-footer">
        <p>
          Powered by AES-256 encryption with PBKDF2 key derivation and HMAC verification
        </p>
      </footer>
    </div>
  );
}

export default App;
