import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Upload from './Upload';
import Catalog from './Catalog';

function App() {
  return (
    <Router>
      <Routes>
        
        <Route path="/" element={<Upload />} />
        <Route path="/catalog" element={<Catalog />} />
      </Routes>
    </Router>
  );
}

export default App;