import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom';
import axios from "axios";

function Project() {
    const [projectData, setProjectData] = useState([])
    const {projectID} = useParams();

    useEffect(() => {
        axios({
            method: "GET",
            url: `project/${projectID}`  
          }).then((response) => {
            setProjectData(response.data);
          }).catch((error) => {
            if (error.response) {
              console.log(error.response)
              console.log(error.response.status)
              console.log(error.response.headers)
              }
          })
    }, []);

    return (
        <div className="App">
            <header className="Base">
                <p>Project Details for {projectID}</p>
                <td>{projectData["Company"]}</td>
                <td>{projectData["Members"]}</td>
            </header>
        </div>
    );
}

export default Project;