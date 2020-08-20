import React, {useState} from 'react'
import SubmitMove from './SubmitMove'

function Tile(props){
  const[relX, setRelX] = useState(0)
  const[relY, setRelY] = useState(0)


  const dragging = (startX, startY, boundingBox) => (event) => {
    let diffX = event.clientX - boundingBox.left
    let diffY = event.clientY - boundingBox.top
    setRelX(relX + (diffX - startX))
    setRelY(relY + (diffY - startY))
  }

  const startDrag = (event) => {
    const target = event.target
    let boundingBox = event.target.getBoundingClientRect()

    let diffX = event.clientX - boundingBox.left
    let diffY = event.clientY - boundingBox.top
    const drag_event = dragging(diffX, diffY, boundingBox)
    window.addEventListener('mousemove',drag_event)

    const onMouseUp = (event) => {
      const board = document.getElementById('board')
      const boardBoundingBox = board.getBoundingClientRect()
      const bb = target.getBoundingClientRect()
      let tileX = bb.left + bb.width / 2
      let tileY = bb.top + bb.height / 2
      let boardX = tileX - boardBoundingBox.left
      let boardY = tileY - boardBoundingBox.top
      // let boardX = event.clientX - boardBoundingBox.left
      // let boardY = event.clientY - boardBoundingBox.top

      if(boardX > 0 && boardX < boardBoundingBox.width && boardY > 0 && boardY < boardBoundingBox.height){
        const num_rows = board.getElementsByClassName('row').length
        let spaceX = Math.floor(num_rows * boardX / boardBoundingBox.width)
        let spaceY = Math.floor(num_rows * boardY / boardBoundingBox.height)
        console.log(spaceX, spaceY);
        props.move([spaceX, spaceY])
        spaceX = boardBoundingBox.left + ( spaceX * boardBoundingBox.width / num_rows )
        spaceY = boardBoundingBox.top + ( spaceY * boardBoundingBox.height / num_rows )
        let offX = boundingBox.left - spaceX
        let offY = boundingBox.top - spaceY
        setRelX(relX - offX + 2)
        setRelY(relY - offY + 2)
      }else{
        setRelX(0)
        setRelY(0)
        props.move(null)
      }
      window.removeEventListener('mousemove', drag_event)
      // Remove self too.
      window.removeEventListener('mouseup', onMouseUp)
    }
    window.addEventListener('mouseup', onMouseUp)
  }
  return <div
    style={{
      position: 'relative',
      left: relX,
      top: relY,
    }}
    className='player-tile'
    onMouseDown={startDrag}>
    {props.letter}
  </div>
}

export default function Rack(game, post){
  let letters = ''
  for(let letter in game.user.rack){
    letters += letter.repeat(game.user.rack[letter])
  }
  const [move, setMove] = useState([])
  const moveTile = (i) => (location) => {
    let move_copy = [...move]
    move_copy[i] = location
    setMove(move_copy)
  }
  const get_move_obj = () => {
    let move_obj = {}
    move.map((m,i) => {
      if(m){
        move_obj[m[0]+','+m[1]] = letters[i]
      }
    })
    return move_obj
  }
  return <div>
    {move}
    <div>
      {letters.split('').map((letter, i) => Tile({move: moveTile(i), letter: letter}))}
    </div>
    <SubmitMove game_id={game.id} move={get_move_obj} post={post}/>
  </div>
}
