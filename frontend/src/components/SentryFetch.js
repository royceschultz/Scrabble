import { Auth } from 'aws-amplify'

export default async function SentryFetch(){
  const user = await Auth.currentAuthenticatedUser();
  if(user == undefined){
    console.log('No user logged in');
    return
  }else{
    console.log(user)
  }
}
