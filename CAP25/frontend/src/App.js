import React, { useState, useEffect } from 'react';
import './App.css';

// Helper function to compute the lowest satisfactory score for a group
function getLowestSatScore(project, studentIndices, matchingData) {
  const allocatedStudents = studentIndices.map(idx => matchingData.students[idx]);
  // Calculate the sat score for each skill required by the project
  const satScores = Object.keys(project.skill_req).map(key => {
    const projectReq = project.skill_req[key];
    const totalStudentSkill = allocatedStudents.reduce(
      (sum, student) => sum + (student.skill_set[key] || 0),
      0
    );
    return projectReq > 0 ? totalStudentSkill / projectReq : 0;
  });
  return satScores.length > 0 ? Math.min(...satScores) : 0;
}

function TeamDetails({ project, studentIndices, matchingData }) {
  // Gather allocated students from indices
  const allocatedStudents = studentIndices.map(idx => matchingData.students[idx]);

  // Build an array of column objects based on the project's skill requirements
  const skillColumns = Object.keys(project.skill_req).map(key => {
    const projectReq = project.skill_req[key];
    const totalStudentSkill = allocatedStudents.reduce((sum, student) => {
      return sum + (student.skill_set[key] || 0);
    }, 0);
    const satScore = projectReq > 0 ? (totalStudentSkill / projectReq) : 0;
    const skillName = matchingData.skills[key] || `Skill ${key}`;
    return { skillIndex: key, skillName, projectReq, totalStudentSkill, satScore };
  });

  // Sort the skills (columns) by satisfactory score (ascending)
  skillColumns.sort((a, b) => a.satScore - b.satScore);

  return (
    <div className="match-group">
      <h3>Team: {project?.name || 'Unnamed Project'}</h3>
      {/* Container to allow horizontal scrolling */}
      <div className="table-container">
        <table className="team-table">
          <thead>
            <tr>
              {/* Empty header cell for row labels */}
              <th></th>
              {/* Render header cells for each sorted skill */}
              {skillColumns.map(col => (
                <th key={col.skillIndex}>{col.skillName}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {/* Render a row for each allocated student with their name in the first column */}
            {allocatedStudents.map((student, studentIdx) => (
              <tr key={studentIdx}>
                <td className="row-label">{student.name}</td>
                {skillColumns.map(col => (
                  <td key={col.skillIndex}>
                    {student.skill_set[col.skillIndex] || 0}
                  </td>
                ))}
              </tr>
            ))}
            {/* Row for Total Student Skills */}
            <tr>
              <td className="row-label"><strong>Total Skills</strong></td>
              {skillColumns.map(col => (
                <td key={col.skillIndex}>
                  <strong>{col.totalStudentSkill}</strong>
                </td>
              ))}
            </tr>
            {/* Row for Project Requirements */}
            <tr>
              <td className="row-label"><em>Project Requirement</em></td>
              {skillColumns.map(col => (
                <td key={col.skillIndex}>
                  <em>{col.projectReq}</em>
                </td>
              ))}
            </tr>
            {/* Row for Satisfactory Score */}
            <tr>
              <td className="row-label"><strong>Satisfactory Score</strong></td>
              {skillColumns.map(col => (
                <td key={col.skillIndex}>
                  {col.satScore.toFixed(2)}
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}

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

  // Polling for updated match results
  useEffect(() => {
    const pollInterval = setInterval(async () => {
      try {
        const response = await fetch('http://localhost:8888/match');
        const data = await response.json();
        if (data && Object.keys(data).length > 0) {
          setMatchingData(data);
        }
      } catch (err) {
        console.error('Error fetching match data:', err);
      }
    }, 2000);

    return () => clearInterval(pollInterval);
  }, []);

  const fetchMatchingData = async () => {
    try {
      const response = await fetch('http://localhost:8888/matching', {
        method: 'POST'
      });
      const text = await response.text();
      console.log('Received raw data:', text);
      try {
        const data = JSON.parse(text);
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

  // Determine which students have not been allocated
  const allocatedSet = new Set();
  if (matchingData?.matching) {
    Object.values(matchingData.matching).forEach(arr => {
      arr.forEach(studentIdx => allocatedSet.add(studentIdx));
    });
  }
  const unallocatedStudents = matchingData?.students?.filter((_, idx) => !allocatedSet.has(idx)) || [];

  // Create an array of groups with their computed lowest sat score
  const groups = matchingData?.matching
    ? Object.entries(matchingData.matching).map(([projectIndex, studentIndices]) => {
        const project = matchingData.projects[projectIndex];
        const lowestSat = getLowestSatScore(project, studentIndices, matchingData);
        return { projectIndex, studentIndices, lowestSat };
      })
    : [];

  // Sort groups in ascending order of lowest sat score
  groups.sort((a, b) => a.lowestSat - b.lowestSat);

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
            <button onClick={handleSolverStart} className="solve-button" disabled={isLoading}>
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
          {uploadStatus && (
            <div className="download-section">
              <button onClick={handleDownloadCSV} className="download-button" disabled={!matchingData || !matchingData.matching}>
                Download CSV Output
              </button>
            </div>
          )}
        </section>
        <section className="matching-data">
          <h2>Current Matching Results</h2>
          {matchingData?.matching ? (
            <div className="matches-container">
              {groups.map(({ projectIndex, studentIndices }) => {
                const project = matchingData.projects[projectIndex];
                return (
                  <TeamDetails
                    key={projectIndex}
                    project={project}
                    studentIndices={studentIndices}
                    matchingData={matchingData}
                  />
                );
              })}
              <div className="unallocated-students">
                <h3>Students Not Yet Allocated</h3>
                {unallocatedStudents.length > 0 ? (
                  <ul>
                    {unallocatedStudents.map((student, idx) => (
                      <li key={idx}>
                        {student.name} ({student.eid})
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p>All students have been allocated!</p>
                )}
              </div>
            </div>
          ) : (
            <p>No matching results available</p>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
