import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Results from './pages/Results';
import './index.css';

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="container">
            <Link to="/" className="navbar-brand" style={{ textDecoration: 'none' }}>
              <div className="logo-icon">TVS</div>
              <span>Credit Engine</span>
            </Link>
            <ul className="navbar-nav">
              <li><Link to="/">Dashboard</Link></li>
              <li><a href="https://github.com/ananyaapoorva/tvs-credit-engine" target="_blank" rel="noopener noreferrer">GitHub</a></li>
            </ul>
          </div>
        </nav>

        <main>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/results/:scoreId" element={<Results />} />
          </Routes>
        </main>

        <footer className="footer">
          <div className="container">
            <p>Built for TVS Credit EPIC 8 Hackathon</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

// Temporary fix for Link since we're using it in the Navbar component within App
import { Link } from 'react-router-dom';

export default App;
