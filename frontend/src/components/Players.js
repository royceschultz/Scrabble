import React from 'react'

export default function Players(game){
  return <div>
    {game.players.map(player => <div>
      <p>
        {player.name}
      </p>
      <p>
        {player.score}
      </p>
    </div>)}
  </div>
}
