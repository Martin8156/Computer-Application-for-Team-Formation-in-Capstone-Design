import { useState } from 'react'
import axios from "axios";
import logo from './logo.svg';
import './App.css';

function App() {
  const [groupData, setGroupData] = useState([])

  function getData() {
    axios({
      method: "GET",
      url:"/groups",
    })
    .then((response) => {
      const res = response.data;
      setGroupData(res)
      console.log(groupData)
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })}

  return (
    <div className="App">
      <header className="Base">
        <p>To get your group details: </p><button onClick={getData}>Click me</button>
        <table>
          <thead>
            <tr>
              <th>Project</th>
              <th>Company</th>
              <th>Members</th>
            </tr>
          </thead>
          <tbody>
            {groupData.map((val, proj) => {
              return (
                <tr key={proj}>
                  <td>{val.Project}</td>
                  <td>{val.Company}</td>
                  <td>{val.Members}</td>
                </tr>
              )
            })}
          </tbody>
      </table>
      </header>
    </div>
  );
}

export default App;
