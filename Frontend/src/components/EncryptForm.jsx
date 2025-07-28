import React, { useState } from 'react';
import { Eye, EyeOff, Lock, AlertCircle } from 'lucide-react';
import { pycryptAPI } from '../services/api';

const EncryptForm = ({ onResult, onLoading, onError }) => {
  const [text, setText] = useState('');
  const [password, setPassword] = useState('');
  const [hint, setHint] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!text.trim()) {
      onError('Please enter text to encrypt');
      return;
    }
    
    if (!password.trim()) {
      onError('Please enter a password');
      return;
    }

    setIsLoading(true);
    onLoading(true);
    onError('');

    try {
      const result = await pycryptAPI.encryptText(text, password, hint);
      
      if (result.success) {
        onResult({
          type: 'encrypted',
          content: result.data.encrypted_content,
          hint: result.data.hint,
          originalText: text
        });
      } else {
        onError(result.error);
      }
    } catch (error) {
      onError('Failed to encrypt text. Please try again.');
    } finally {
      setIsLoading(false);
      onLoading(false);
    }
  };

  const handleClear = () => {
    setText('');
    setPassword('');
    setHint('');
    onResult(null);
    onError('');
  };

  return (
    <form onSubmit={handleSubmit} className="encrypt-form">
      <div className="form-group">
        <label htmlFor="encrypt-text">Text to Encrypt</label>
        <textarea
          id="encrypt-text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter your secret message here..."
          rows={6}
          className="form-textarea"
          disabled={isLoading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="encrypt-password">Password</label>
        <div className="password-input-wrapper">
          <input
            id="encrypt-password"
            type={showPassword ? 'text' : 'password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter a strong password"
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

      <div className="form-group">
        <label htmlFor="encrypt-hint">Password Hint (Optional)</label>
        <input
          id="encrypt-hint"
          type="text"
          value={hint}
          onChange={(e) => setHint(e.target.value)}
          placeholder="Optional hint to remember your password"
          className="form-input"
          disabled={isLoading}
        />
      </div>

      <div className="form-actions">
        <button
          type="submit"
          className="btn btn-primary"
          disabled={isLoading || !text.trim() || !password.trim()}
        >
          <Lock size={20} />
          {isLoading ? 'Encrypting...' : 'Encrypt Text'}
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

export default EncryptForm; 