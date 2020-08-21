import React, {useState, useEffect} from 'react'
import {GET, API} from './SentryFetch'
import Board from './Board'
import Tile from './Tile'
import Rack from './Rack'

export default function GameBoard(props){
  const [game, setGame] = useState(null)
  const fetchGameState = () => {
    if(props.id){
      GET(API+'games/game_id', {game_id: props.id}).then(data => {
        console.log(data)
        setGame(data.game_state)
      })
    }
  }
  useEffect(fetchGameState, [props])
  return <div className='game-board'>
    <button className='btn' onClick={fetchGameState}>
      Get game state for {props.id}
    </button>
    {game
      ? (<div>
        <Rack {...game}/>
        <Board {...game}/>
      </div>)
      : null
    }

  </div>
}
