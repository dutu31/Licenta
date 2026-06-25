import React, { useState } from 'react';
import axios from 'axios';
import Login from './Login'; 
import './App.css';

function App() {
  
  const [currentUser, setCurrentUser] = useState(null);

  
  const [file, setFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [recordData, setRecordData] = useState(null);
  const [statusMessage, setStatusMessage] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [isLocalizing, setIsLocalizing] = useState(false);
  const [isLocalized, setIsLocalized] = useState(false);

  const logout = () => {
    setCurrentUser(null);
    setFile(null);
    setImagePreview(null);
    setRecordData(null);
    setIsLocalized(false);
    setStatusMessage('');
  };

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    if (selectedFile) {
      setImagePreview(URL.createObjectURL(selectedFile));
    } else {
      setImagePreview(null);
    }
    setRecordData(null); 
    setIsLocalized(false); 
    setStatusMessage(''); 
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) {
      alert('Please select an image first.');
      return;
    }

    const dataToSend = new FormData();
    dataToSend.append('file', file);
    dataToSend.append('uploaderId', currentUser.username); 

    try {
      setIsUploading(true);
      setStatusMessage('Image saving...');
      const response = await axios.post('http://localhost:8080/api/localization/upload', dataToSend, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setRecordData(response.data); 
      setStatusMessage('Image successfully saved');
    } catch (error) {
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

  const handleReset = () => {
    setFile(null);
    setImagePreview(null);
    setRecordData(null);
    setIsLocalized(false);
    setStatusMessage('');
  };

  const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' };
    return new Date(dateString).toLocaleDateString('ro-RO', options);
  };

  if (!currentUser) {
    return <Login onLoginSuccess={setCurrentUser} />;
  }

  return (
    <div className="main-layout">
      {/* JUMATATEA STÂNGĂ */}
      <div className="left-panel">
        <h2 className="panel-title">Your image preview</h2>
        {imagePreview ? (
          <div className="image-preview-container">
            <img src={imagePreview} alt="Selected for localization" className="preview-image" />
          </div>
        ) : (
          <div className="image-placeholder">
            <p>Please select an image to preview it here.</p>
          </div>
        )}
      </div>

      {/* JUMATATEA DREAPTA */}
      <div className="right-panel">
        <div className="app-container">
          <div className="dashboard-header">
            <div>
              <h1 className="welcome-title">Welcome, {currentUser.username}!</h1>
              <h3 className="dashboard-subtitle">Localize position dashboard</h3>
            </div>
            <button onClick={logout} className="logout-btn">Logout</button>
          </div>
          
          <form onSubmit={handleUpload} className="upload-form">
            <div className="file-drop-area">
              <label>Select image from dashboard:</label>
              <div className="custom-file-upload">
                <input 
                  type="file" 
                  id="file-upload"
                  accept="image/png, image/jpeg" 
                  onChange={handleFileChange} 
                  required 
                  className="file-input-hidden"
                />
                <label htmlFor="file-upload" className="file-upload-button">
                  {file ? file.name : "Choose File"}
                </label>
              </div>
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
              <p className="hint-text">The 3D Map will open directly over this area.</p>
              
              <div className="action-buttons-group">
                <button onClick={handleView} className="action-button view-btn">
                  Open 3D Map (View Location)
                </button>
                
                <button onClick={handleReset} className="action-button reset-btn">
                  Locate New Image
                </button>
              </div>
            </div>
          )}

          {statusMessage && (
            <div className="status-message">
              {statusMessage}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;