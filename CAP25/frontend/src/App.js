import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [matchingData, setMatchingData] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [solverStatus, setSolverStatus] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [filesUploaded, setFilesUploaded] = useState({
    student: false,
    company: false
  });

  useEffect(() => {
    fetchMatchingData();
  }, []);

  const fetchMatchingData = async () => {
    try {
      const response = await fetch('http://localhost:8888/matching', {
        method: 'POST'
      });
      const text = await response.text(); // First get the raw text
      console.log('Received raw data:', text); // Log the raw response
      
      try {
        const data = JSON.parse(text); // Then try to parse it
        console.log('Parsed matching data:', data);
        if (data && Object.keys(data).length > 0) {
          setMatchingData(data);
        }
      } catch (parseError) {
        console.error('Error parsing JSON:', parseError);
        setMatchingData(null);
      }
    } catch (error) {
      console.error('Error fetching matching data:', error);
      setMatchingData(null);
    }
  };

  const handleFileUpload = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    const formData = new FormData(event.target);
    const fileType = formData.get('file_type');
    
    try {
      const response = await fetch('http://localhost:8888/file/upload', {
        method: 'POST',
        body: formData
      });
      const result = await response.text();
      setUploadStatus(result);
      
      // Update the filesUploaded state
      setFilesUploaded(prev => ({
        ...prev,
        [fileType.toLowerCase()]: true
      }));
    } catch (error) {
      console.error('Error:', error);
      setUploadStatus('Upload failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSolverStart = async () => {
    setIsLoading(true);
    try {
      const solverResponse = await fetch('http://localhost:8888/action/solve', {
        method: 'POST'
      });
      const solverResult = await solverResponse.json();
      setSolverStatus(solverResult.msg);

      if (solverResult.result === 'success') {
        setSolverStatus('Solver running...');
        let attempts = 0;
        const maxAttempts = 15;
        
        const pollInterval = setInterval(async () => {
          try {
            console.log('Polling for results...');
            const response = await fetch('http://localhost:8888/matching', {
              method: 'POST'
            });
            const text = await response.text();
            console.log('Received raw polling data:', text);
            
            try {
              const data = JSON.parse(text);
              console.log('Parsed polling data:', data);
              
              if (data && data.matching && Object.keys(data.matching).length > 0) {
                console.log('Found matching results:', data.matching);
                setMatchingData(data);
                setSolverStatus('Matching complete!');
                clearInterval(pollInterval);
              } else {
                attempts++;
                if (attempts >= maxAttempts) {
                  clearInterval(pollInterval);
                  setSolverStatus('Solver timed out. Please try again.');
                }
              }
            } catch (parseError) {
              console.error('Error parsing JSON:', parseError);
              attempts++;
              if (attempts >= maxAttempts) {
                clearInterval(pollInterval);
                setSolverStatus('Invalid data received. Please try again.');
              }
            }
          } catch (error) {
            console.error('Error polling for results:', error);
            attempts++;
            if (attempts >= maxAttempts) {
              clearInterval(pollInterval);
              setSolverStatus('Solver failed. Please try again.');
            }
          }
        }, 2000);
      }
    } catch (error) {
      console.error('Error:', error);
      setSolverStatus('Solver failed to start');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Project Matching System</h1>
      </header>
      
      <main>
        <section className="upload-section">
          <h2>Upload CSV Files</h2>
          <form onSubmit={handleFileUpload}>
            <div className="upload-controls">
              <input type="file" name="filearg" accept=".csv" required />
              <select name="file_type" required>
                <option value="">Select file type...</option>
                <option value="Student">Student Preference</option>
                <option value="Company">Company Preference</option>
              </select>
              <button type="submit">Upload</button>
            </div>
          </form>
          
          <div className="file-status">
            <p>Student File: {filesUploaded.student ? '✅ Uploaded' : '❌ Not uploaded'}</p>
            <p>Company File: {filesUploaded.company ? '✅ Uploaded' : '❌ Not uploaded'}</p>
          </div>

          {filesUploaded.student && filesUploaded.company && (
            <button 
              onClick={handleSolverStart}
              className="solve-button"
              disabled={isLoading}
            >
              Start Matching
            </button>
          )}

          {uploadStatus && <p className="status-message">{uploadStatus}</p>}
          {solverStatus && <p className="status-message">{solverStatus}</p>}
          {isLoading && (
            <div className="loading-indicator">
              <p>Processing...</p>
            </div>
          )}
        </section>

        <section className="matching-data">
          <h2>Current Matching Results</h2>
          {matchingData?.matching ? (
            <ul>
              {Object.entries(matchingData.matching).map(([projectIndex, studentIndices]) => {
                const project = matchingData.projects[projectIndex];
                return (
                  <li key={projectIndex} className="project-match">
                    <strong>Project: {project?.name || `Project ${projectIndex}`}</strong>
                    <ul className="student-list">
                      {studentIndices.map(studentIndex => {
                        const student = matchingData.students[studentIndex];
                        return (
                          <li key={studentIndex} className="student-item">
                            {student?.name || `Student ${studentIndex}`}
                          </li>
                        );
                      })}
                    </ul>
                  </li>
                );
              })}
            </ul>
          ) : (
            <p>No matching results available</p>
          )}
        </section>
      </main>
    </div>
  );
}

export default App; 