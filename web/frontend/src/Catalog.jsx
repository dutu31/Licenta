import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './App.css';

function Catalog() {
  const [videos, setVideos] = useState([]);
  const navigate = useNavigate();
    useEffect(() => {
        fetchVideos();
    }, []);
        const fetchVideos = async () => {
            try {
                const response = await axios.get('http://localhost:8080/api/videos');
                setVideos(response.data);
            } catch (error) {
                console.error('Error fetching videos:', error);
                alert('Error fetching videos: ' + error.message);
            }
        };
        return (
            <div className="app-container" style={{ maxWidth: '800px' }}>
      <h2 className="app-title">Videos</h2>
      
      
      <button 
        onClick={() => navigate('/')} 
        className="submit-button" 
        style={{ marginBottom: '20px', backgroundColor: '#6c757d' }}
      >
        Back to upload
      </button>

      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
          <thead>
            <tr style={{ backgroundColor: '#f2f2f2', textAlign: 'left' }}>
              <th style={{ padding: '12px', borderBottom: '2px solid #ddd' }}>ID</th>
              <th style={{ padding: '12px', borderBottom: '2px solid #ddd' }}>File name</th>
              <th style={{ padding: '12px', borderBottom: '2px solid #ddd' }}>Uploader</th>
              <th style={{ padding: '12px', borderBottom: '2px solid #ddd' }}>Road segment</th>
              <th style={{ padding: '12px', borderBottom: '2px solid #ddd' }}>Status</th>
            </tr>
          </thead>
          <tbody>
            {videos.length === 0 ? (
              <tr>
                <td colSpan="5" style={{ padding: '15px', textAlign: 'center' }}>No uploaded videos.</td>
              </tr>
            ) : (
              videos.map((video) => (
                <tr key={video.id} style={{ borderBottom: '1px solid #ddd' }}>
                  <td style={{ padding: '12px' }}>{video.id}</td>
                  <td style={{ padding: '12px' }}>{video.originalFilename}</td>
                  <td style={{ padding: '12px' }}>{video.uploaderId}</td>
                  <td style={{ padding: '12px' }}>{video.roadSegment}</td>
                  <td style={{ padding: '12px' }}>
                    
                    <span style={{ 
                      padding: '5px 10px', 
                      borderRadius: '15px', 
                      fontSize: '12px',
                      backgroundColor: video.isProcessed ? '#d4edda' : '#fff3cd',
                      color: video.isProcessed ? '#155724' : '#856404'
                    }}>
                      {video.isProcessed ? 'Processed' : 'Pending'}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
        );
    }
    export default Catalog;