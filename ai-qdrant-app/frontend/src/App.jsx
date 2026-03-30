import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!query) return;
    setLoading(true);
    try {
      // Ensure this URL matches your FastAPI backend
      const res = await axios.get(`http://localhost:8000/api/search?q=${query}`);
      setResults(res.data);
    } catch (err) {
      console.error("SYSTEM_ERROR:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ backgroundColor: '#000', color: '#0f0', minHeight: '100vh', padding: '40px', fontFamily: 'monospace' }}>
      <header style={{ borderBottom: '1px solid #050', marginBottom: '20px', paddingBottom: '10px' }}>
        <h1 style={{ fontSize: '1.5rem', letterSpacing: '2px' }}>[ SYSTEM_AI_SEARCH_v1.0 ]</h1>
      </header>
      
      <div style={{ display: 'flex', gap: '10px', marginBottom: '30px' }}>
        <input 
          style={{ 
            background: '#000', border: '1px solid #0f0', color: '#0f0', 
            padding: '12px', flex: 1, outline: 'none', fontSize: '16px' 
          }}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          placeholder="ENTER_QUERY_PROMPT..."
        />
        <button 
          onClick={handleSearch}
          style={{ 
            background: '#0f0', color: '#000', fontWeight: 'bold', 
            padding: '0 25px', cursor: 'pointer', border: 'none', transition: '0.2s'
          }}
        >
          {loading ? 'EXECUTING...' : 'SEARCH'}
        </button>
      </div>

      <div className="results-container">
        {results.length > 0 ? (
          results.map((item, index) => (
            <div key={index} style={{ borderLeft: '3px solid #050', padding: '15px', marginBottom: '20px', backgroundColor: '#0501' }}>
              <p style={{ color: '#fff', margin: '0 0 10px 0' }}>{item.text}</p>
              <div style={{ color: '#0a0', fontSize: '12px' }}>MATCH_CONFIDENCE: {(item.score * 100).toFixed(2)}%</div>
            </div>
          ))
        ) : (
          <p style={{ opacity: 0.5 }}>READY_FOR_INPUT_</p>
        )}
      </div>
    </div>
  );
}

export default App;