import React, {useState, useEffect} from 'react'
import Game from './Game'

const api_url = 'https://5o2i6gf458.execute-api.us-west-2.amazonaws.com/prod/'

function game_summary(game){
  return <div>
    <p>
      {game.id}
    </p>
    Scores:
    <p>
      {game.players.map((player) => <div>
        {player.name}: {player.score}
      </div>)}
    </p>

    Current Turn: {game.current_player_name}
  </div>
}

export default function Dashboard(props){
  const [games, setGames] = useState([])
  useEffect(() => {
    props.get(api_url+'game').then(data => {
      setGames(data.games)
    })
  }, [])

  const [gameState, setGameState] = useState(null)
  const fetchGameState = (gameId) => {
    props.get(api_url+'game', {game_id: gameId}).then(data => {
      console.log(data);
      setGameState(data.game_state)
    })
  }
  return <div>
    Dashboard
    {games.map(game => <div>
      <button onClick={() => fetchGameState(game.id)}>
        {game_summary(game)}
      </button>
    </div>)}
    {gameState ? <div>
      <Game game={gameState} {...props}/>
    </div> : null}
  </div>
}
