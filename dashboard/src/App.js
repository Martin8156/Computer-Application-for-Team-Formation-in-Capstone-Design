import {BrowserRouter as Router, Routes, Route, Link} from "react-router-dom"
import './App.css';
import Home from './components/home';
import Project from './components/project';

function App() {
  return (
    <div className="App">
    <header className="App-header">
     <Router>
        <div>
        <switch>
          <Routes>
              <Route exact path="/" element={<Home></Home>} />
              <Route path="/project/:projectID" element={<Project></Project>} />
          </Routes>
        </switch>
        </div>
      </Router>
    </header>
  </div>
  );
}

export default App;