import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import axios from "axios";
import './project.css'

function Project() {
    const {projectID} = useParams();
    const navigate = useNavigate();
    const [projectData, setProjectData] = useState({EIDs: []})

    useEffect(() => {
        axios({
            method: "GET",
            url: `/project/${projectID}`  
          }).then((response) => {
            setProjectData(response.data);
            console.log(projectData)
          }).catch((error) => {
            if (error.response) {
              console.log(error.response)
              console.log(error.response.status)
              console.log(error.response.headers)
            }
        })
        console.log(projectData);
    }, []);

    function getHome() {
        navigate("/");
    }


    return (
        <div className="App">
            <header className="Base">
                <h4>Project Details for {projectID}</h4>
                <table>
                    <thead>
                        <tr>
                            <th className="projecttitle">Project</th>
                            <th className ="company">Company</th>
                            <th className="members">Members</th>
                            <th className="gpa">Avg GPA</th>
                            <th className="cost">Cost (4 -20)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td className="project" >{projectData.Project}</td>
                            <td className ="company">{projectData.Company}</td>
                            <td className="members">{projectData.EIDs.join(", ")}</td>
                            <td className="gpa">{projectData["Avg GPA"]}</td>
                            <td className="cost">{projectData["Cost"]}</td>
                        </tr>
                    </tbody>
                </table>
                <button onClick={() => getHome()}>Return</button>
            </header>
        </div>
    );
}

export default Project;