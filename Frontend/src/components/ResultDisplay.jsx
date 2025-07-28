import React, { useState } from 'react';
import { Copy, Check, AlertCircle, Shield, Info } from 'lucide-react';

const ResultDisplay = ({ result, error }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(result.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text:', err);
    }
  };

  if (error) {
    return (
      <div className="result-container error">
        <div className="result-header">
          <AlertCircle size={20} />
          <span>Error</span>
        </div>
        <div className="result-content">
          <p className="error-message">{error}</p>
        </div>
      </div>
    );
  }

  if (!result) {
    return null;
  }

  return (
    <div className={`result-container ${result.type}`}>
      <div className="result-header">
        <Shield size={20} />
        <span>
          {result.type === 'encrypted' ? 'Encrypted Content' : 'Decrypted Content'}
        </span>
        <button
          onClick={handleCopy}
          className={`copy-btn ${copied ? 'copied' : ''}`}
          title="Copy to clipboard"
        >
          {copied ? <Check size={16} /> : <Copy size={16} />}
          {copied ? 'Copied!' : 'Copy'}
        </button>
      </div>

      <div className="result-content">
        <textarea
          value={result.content}
          readOnly
          rows={6}
          className="result-textarea"
          placeholder="Result will appear here..."
        />
      </div>

      {result.type === 'encrypted' && result.hint && (
        <div className="result-info">
          <Info size={16} />
          <span>Password hint: {result.hint}</span>
        </div>
      )}

      <div className="result-stats">
        <span className="stat">
          Length: {result.content.length} characters
        </span>
        {result.type === 'encrypted' && (
          <span className="stat">
            AES-256 encrypted
          </span>
        )}
      </div>
    </div>
  );
};

export default ResultDisplay; 