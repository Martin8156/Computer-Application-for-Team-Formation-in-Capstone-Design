import { useState } from 'react'
import axios from "axios";
import logo from './logo.svg';
import './App.css';

function App() {
  const [groupData, setGroupData] = useState(null)

  function getData() {
    axios({
      method: "GET",
      url:"/groups",
    })
    .then((response) => {
      const res = response.data
      console.log(res)
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })}

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <p>To get your group details: </p><button onClick={getData}>Click me</button>
      </header>
    </div>
  );
}

export default App;
