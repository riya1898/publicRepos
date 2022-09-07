import { useState } from 'react'
import axios from "axios";
import './App.css';

function App() {

  const [repositoryData, setRepoData] = useState(null)

  function getData() {
    axios({
      method: "GET",
      url:"/home",
    })
    .then((response) => {
      const res = response.data
      setRepoData(response.data)
      console.log("res", res)
      console.log(repositoryData)
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        }
    })}

  return (
    <div className="App">
      <header className="App-header">        
        <p>To get your repository details: </p><button onClick={getData}>Click here</button>
        { repositoryData && (
          <ul>
            {repositoryData.map(repo => (
              <li key={repo[0]}>{repo[1]}</li>
            ))}
          </ul>
        )}
      </header>
    </div>
  );
}

export default App;