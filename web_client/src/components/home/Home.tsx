import React from 'react';
import { Link } from 'react-router-dom';
import Button from '@material-ui/core/Button';
import { makeStyles } from '@material-ui/core/styles';
import FormLabel from '@material-ui/core/FormLabel';
import FormControl from '@material-ui/core/FormControl';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Fade from '@material-ui/core/Fade';
import CircularProgress from '@material-ui/core/CircularProgress';
import Typography from '@material-ui/core/Typography'

var formItems: any[] = []
var formAmounts = []

var W3CWebSocket = require('websocket').w3cwebsocket;
  var client = new W3CWebSocket('ws://localhost:8200/');

  console.log("Starting Client");

  client.onerror = function() {
      console.log('Connection Error');
  };

  client.onopen = function() {
      if (client.readyState === client.OPEN)
      {
        console.log('Client Connecting');
        client.send(JSON.stringify(
          {src: 'C', 
          type: 0}
        ));
        console.log("Sending inventory request");
        client.send(JSON.stringify(
          {src: 'C', 
          type: 3}
        ));
      }
  };

  client.onclose = function() {
      console.log('Client Closed');
  };

  client.onmessage = function(e: any) {
      const jsonData = JSON.parse(e.data);
      if(jsonData.type === 0)
      {
        console.log("Client Connected")
      }
      else if(jsonData.type === 5)
      {
        console.log("Available items:")
        jsonData.items.forEach((item: any) => {
            console.log("Type: " + item.id + ", Amount: " + item.amount);
            if(!formItems.includes(item.id))
              formItems.push(item.id);
            formAmounts.push(item.amount);
        });
        formItems.forEach((item)=> {console.log(item);})
      }
  };

let useStyles = makeStyles((theme) => ({
    root: {
      display: 'flex',
    },
    formControl: {
      margin: theme.spacing(3),
    },
}));

const useStyles2 = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  button: {
    margin: theme.spacing(2),
    alignItems: 'center',
    flexDirection: 'column',
    width: 200,
  },
  placeholder: {
    height: 40,
  },
}));

export default function Home(){
  const classes = useStyles();
  const [state, setState] = React.useState({
      iPhone12: false,
      SmartWatch: false,
      Airpods: false,
  });
  const displayItems = formItems;

  const handleChange = (event: any) => {
      setState({ ...state, [event.target.name]: event.target.checked });
  };
  
  const { iPhone12, SmartWatch, Airpods } = state;
  const error = [iPhone12, SmartWatch, Airpods].filter((v) => v).length !== 2;

  const classes2 = useStyles2();
  const [loading, setLoading] = React.useState(false);
  const [query, setQuery] = React.useState('idle');
  const timerRef = React.useRef<number>();

  React.useEffect(
    () => () => {
      clearTimeout(timerRef.current);
    },
    [],
  );

  const handleClickLoading = () => {
    setLoading((prevLoading) => !prevLoading);
  };

  const refreshInventory = () =>{
    console.log("Sending inventory request");
    client.send(JSON.stringify(
      {src: 'C', 
      type: 3}
    ));
  }

  const handleClickQuery = () => {
    clearTimeout(timerRef.current);
    console.log("Sending inventory request");
    client.send(JSON.stringify(
      {src: 'C', 
      type: 3}
    ));

    if (query !== 'idle') {
      setQuery('idle');
      return;
    }

    setQuery('progress');
    timerRef.current = window.setTimeout(() => {
      setQuery('success');
    }, 5000);
  };

    return (
        <div className='wrapper'>
        <div className='form-wrapper'>
        <div className={classes.root} style={{display: 'flex', justifyContent: 'center'}}>
      <FormControl component="fieldset" className={classes.formControl}>
        <FormLabel component="legend">Select Items To Place</FormLabel>
        <FormGroup id="form">
          <FormControlLabel
            control={<Checkbox checked={iPhone12} onChange={handleChange} name="iPhone12" />}
            label="iPhone 12"
          />
          <FormControlLabel
            control={<Checkbox checked={SmartWatch} onChange={handleChange} name="SmartWatch" />}
            label="Smart Watch"
          />
          <FormControlLabel
            control={<Checkbox checked={Airpods} onChange={handleChange} name="Airpods" />}
            label="Airpods"
          />
          {
            displayItems.map( (item) => {
                    <FormControlLabel
                  control={<Checkbox checked={Airpods} onChange={handleChange} name="Airpods" />}
                  label="Airpods"
                />
            })
          }
          <div className='submit'>
          <div className={classes2.root}>
      <div className={classes2.placeholder}>
        <Fade
          in={loading}
          style={{
            transitionDelay: loading ? '800ms' : '0ms',
          }}
          unmountOnExit
        >
          <CircularProgress />
        </Fade>
      </div>
      <div className={classes2.placeholder}>
        {query === 'success' ? (
          <Typography>Success!</Typography>
        ) : (
          <Fade
            in={query === 'progress'}
            style={{
              transitionDelay: query === 'progress' ? '800ms' : '0ms',
            }}
            unmountOnExit
          >
            <CircularProgress />
          </Fade>
        )}
      </div>
      <div className='submit'>
      <Button onClick={handleClickQuery} className={classes2.button} fullWidth={true} variant="contained" color='primary'>
        {query !== 'idle' ? 'Reset' : 'Pick!'}
      </Button>
      <Button onClick={refreshInventory} className={classes2.button} fullWidth={true} variant="outlined" color='primary'>
        Refresh inventory list
      </Button>
      <Button component={Link} to="/Login" variant="outlined" color='primary'>Click here to sign out</Button>
      </div>
    </div>
          </div>
        </FormGroup>
      </FormControl>
    </div>
    </div>
    </div>
    ); 
}