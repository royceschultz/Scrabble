import React from 'react'
import Board from './Board'
import Players from './Players'
import Rack from './Rack'

export default function Game(props){
  return <div>
    Game
    {Players(props.game)}
    {Rack(props.game, props.post)}
    {Board(props.game)}
  </div>
}
