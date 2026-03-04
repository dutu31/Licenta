import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import { useNavigate } from 'react-router-dom';

function Upload() {
  const [file, setFile] = useState(null);
  const [formData, setFormData] = useState({
    uploaderId: '',
    roadSegment: '',
  });
  const navigate = useNavigate();
  
  const handleChange = (e) => {
    if(e.target.type === 'file') {
      setFile(e.target.files[0]);
    } else {
      setFormData({
        ...formData,
        [e.target.name]: e.target.value,
      });
    }
  };
  const handleSubmit= async (e) => {
    e.preventDefault();
    if(!file) {
      alert('Please select a file to upload');
      return;
    }
    const dataToSend = new FormData();
    dataToSend.append('file', file);
    dataToSend.append('uploaderId', formData.uploaderId);
    dataToSend.append('roadSegment', formData.roadSegment);
    
    try {
      const response = await axios.post('http://localhost:8080/api/videos/upload', dataToSend, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('File uploaded successfully! ID: ' + response.data.id);
      console.log('Response:', response.data);
      setFile(null);
      setFormData({ uploaderId: '', roadSegment: '' });
      document.getElementById('videoInput').value = '';
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file: ' + error.message);
    }
  };

  return (
    <div className="app-container">
      <h2 className="app-title">Upload new video</h2>
      
      <form onSubmit={handleSubmit} className="upload-form">

        <div style={{ display: 'flex', gap: '10px' }}>
          <button type="submit" className="submit-button" style={{ flex: 1 }}>
            Upload video
          </button>
          
          <button 
            type="button" 
            onClick={() => navigate('/catalog')} 
            className="submit-button" 
            style={{ flex: 1, backgroundColor: '#17a2b8' }}
          >
            See all videos
          </button>
        </div>
        
        <div className="file-drop-area">
          <label className="file-label">Select video file (.mp4):</label>
          <input 
            type="file" 
            id="videoInput"
            accept="video/mp4,video/x-m4v,video/*" 
            onChange={handleChange} 
            required 
          />
        </div>

        <div className="form-group">
          <label>User ID (Uploader):</label>
          <input 
            type="text" 
            name="uploaderId" 
            value={formData.uploaderId} 
            onChange={handleChange} 
            required 
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label>Road Segment:</label>
          <input 
            type="text" 
            name="roadSegment" 
            value={formData.roadSegment} 
            onChange={handleChange} 
            required 
            className="form-input"
          />
        </div>

        <button type="submit" className="submit-button">
          Upload Video
        </button>
      </form>
    </div>
  );
}

export default Upload;
