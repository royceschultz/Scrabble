import { Auth } from 'aws-amplify'

export let API = 'https://5o2i6gf458.execute-api.us-west-2.amazonaws.com/prod/'

export default async function SentryFetch(){
  const user = await Auth.currentAuthenticatedUser();
  if(user == undefined){
    console.log('No user logged in');
    return
  }else{
    console.log(user)
  }
}

export let GET = async (url, params) => {
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

export let POST = async (url, data) => {
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
