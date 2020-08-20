import React, {useState} from 'react'

export default function Tile(props){
  const[relX, setRelX] = useState(0)
  const[relY, setRelY] = useState(0)


  const getSpacePosition = (x,y) => {
    const board = document.getElementById('board')
    const boundingBox = board.getBoundingClientRect()
    console.log(boundingBox);
    return [0,0]
  }

  const followMouse = (tileX, tileY, offX, offY) => (event) => {
    setRelX(event.clientX - offX - tileX + relX)
    setRelY(event.clientY - offY - tileY + relY + window.scrollY)
  }

  const onBoard = (tile) => {
    const board = document.getElementById('board')
    const boardBox = board.getBoundingClientRect()
    const tileBox = tile.getBoundingClientRect()
    let offX = tileBox.left - boardBox.left + tileBox.width / 2
    let offY = tileBox.top - boardBox.top + tileBox.height / 2
    if(offX >= 0 && offX < boardBox.width - tileBox.width){
      if(offY >= 0 && offY < boardBox.height - tileBox.height){
        return true
      }
    }
    return false
  }

  const snapToGrid = (tile) => {
    const tileBox = tile.getBoundingClientRect()
    const board = document.getElementById('board')
    const boardBox = board.getBoundingClientRect()
    let offX = tileBox.left - boardBox.left
    let offY = tileBox.top - boardBox.top
    // offX = Math.floor(props.board_width * offX / boardBox.width)
    // offY = Math.floor(props.board_width * offY / boardBox.height)
    let tileWidth = boardBox.width / props.board_width
    let coordX = Math.floor((offX + tileBox.width / 2) / tileWidth )
    let coordY = Math.floor((offY + tileBox.height / 2) / tileWidth)

    let spaceX = coordX * tileWidth
    let spaceY = coordY * tileWidth
    setRelX((relX) => relX + (spaceX - offX))
    setRelY((relY) => relY + (spaceY - offY))
    console.log(coordX, spaceX, offX);
    console.log(coordY, spaceY, offY);
  }

  const startDrag = (event) => {
    if(props.dragable){
      const tile = event.target
      const tileBox = tile.getBoundingClientRect()
      let offX = event.pageX - tileBox.left
      let offY = event.pageY - tileBox.top
      let followFunc = followMouse(tileBox.left, tileBox.top, offX, offY)
      window.addEventListener('mousemove',followFunc)
      const cleanUp = (event) => {
        window.removeEventListener('mousemove',followFunc)
        window.removeEventListener('mouseup',cleanUp)
        if(onBoard(tile)){
          console.log('on board')
          snapToGrid(tile)
        }else{
          setRelX(0)
          setRelY(0)
        }
      }
      window.addEventListener('mouseup',cleanUp)
    }
  }

  return <div style={{
    position: 'relative',
    left: relX,
    top: relY,
  }} onMouseDown={startDrag} className='tile'>
    {props.letter}
  </div>
}
