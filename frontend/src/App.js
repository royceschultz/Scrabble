import React from 'react';
import logo from './logo.svg';
import './App.css';

import { withAuthenticator, AmplifyAuthenticator, AmplifySignOut } from '@aws-amplify/ui-react';
import Amplify, { Auth, API } from 'aws-amplify';
import { awsconfig } from './aws-config';
// Amplify.configure(awsconfig);
Amplify.configure({
    Auth: {
      userPoolId: 'us-west-2_uy6X77g8K',
      userPoolWebClientId: '3i7g2qdqtcqjcvf57lr5m24ks5',
      Region: 'us-west-2',
      // TODO: Consider adding cookie storage param
    },
    API: {
      endpoints: [
        {
          name:'pets',
          endpoints:'5e1yvhtlqk.execute-api.us-west-2.amazonaws.com'
        },
      ]
    }
});

let callAPI = async (url) => {
    console.log('here')
    const user = await Amplify.Auth.currentAuthenticatedUser();
    const token = user.signInUserSession.idToken.jwtToken;

    console.log(url)
    console.log(token)

    fetch(url, {
      method: 'GET',
      headers: {
        Authorization: token
      }
    }).then(data => data.json()).then(j => console.log(j))

}

callAPI('https://5e1yvhtlqk.execute-api.us-west-2.amazonaws.com/beta/pets')

function App() {
  return (
    <div className="App">
      <AmplifyAuthenticator>
        <div>
          My App
          <AmplifySignOut />
        </div>
      </AmplifyAuthenticator>
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
      </header>
    </div>
  );
}

export default App;
