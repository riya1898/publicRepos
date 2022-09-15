import { useState } from 'react'
import axios from "axios";
import './App.css';
import * as React from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';


const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));

function App() {

  const [username, setName] = useState()
  const [repositoryData, setRepoData] = useState(null)
  var pageNumber = 0

  let handleSubmit = async (event) => {
    event.preventDefault();
    getData("d");
 };


  function getData(pageLabel) {
  console.log(username)
    axios({
      method: "GET",
      url:"/home?uname=" +username+ "&&page=" +pageLabel,
    })
    .then((response) => {
      console.log("inside response")
      const repositoryData = response.data
      setRepoData(response.data)
      console.log(repositoryData)
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        }
    })
  }

  function next() {
    getData("n")
  }

  function previous() {
      getData("p")
  }


  return (
    <div style = {{backgroundColor: "#a9a9a9"}}>
      <header>
      <Box component="span" sx={{
        width: '100%',
        height: 300,
        backgroundColor: 'black',}}>
        Welcome!
      </Box> 
      <form onSubmit = {handleSubmit}>
          <label> Enter Github Username :
              <input type = "text" id = "name" name = "githubUsername" onChange = {(e) => setName(e.target.value)} />
          </label>
        <p>To get your repository details: </p><button type ="submit">Click here</button>
      </form>

        <button onClick ={next}> Next </button> 
        <button onClick = {previous}> Previous </button>

        { repositoryData && (
        <Box sx={{ flexGrow: 1 }}>
          <Grid container spacing={2} style= {{ padding: '25px 25px'}}>
          { repositoryData.map((repo) =>  { return (    
            <Grid item xs={4} md ={3} >
            <Card sx={{ maxWidth: 345 }}>
                <CardContent>
                  <Typography gutterBottom variant="h5" component="div">
                    {repo[2]}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Lizards are a widespread group of squamate reptiles, with over 6,000
                    species, ranging across all continents except Antarctica
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button size="small">Share</Button>
                  <Button size="small">Learn More</Button>
                </CardActions>
              </Card>
            </Grid>
            ) } ) }
          </Grid>
        </Box>
        )}
      </header>
    </div>
  );
}

export default App;