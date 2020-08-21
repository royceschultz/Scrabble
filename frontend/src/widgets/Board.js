import React from 'react'
import './Board.css'
import Tile from './Tile'

const searchInOrder = (key, objects, def) => {
  console.log(objects);
  for(let i in objects){
    console.log(i);
    if(key in objects[i]){
      return objects[i][key]
    }
  }
  if(def == undefined){
    return null
  }
  return def
}

export default function Board(props){
  const range = [...Array(props.board_size).keys()]



  return <div id='board'>
    {range.map((i) => <div className='board_row'>
      {range.map((j) => {
        let position = i + ',' + j
        const bonus = (position in props.bonus_tiles
                        ? props.bonus_tiles[position]
                        : '')
        return <div className={'board_space ' + (bonus?'bonus-'+bonus:'')}>
          {(position in props.played_tiles)
              ? <Tile letter={props.played_tiles[position]} draggable={false} />
              : bonus
          }
        </div>
      })}
    </div>)}
  </div>
}
