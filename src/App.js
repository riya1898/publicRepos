import { useState, useEffect } from 'react'
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
import dayjs from 'dayjs';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker'
import { Input } from '@mui/material';

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
  const [date, setDate] = useState(dayjs('1970-01-011T21:11:54'));
  const [searchInput, setSearchInput] = useState('');
  const [filteredResults, setFilteredResults] = useState([]);
  const [errorCode, errorData] =useState(0)
  
  let handleSubmit = async (event) => {
    event.preventDefault();
    getData("d", date);
 };


//  const handleChange = (newValue) => {
//   setDate(newValue);
//   console.log(newValue)
//   date = JSON.stringify(newValue)
//   console.log(date)
//   // getData("d")
// };

const searchItems = (searchValue) => {
  setSearchInput(searchValue)
  console.log(searchValue)
  if(repositoryData !== '' && searchInput!== '') {
    const filteredData = repositoryData.filter((item) => {
      console.log(item.repositoryName)
      return Object.values(item.repositoryName).join('').toLowerCase().includes(searchInput.toLowerCase())
      })
      console.log(filteredData)
      setRepoData(filteredData)
  }
  else
      setRepoData(repositoryData)
}

  function getData(pageLabel, date) {
  console.log(username)
  console.log(date)
    axios({
      method: "GET",
      url:"/home?uname=" +username+ "&&page=" +pageLabel+ "&&date=" +date
    })
    .then((response) => {
      errorData(response.status)
      if(response.status == 200) {
        const repositoryData = response.data
        setRepoData(repositoryData)
        errorCode = 200
        setName(repositoryData.name)
        console.log(response.status)
      }
    }, (error) => {
      console.log(error.response)
      errorCode = error.response.status
      errorData(error.response.status)
      console.log(errorCode)

    }).catch((error) => {
      console.log(error)
      if (error.response) {
        console.log(error.response)
        errorCode = error.response.status
        console.log(errorCode)
        errorData(error.response.status)
        console.log("Reaching end of line")
        }
    })
    console.log(errorCode)
    console.log("Ending function call")
  }

  
  function next() {
      getData("n", date)
  }

  function previous() {
      getData("p", date)
  }


  return (
    
    <div style = {{backgroundColor: "#140005"}}>
      <Box sx={{ flexGrow: 1 }}>
          <Grid container spacing={2} style= {{ padding: '25px 25px'}}>
          <Grid item xs={12} md ={12} >
          <Box component="span" sx={{
            width: '100%',
            height: 300,
            textAlign: 'center',
            fontSize: '30px'}}>
            <h1 style={{ color: 'white'}}>Welcome!</h1>
          </Box> 
          </Grid>

          {/* <Grid item xs={3} md ={3} style = {{backgroundColor: "#FFFFFF"}} >
          <LocalizationProvider dateAdapter={AdapterDayjs} color = "#FFFFFF">
            <Stack spacing={3}>
              <DesktopDatePicker
                label="Date desktop"
                inputFormat="MM/DD/YYYY"
                views={["year", "month", "day"]}
                value={date}
                onChange= {(e) => setDate(e.target.value)}
                format="DD-MM-YYYY"
                defaultValue = "10-10-1970"
                // value={value}
                // onChange={handleChange}
                renderInput={(params) => <TextField {...params} />}
                sx={{ backgroundColor: 'white' }}
              />
              </Stack>
          </LocalizationProvider>
          </Grid> */}

          <Grid item xs={6} md ={6}style = {{ marginBottom:'30px'}} >
          <form onSubmit = {handleSubmit}>
              <h2 style={{color:'white', marginRight:'10px'}}> Enter Github Username 
                  <input style = {{ height: '25px', borderRadius:'5px', marginLeft:'10px'}} type = "text" id = "name" name = "githubUsername" onChange = {(e) => setName(e.target.value)} required />
            </h2>

            <h2 style={{color:'white', marginRight:'10px'}}> Repository Created After
                  <input style = {{ height: '25px', borderRadius:'5px', marginLeft:'10px'}} type = "date" id = "date" name = "date"  onChange = {(e) => setDate(e.target.value)} required />
            </h2>
            <button  style = {{ height: '35px', borderRadius:'5px'}} type ="submit">Get repository details</button>
          </form>
          </Grid>
          
          <Grid item xs={6} md ={6} style = {{ textAlign:'right', marginBottom: '40px'}}>
            <a style ={{ backgroundColor: "#FFFFFF", fontSize: "14px", marginRight:'30px'}} href="https://api.github.com/users" target="_blank">List of Github usernames</a>
            <br></br>
          <Input style = {{ height: '30px',  width : '220px', borderRadius:'5px', margin:' 20px 30px', fontSize:'14px',  backgroundColor: "#FFFFFF"}}
                icon='search'
                placeholder='Search by repository name'
                onChange={(e) => searchItems(e.target.value)}
            />
         <br></br>
        <button  style = {{ height: '30px', width : '80px', borderRadius:'5px', marginLeft:'10px', marginRight:'15px'}} onClick ={previous}> Previous</button> 
        <button  style = {{ height: '30px', width: '80px', borderRadius:'5px', marginRight:'30px',}} onClick = {next}> Next </button>
        </Grid>
    
        { repositoryData &&   ( repositoryData.map((repo) =>  { return (    
            <Grid item xs={4} md ={3} >
            <Card sx={{ maxWidth: 345, height: '16vw' }}>
                <CardContent>
                  <Typography gutterBottom variant="h5" component="div">
                    {repo.repositoryName}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {repo.description}
                  </Typography>
                </CardContent>
                <CardActions style = {{ marginTop:"auto"}}>
                <Button style ={{backgroundColor:"#464033"}} size="small" variant="contained" href = {repo.repoURL} target="_blank">  Learn More </Button>
                </CardActions>
              </Card>
            </Grid>
            ) } )
        ) 
      }  
       { errorCode != 200 &&
       (
          <Grid item xs={12} md ={12} >
          <Card sx={{ height: '3vw', textAlign: 'çenter'}}>
              <CardContent>
                <label> Enter a github username </label>
                <label> Or click the link above to check usernames </label>
              </CardContent>
            </Card>
          </Grid>
       )
       }
        
        
          {/* { searchInput.length > 1 ? ( filteredResults.map((repo) =>  { return (    
            <Grid item xs={4} md ={3} >
            <Card sx={{ maxWidth: 345, height: '16vw' }}>
                <CardContent>
                
                  <Typography gutterBottom variant="h5" component="div">
                     {repo.repositoryName}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {repo.description}
                  </Typography>
                </CardContent>
                <CardActions style = {{ marginTop:"auto"}}>
                <Button style ={{backgroundColor:"#464033"}} size="small" variant="contained" href = {repo.repoURL} target="_blank">  Learn More </Button>
                </CardActions>
              </Card>
            </Grid>
            ) } )
          ) :
             (  repositoryData && repositoryData.map((repo) =>  { return (    
              <Grid item xs={4} md ={3} >
              <Card sx={{ maxWidth: 345, height: '17vw' }}>
                  <CardContent>
                    <Typography gutterBottom variant="h5" component="div">
                      {repo.repositoryName}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {repo.description}
                    </Typography>
                  </CardContent>
                  <CardActions style = {{ marginTop:"auto"}}>
                  <Button style ={{backgroundColor:"#464033"}} size="small" variant="contained" href = {repo.repoURL} target="_blank">  Learn More </Button>
                  </CardActions>
                </Card>
              </Grid>
              ) } ) )
           }  */}

            
        </Grid>
        </Box>
    </div>
  );
}

export default App;