import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';
import axios from "axios";

function Project() {
    const [projectData, setProjectData] = useState([])
    const {projectID} = useParams();
    const navigate = useNavigate();

    useEffect(() => {
        axios({
            method: "GET",
            url: `/project/${projectID}`  
          }).then((response) => {
            setProjectData(response.data);
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
                <p>Project Details for {projectID}</p>
                <table>
                    <thead>
                        <tr>
                            <th>Company</th>
                            <th>Members</th>
                        </tr>
                    </thead>
                    <tbody>
                        <td>{projectData["Company"]}</td>
                        <td>{projectData["Members"]}</td>
                    </tbody>
                </table>
                <button onClick={() => getHome()}>Return</button>
            </header>
        </div>
    );
}

export default Project;