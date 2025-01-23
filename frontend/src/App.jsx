import React, { useEffect, useState } from 'react';
import axios from 'axios';

const App = () => {
  const [message, setMessage] = useState('');

  useEffect(() => {
    axios.get('/api/hello')
      .then(response => {
        setMessage(response.data.message);
      })
      .catch(error => {
        console.error('There was an error fetching the message!', error);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>CS 348 Group Project</h1>
        <p>{message || 'Loading...'}</p>
      </header>
    </div>
  );
}

export default App
