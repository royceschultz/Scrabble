import React from 'react'
import './App.css'

import Dashboard from './components/Dashboard'
import Home from './widgets/Home'

import { withAuthenticator, AmplifyAuthenticator, AmplifySignOut } from '@aws-amplify/ui-react'
import Amplify, { Auth } from 'aws-amplify'
import { awsconfig } from './aws-config'
Amplify.configure(awsconfig)

let callAPI = async (url, params) => {
    params = (typeof params !== 'undefined') ?  params : {}
    const user = await Auth.currentAuthenticatedUser();
    if(user == undefined){
      console.log('No user logged in');
      return
    }
    const token = user.signInUserSession.idToken.jwtToken;
    // convert object to list -- to enable .map
    let data = Object.entries(params);
    // encode every parameter (unpack list into 2 variables)
    data = data.map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`);
    // combine into string
    let query = '?' + data.join('&');
    console.log(query); // => width=1680&height=1050

    let res = await fetch(url+query, {
      method: 'GET',
      headers: {
        Authorization: token
      },
    })
    let json_data = await res.json()
    return json_data
}

let postAPI = async (url, data) => {
    const user = await Auth.currentAuthenticatedUser();
    if(user == undefined){
      console.log('No user logged in');
      return
    }
    const token = user.signInUserSession.idToken.jwtToken;

    console.log(url)
    console.log(token)

    let res = await fetch(url, {
      method: 'POST',
      headers: {
        Authorization: token,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    })
    let json_data = await res.json()
    return json_data
}

const api_url = 'https://5o2i6gf458.execute-api.us-west-2.amazonaws.com/prod/'

function App() {
  return (
    <div className="App">
      <AmplifyAuthenticator>
        <div>
          My App
          <AmplifySignOut />
        </div>
      </AmplifyAuthenticator>
      <div>
        {['new_game','game'].map((path) => {
          return (
            <button onClick={() => callAPI(api_url+path).then(data => {console.log(data)})}>
              GET: {path}
            </button>
          )
        })}
        <button onClick={() => postAPI(api_url+'test', {'message': 'test'}).then(data => {console.log(data)})}>
          Test Post
        </button>
      </div>
      <div>
        {/* <Dashboard get={callAPI} post={postAPI}/> */}
        <Home/>
      </div>
    </div>
  );
}

export default App;
