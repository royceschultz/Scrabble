import React, {useState, useEffect} from 'react'
import {GET, API} from './SentryFetch'
import { Auth } from 'aws-amplify'
import GameBoard from './GameBoard'

export default function Home(){
  // State variables
  const [games, setGames] = useState([])
  const [selectedGame, setSelectedGame] = useState(null)
  const fetchGames = () => {
    GET(API+'games').then(data => {
      console.log(data)
      setGames(data.games)
    })
  }
  useEffect(fetchGames, [])

  const callNewGame = (event) => {
    GET(API+'new_game').then(data => {
      console.log(data)
      fetchGames()
    })
  }
  return <div>
    Home
    <button className='btn' onClick={callNewGame}>
      New Game
    </button>
    <div>
      {games.map(game => <span>
        <button className='btn' onClick={() => setSelectedGame(game)}>
          {game.players.map((player) => <div>
            {player.score} : {player.name}
          </div>)}
          {Auth.user.username == game.current_player_name
            ? 'Your Turn'
            : 'Waiting for opponent'}
        </button>
      </span>)}
    </div>
    <div>
      {selectedGame
        ? <GameBoard {...selectedGame} />
        : null
      }
    </div>
  </div>
}
