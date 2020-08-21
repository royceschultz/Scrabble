import React, {useState} from 'react'
import Tile from './Tile'

import { POST, API } from './SentryFetch'

export default function Rack(props){
  const [locations, setLocations] = useState([])
  let letters = ''
  for (let letter in props.user.rack){
    letters += letter.repeat(props.user.rack[letter])
  }

  const reportLocation = (idx) => (location) => {
    let new_locs = [...locations]
    new_locs[idx] = location
    setLocations(new_locs)
  }

  const isSpaceEmpty = (location) => {
    if(locations.includes(location)){
      return false
    }
    if(location in props.played_tiles){
      return false
    }
    return true
  }

  const handleSubmit = (event) => {
    let move = {}
    for(let i in letters){
      const loc = locations[i]
      if(loc){
        const letter = letters[i]
        move[loc] = letter
      }
    }
    console.log(move)
    POST(API + 'play', {move: move, game_id: props.id}).then(data => console.log(data))
  }
  return <div>
    <div className='rack-letters'>
      {[...letters].map((letter, i) => <Tile dragable={true}
              letter={letter}
              board_width={15}
              report_location={reportLocation(i)}
              is_space_empty={isSpaceEmpty}
            />)}
    </div>
    <button className='btn' onClick={handleSubmit}>
      Submit move
    </button>
  </div>
}
