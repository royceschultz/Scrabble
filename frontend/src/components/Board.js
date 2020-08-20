import React from 'react'
import './Board.css'

const get = (obj, key, def) => key in obj ? obj[key] : def ? def : null

export default function Board(game){
  let size = game.board_size
  let range = [...Array(size).keys()]
  return <div className='board' id='board'>
    {range.map(row => <div className='row'>
      {range.map(col => {
        let coord = row + ',' + col
        let value = get(game.played_tiles, coord, get(game.bonus_tiles, coord, '.'))
        return <div className='cell'>
          {value}
        </div>
      })}
    </div>)}
  </div>
}
