import { useState } from 'react'
import { useNavigate } from 'react-router-dom';
import axios from "axios";
import './Home.css';

function Home() {
  const navigate = useNavigate();
  const [groupData, setGroupData] = useState([])

  function getSheet() {
    axios({
      method: "GET",
      url: "/get_excel"
    })
    .catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
      }
    })
  }

  function getData() {
    axios({
      method: "GET",
      url:"/groups",
    })
    .then((response) => {
      const res = response.data;
      console.log(res);
      setGroupData(res);
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
      }
    })}

    function getProject(projectID) {
      navigate(`/project/${projectID}`);
    }

  return (
    <div className="Base">
      <header> To get your group details:</header>
      <body>
        <button onClick={getData}>Show Groups</button>
        <button onClick={getSheet}>Download Excel Spreadsheet of Groups</button>
        <table>
          <thead>
            <tr>
              <th>ID</th> 
              <th className="projecttitle">Project</th>
              <th className ="company">Company</th>
              <th className="members">Members</th>
              <th className="gpa">Avg GPA</th>
            </tr>
          </thead>
          <tbody>
            {groupData.map((val, proj) => {
              return (
                <tr key={proj}>
                  <td className="id" onClick={() => (getProject(val.ID))}> {val.ID}</td>
                  <td className="project" >{val.Project}</td>
                  <td className ="company">{val.Company}</td>
                  <td className="members">{val.EIDs.join(", ")}</td>
                  <td className="gpa">{val["Avg GPA"]}</td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </body>
    </div>
  );
}

export default Home;
