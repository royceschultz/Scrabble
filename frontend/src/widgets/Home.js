import React, {useState, useEffect} from 'react'
import {GET, API} from './SentryFetch'
import { Auth } from 'aws-amplify'
import GameBoard from './GameBoard'

export default function Home(){
  // State variables
  const [games, setGames] = useState([])
  const [selectedGame, setSelectedGame] = useState(null)
  useEffect(() => {
    GET(API+'game').then(data => {
      console.log(data)
      setGames(data.games)
    })
  }, [])
  return <div>
    Home
    <div>
      {games.map(game => <span>
        <button onClick={() => setSelectedGame(game)}>
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
        ? <GameBoard gameId={selectedGame.id} />
        : null
      }
    </div>
  </div>
}
