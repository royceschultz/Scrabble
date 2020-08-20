import React from 'react'
import './Board.css'

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
        return <div className='board_space'>
          {searchInOrder(position, [props.played_tiles, props.bonus_tiles], ' ')}
        </div>
      })}
    </div>)}
  </div>
}
