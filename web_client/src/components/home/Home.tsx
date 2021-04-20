import React from 'react';
import { Link } from 'react-router-dom';
import Button from '@material-ui/core/Button';
import { makeStyles } from '@material-ui/core/styles';
import FormLabel from '@material-ui/core/FormLabel';
import FormControl from '@material-ui/core/FormControl';
import FormGroup from '@material-ui/core/FormGroup';
import Fade from '@material-ui/core/Fade';
import CircularProgress from '@material-ui/core/CircularProgress';
import Typography from '@material-ui/core/Typography'
import { TextField } from '@material-ui/core';

class Item {
  name: string;
  availableAmount: number;
  chosenAmount: number;

  constructor(itemName: string, amount: number) {
    this.name = itemName;
    this.availableAmount = amount;
    this.chosenAmount = 0;
  }

  chooseAmount(amount: number) {
    this.chosenAmount = amount;
  }

}

var formItems: Array<Item> = []

var W3CWebSocket = require('websocket').w3cwebsocket;
  var client = new W3CWebSocket('ws://192.168.43.36:8200/');

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
        console.log("Server Acknowledgement")
      }
      else if(jsonData.type === 3)
      {
        console.log("Order completed")
        alert("Order Completed! It's waiting for you to pick it up at: (" + jsonData.location.row + ", " + jsonData.location.col + ")")
        client.send(JSON.stringify(
          {src: 'C', 
          type: 2}
        ));
      }
      else if(jsonData.type === 4)
      {
        var message = "Items that are not available (rest of items are on their way):\n";
        jsonData.items.forEach((item: any) => {
          message += item.id + "\n";
        })
        alert(message);
        client.send(JSON.stringify(
          {src: 'C', 
          type: 2}
        ));
      }
      else if(jsonData.type === 5)
      {
        console.log("Available items:")
        jsonData.items.forEach((item: any) => {
            console.log("Type: " + item.id + ", Amount: " + item.amount);
            formItems.forEach(currItem => {
                if(currItem.name === item.id)
                {
                  formItems.splice(formItems.indexOf(currItem), 1);
                }
            })
            formItems.push(new Item(item.id, item.amount));
        });
        formItems.forEach((item)=> {console.log(item);})
        client.send(JSON.stringify(
          {src: 'C', 
          type: 2}
        ));
      }
  };

let useStyles = makeStyles((theme) => ({
    root: {
      '& .MuiTextField-root': {
        margin: theme.spacing(1),
        width: '30ch',
      },
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
    margin: theme.spacing(1),
    alignItems: 'center',
    flexDirection: 'column',
    width: 200,
  },
  placeholder: {
    height: 10,
  },
}));

export default function Home(){
  const classes = useStyles();
  const [state, setState] = React.useState({
  });
  const displayItems = formItems;
  
  const {} = state;

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

  const handleTextFieldChange = (e: any) => {
    formItems.forEach(currItem => {
      if(currItem.name === e.target.id)
      {
        currItem.chooseAmount(e.target.value);
      }
    })
  }

  const refreshInventory = () =>{
    console.log("Sending inventory request");
    client.send(JSON.stringify(
      {src: 'C', 
      type: 3}
    ));
  }

  const handleClickQuery = () => {
    clearTimeout(timerRef.current);
    console.log("Sending order");
    var orderedItems: any = []
    formItems.forEach(currItem => {
      if(currItem.chosenAmount > 0)
      {
        orderedItems.push(
          {
            id: currItem.name,
            amount: Number(currItem.chosenAmount)
          }
        )
      }
    })
    console.log(JSON.stringify(
      {src: 'C', 
      type: 1,
      items: orderedItems}
    ));
    client.send(JSON.stringify(
      {src: 'C', 
      type: 1,
      items: orderedItems}
    ));
  };

    return (
        <div className='wrapper'>
          <div><img src="./logo.png" height="100" width="200"></img></div>
        <div className='form-wrapper'>
        <div className={classes.root} style={{display: 'flex', justifyContent: 'center'}}>
      <FormControl component="fieldset" className={classes.root}>
        <FormLabel component="legend">Select Amounts Of Items</FormLabel>
        <FormGroup id="form">
          {
            displayItems.map( (item) => (
                <TextField id={item.name} label={item.name + ": " + item.availableAmount + " available"} type="search" variant="outlined" onChange={handleTextFieldChange} />
            ))
          }
          <div className='submit'>
          <div className={classes.root}>
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
