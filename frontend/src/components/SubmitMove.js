import React from 'react'

const api_url = 'https://5o2i6gf458.execute-api.us-west-2.amazonaws.com/prod/'

export default function SubmitMove(props){
  const postMove = () => {
    props.post(api_url+'game', {move: props.move(), game_id: props.game_id}).then(data => console.log(data))
  }
  return <button onClick={postMove}>
    Submit Move
  </button>
}
