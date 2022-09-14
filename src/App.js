import { useState } from 'react'
import axios from "axios";
import './App.css';
import {CardContent, Typography, Box, Grid} from '@material-ui/core';
import Card from 'react-bootstrap/Card';

function App() {

  const [username, setName] = useState()
  const [repositoryData, setRepoData] = useState(null)

  let handleSubmit = async (event) => {
    event.preventDefault();
    getData();
 };


  function getData() {
  console.log(username)
    axios({
      method: "GET",
      url:"/home/" +username,
    })
    .then((response) => {
      const repositoryData = response.data
      setRepoData(response.data)
      console.log(repositoryData)
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        }
    })
  }


  return (
    <div>
      <header> 
      <form onSubmit = {handleSubmit}>
          <label> Enter Github Username :
              <input type = "text" id = "name" name = "githubUsername" onChange = {(e) => setName(e.target.value)} />
          </label>
      <p>To get your repository details: </p><button type ="submit">Click here</button>
        </form>

        {repositoryData && (
          <div> 
            {repositoryData.map((repo) => (
              <div className="grid"> 
              <Card style={{ width: '18rem' }} key ={repo[0]}>
                <Card.Body>
                  <Card.Title>{repo[1]}</Card.Title>
                  <Card.Text>
                    View details
                  </Card.Text>
                </Card.Body>
              </Card>
              </div>
            )) }
          </div>
              // <Grid item xs={4} sx={{backgroundColor: "#1B9CB3"}}>
              // // <Box sx={{ bgcolor: '#987653', p: 10 }} key={repo[0]}>
              // {/* <Card variant="outlined" elevation={3}> */}
              //     {/* <CardContent> */}
              //       {/* <Typography key={repo[0]} sx={{margin: 2, wordBreak: "break-word", lineHeight: .8, color: "white"}} inline variant="caption"> */}
              //             //  {repo[1]}
              //       {/* </Typography> */}
              //     {/* </CardContent> */}
              //   {/* // </Card> */}
              //   {/* // </Grid> */}
              //   // </Box>
            // ))}
        )}
      </header>
    </div>
  );
}

export default App;