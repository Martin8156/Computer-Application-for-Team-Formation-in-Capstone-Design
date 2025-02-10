import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [matchingData, setMatchingData] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  useEffect(() => {
    fetchMatchingData();
  }, []);

  const fetchMatchingData = async () => {
    try {
      const response = await fetch('http://localhost:8888/matching', {
        method: 'POST'
      });
      const data = await response.json();
      setMatchingData(data);
    } catch (error) {
      console.error('Error fetching matching data:', error);
    }
  };

  const handleFileUpload = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.target);
    
    try {
      const response = await fetch('http://localhost:8888/file/upload', {
        method: 'POST',
        body: formData
      });
      const result = await response.text();
      setUploadStatus(result);
    } catch (error) {
      console.error('Error uploading file:', error);
      setUploadStatus('Upload failed');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Project Matching System</h1>
      </header>
      
      <main>
        <section className="upload-section">
          <h2>Upload CSV File</h2>
          <form onSubmit={handleFileUpload}>
            <input type="file" name="filearg" accept=".csv" />
            <button type="submit">Upload</button>
          </form>
          {uploadStatus && <p>{uploadStatus}</p>}
        </section>

        <section className="matching-data">
          <h2>Current Matching Data</h2>
          {matchingData && (
            <div>
              <h3>Skills</h3>
              <ul>
                {Object.entries(matchingData.skills).map(([key, skill]) => (
                  <li key={key}>{skill}</li>
                ))}
              </ul>

              <h3>Students</h3>
              <ul>
                {matchingData.students.map((student, index) => (
                  <li key={index}>
                    {student.name} (EID: {student.eid})
                    <br />
                    Skills: {Object.entries(student.skill_set).map(([skillId, skillValue]) => matchingData.skills[skillId]).join(', ')}
                  </li>
                ))}
              </ul>

              <h3>Projects</h3>
              <ul>
                {matchingData.projects.map((project, index) => (
                  <li key={index}>
                    {project.name}
                    <br />
                    Required Skills: {Object.entries(project.skill_req).map(skillId => matchingData.skills[skillId]).join(', ')}
                  </li>
                ))}
              </ul>
              
              <h4>Matching</h4>
              <ul>
                {Object.entries(matchingData.matching).map(([projectIndex, studentIndices]) => (
                  <li key={projectIndex}>
                    <strong>{matchingData.projects[projectIndex].name}</strong>
                    <ul>
                      {studentIndices.map(studentIndex => (
                        <li key={studentIndex}>
                          {matchingData.students[studentIndex].name} (EID: {matchingData.students[studentIndex].eid})
                        </li>
                      ))}
                    </ul>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App; 