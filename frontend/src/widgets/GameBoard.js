import React, {useState, useEffect} from 'react'
import {GET, API} from './SentryFetch'
import Board from './Board'
import Tile from './Tile'

export default function GameBoard(props){
  const [game, setGame] = useState(null)
  const fetchGameState = () => {
    if(props.gameId){
      GET(API+'game', {game_id: props.gameId}).then(data => {
        console.log(data)
        setGame(data.game_state)
      })
    }
  }
  useEffect(fetchGameState, [props])
  return <div>
    GameBoard
    <Tile letter='R' dragable={true} board_width={15}/>
    <button onClick={fetchGameState}>
      Get game state for {props.gameId}
    </button>
    {game
      ? (<div>
        <Board {...game}/>
      </div>)
      : null
    }

  </div>
}
