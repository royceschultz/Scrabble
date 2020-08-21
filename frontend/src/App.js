import React from 'react'
import './App.css'

import Dashboard from './components/Dashboard'
import Home from './widgets/Home'

import { withAuthenticator, AmplifyAuthenticator, AmplifySignOut } from '@aws-amplify/ui-react'
import Amplify, { Auth } from 'aws-amplify'
import { awsconfig } from './aws-config'
Amplify.configure(awsconfig)

function App() {
  return (
    <div className="App">
      <AmplifyAuthenticator>
        <div>
          My App
          <AmplifySignOut />
        </div>
      </AmplifyAuthenticator>
      <Home/>
    </div>
  );
}

export default App;
