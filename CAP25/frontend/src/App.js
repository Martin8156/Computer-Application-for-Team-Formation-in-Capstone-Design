import React, { useState, useEffect, useRef } from 'react'; // Added useRef
import './App.css';
import { use } from 'react';

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

  useEffect(() => {
    fetchMatchData();
  }, []);

  // Global ref for the matching poll interval (if needed)
  const pollMatchIntervalRef = useRef(null);
  // Global ref for the solver polling interval
  const solverPollingIntervalRef = useRef(null);

  // useEffect(() => {
  //   pollMatchIntervalRef.current = setInterval(async () => {
  //     try {
  //       const response = await fetch('http://localhost:8888/match');
  //       const data = await response.json();
  //       if (data && Object.keys(data).length > 0) {
  //         setMatchingData(data);
  //       }
  //     } catch (err) {
  //       console.error('Error fetching match data:', err);
  //     }
  //   }, 2000);

  //   return () => clearInterval(pollMatchIntervalRef.current);
  // }, []);

  const fetchMatchData = async () => {
    try {
      const response = await fetch('http://localhost:8888/match');
      const data = await response.json();
      if (data && Object.keys(data).length > 0) {
        setMatchingData(data);
      }
    } catch (err) {
      console.error('Error fetching match data:', err);
    }
  };
    
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
        
        pollMatchIntervalRef.current = setInterval(() => {
          fetchMatchData();
        }
        , 2000);
        
        // Store the polling interval in solverPollingIntervalRef
        solverPollingIntervalRef.current = setInterval(async () => {
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
              } else {
                attempts++;
                if (attempts >= maxAttempts) {
                  clearInterval(solverPollingIntervalRef.current);
                  setSolverStatus('Solver timed out. Please try again.');
                }
              }
            } catch (parseError) {
              console.error('Error parsing JSON:', parseError);
              attempts++;
              if (attempts >= maxAttempts) {
                clearInterval(solverPollingIntervalRef.current);
                setSolverStatus('Invalid data received. Please try again.');
              }
            }
          } catch (error) {
            console.error('Error polling for results:', error);
            attempts++;
            if (attempts >= maxAttempts) {
              clearInterval(solverPollingIntervalRef.current);
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

  // Kill function to terminate the solver polling interval
  const handleKill = async () => {
    try {
      const response = await fetch('http://localhost:8888/action/kill', {
        method: 'POST'
      });
      const res = await response.json();
      setSolverStatus(res.msg);
    } catch (error) {
      console.error('Error killing backend solver:', error);
      setSolverStatus('Error terminating solver');
    }
  
    if (solverPollingIntervalRef.current) {
      clearInterval(solverPollingIntervalRef.current);
      //solverPollingIntervalRef.current = null;
    }
    if(pollMatchIntervalRef.current) {
      clearInterval(pollMatchIntervalRef.current);
      //pollMatchIntervalRef.current = null;
    }
  };

  const handleDownloadCSV = async () => {
    try {
      const response = await fetch('http://localhost:8888/action/output-csv');
      console.log('Download response:', response);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const blob = await response.blob();
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "data.csv";
      document.body.appendChild(a);
      a.click();
      
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading CSV:', error);
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
            <>
              <button 
                onClick={handleSolverStart}
                className="solve-button"
                disabled={isLoading}
              >
                Start Matching
              </button>

              <button 
                onClick={handleKill}
                className="kill-button"
                //disabled={!solverPollingIntervalRef.current}
                style={{ marginLeft: "1rem" }} // Added inline spacing
              >
                Stop Solver
              </button>
            </>
          )}

          {uploadStatus && <p className="status-message">{uploadStatus}</p>}
          {solverStatus && <p className="status-message">{solverStatus}</p>}
          {isLoading && (
            <div className="loading-indicator">
              <p>Processing...</p>
            </div>
          )}

          {uploadStatus && (
            <div className="download-section">
              <button 
                onClick={handleDownloadCSV} 
                className="download-button"
                disabled={!matchingData || !matchingData.matching}
              >
                Download CSV Output
              </button>
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
                            {student?.eid && `(${student.eid})`}
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