import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router } from 'react-router-dom';
import { UserProvider } from './components/UserContext';
import App from './App';
import './index.css';
import './satoshi.css';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <Router>
      <UserProvider>  {/* <-- Use the UserProvider as a wrapper */}
        <App />
      </UserProvider>
    </Router>
  </React.StrictMode>
);
