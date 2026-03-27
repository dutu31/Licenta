import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [uploaderId, setUploaderId] = useState('');
  
  const [recordData, setRecordData] = useState(null);
  
  const [statusMessage, setStatusMessage] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [isLocalizing, setIsLocalizing] = useState(false);
  const [isLocalized, setIsLocalized] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setRecordData(null);
    setIsLocalized(false);
    setStatusMessage('');
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file || !uploaderId) {
      alert('Please add userID and image');
      return;
    }

    const dataToSend = new FormData();
    dataToSend.append('file', file);
    dataToSend.append('uploaderId', uploaderId);

    try {
      setIsUploading(true);
      setStatusMessage('Image saving...');
      
      const response = await axios.post('http://localhost:8080/api/localization/upload', dataToSend, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      setRecordData(response.data); 
      setStatusMessage('Image successfully saved');
    } catch (error) {
      console.error('Upload error:', error);
      setStatusMessage('Upload error: ' + error.message);
    } finally {
      setIsUploading(false);
    }
  };

  const handleLocalize = async () => {
    try {
      setIsLocalizing(true);
      setStatusMessage('Running COLMAP on server. This process could take a while');
      
      const response = await axios.post('http://localhost:8080/api/localization/run-localize');
      
      setStatusMessage(response.data);
      setIsLocalized(true); 
    } catch (error) {
      setStatusMessage("Error: COLMAP couldn't localize the image.");
      setIsLocalized(false);
    } finally {
      setIsLocalizing(false);
    }
  };

  const handleView = async () => {
    try {
      setStatusMessage('Opening Open3D on server...');
      await axios.post('http://localhost:8080/api/localization/view');
    } catch (error) {
      setStatusMessage('Error at opening the visualizer');
    }
  };

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' };
    return new Date(dateString).toLocaleDateString('ro-RO', options);
  };

  return (
    <div className="app-container">
      <h1 className="welcome-title">Welcome!</h1>
      <h3 className="dashboard-subtitle">Localize position dashboard</h3>
      
      <form onSubmit={handleUpload} className="upload-form">
        <div className="form-group">
          <label>User ID:</label>
          <input 
            type="text" 
            value={uploaderId} 
            onChange={(e) => setUploaderId(e.target.value)} 
            required 
            className="form-input"
          />
        </div>

        <div className="file-drop-area">
          <label>Select image from dashboard:</label>
          <input 
            type="file" 
            accept="image/png, image/jpeg" 
            onChange={handleFileChange} 
            required 
            className="file-input"
          />
        </div>

        <button 
          type="submit" 
          className={`submit-button ${recordData ? 'success' : ''}`}
          disabled={isUploading || recordData !== null}
        >
          {isUploading ? 'Loading...' : (recordData ? 'Imagine Loaded' : '1. Upload Image')}
        </button>
      </form>

      {recordData && (
        <div className="details-box">
          <h4>Details</h4>
          <p><strong>Database ID:</strong> #{recordData.id}</p>
          <p><strong>Uploader:</strong> {recordData.uploaderId}</p>
          <p><strong>Date and time:</strong> {formatDate(recordData.uploadDateTime)}</p>
          <p><strong>Current Status:</strong> {recordData.status}</p>

          <button 
            onClick={handleLocalize}
            disabled={isLocalizing || isLocalized}
            className={`action-button localize-btn ${isLocalized ? 'disabled' : ''}`}
          >
            {isLocalizing ? 'COLMAP processing...' : (isLocalized ? 'Localizing succeed!' : '2. Running localize in 3d map')}
          </button>
        </div>
      )}

      {isLocalized && (
        <div className="view-container">
          <button onClick={handleView} className="action-button view-btn">
            Open 3D Map (View Location)
          </button>
        </div>
      )}

      {statusMessage && (
        <div className="status-message">
          {statusMessage}
        </div>
      )}
    </div>
  );
}

export default App;