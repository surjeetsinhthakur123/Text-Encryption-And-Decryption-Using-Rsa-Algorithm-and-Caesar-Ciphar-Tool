import React, { useState } from 'react';
import { Eye, EyeOff, Unlock, AlertCircle } from 'lucide-react';
import { pycryptAPI } from '../services/api';

const DecryptForm = ({ onResult, onLoading, onError }) => {
  const [encryptedContent, setEncryptedContent] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!encryptedContent.trim()) {
      onError('Please enter encrypted content to decrypt');
      return;
    }
    
    if (!password.trim()) {
      onError('Please enter the password');
      return;
    }

    setIsLoading(true);
    onLoading(true);
    onError('');

    try {
      const result = await pycryptAPI.decryptText(encryptedContent, password);
      
      if (result.success) {
        onResult({
          type: 'decrypted',
          content: result.data.decrypted_text,
          originalEncrypted: encryptedContent
        });
      } else {
        onError(result.error);
      }
    } catch (error) {
      onError('Failed to decrypt text. Please check your password and try again.');
    } finally {
      setIsLoading(false);
      onLoading(false);
    }
  };

  const handleClear = () => {
    setEncryptedContent('');
    setPassword('');
    onResult(null);
    onError('');
  };

  return (
    <form onSubmit={handleSubmit} className="decrypt-form">
      <div className="form-group">
        <label htmlFor="decrypt-content">Encrypted Content</label>
        <textarea
          id="decrypt-content"
          value={encryptedContent}
          onChange={(e) => setEncryptedContent(e.target.value)}
          placeholder="Paste your encrypted content here..."
          rows={6}
          className="form-textarea encrypted-content"
          disabled={isLoading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="decrypt-password">Password</label>
        <div className="password-input-wrapper">
          <input
            id="decrypt-password"
            type={showPassword ? 'text' : 'password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            className="form-input"
            disabled={isLoading}
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="password-toggle"
            disabled={isLoading}
          >
            {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
          </button>
        </div>
      </div>

      <div className="form-actions">
        <button
          type="submit"
          className="btn btn-primary"
          disabled={isLoading || !encryptedContent.trim() || !password.trim()}
        >
          <Unlock size={20} />
          {isLoading ? 'Decrypting...' : 'Decrypt Text'}
        </button>
        <button
          type="button"
          onClick={handleClear}
          className="btn btn-secondary"
          disabled={isLoading}
        >
          Clear
        </button>
      </div>
    </form>
  );
};

export default DecryptForm; 