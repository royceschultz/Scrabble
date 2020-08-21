import React, {useState} from 'react'

export default function Tile(props){
  const[relX, setRelX] = useState(0)
  const[relY, setRelY] = useState(0)
  const[lastX, setLastX] = useState(0)
  const[lastY, setLastY] = useState(0)


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
    if(offX >= 0 && offX < boardBox.width){
      if(offY >= 0 && offY < boardBox.height){
        return true
      }
    }
    return false
  }

  const snapToGrid = (tile) => {
    const tileBox = tile.getBoundingClientRect()
    const board = document.getElementById('board')
    const boardBox = board.getBoundingClientRect()
    console.log(tileBox, boardBox)
    let offX = tileBox.left - boardBox.left
    let offY = tileBox.top - boardBox.top
    // offX = Math.floor(props.board_width * offX / boardBox.width)
    // offY = Math.floor(props.board_width * offY / boardBox.height)
    let tileWidth = boardBox.width / props.board_width
    let tileHeight = boardBox.height / props.board_width
    let coordX = Math.floor((offX + tileBox.width / 2) / tileWidth )
    let coordY = Math.floor((offY + tileBox.height / 2) / tileHeight)
    console.log(coordX, coordY)
    if(props.is_space_empty){
      if(props.is_space_empty(coordX + ',' + coordY) == false){
        console.log('space isnt empty')
        console.log(coordX + ',' + coordY)
        setRelX(lastX)
        setRelY(lastY)
        return
      }
    }

    // Report location back to parent so rack component can construct the move
    if(props.report_location){
      props.report_location(coordX+','+coordY)
    }

    let spaceX = coordX * tileWidth
    let spaceY = coordY * tileHeight
    // Convert absolute coordinates to relative

    setRelX((relX) => {
      const board = document.getElementById('board')
      const boardBox = board.getBoundingClientRect()
      const tileBox = tile.getBoundingClientRect()
      let offX = tileBox.left - boardBox.left
      let rel_position = relX + (spaceX - offX)
      // let rel_position = spaceX
      setLastX(rel_position)
      console.log(rel_position, relX, spaceX, offX, (spaceX - offX))
      return rel_position
    })
    // setRelY((relY) => {
    //   let rel_position = relY + (spaceY - offY)
    //   setLastY(rel_position)
    //   console.log(rel_position, relY, spaceY, offY)
    //   return rel_position
    // })
    setRelY((relY) => {
      const board = document.getElementById('board')
      const boardBox = board.getBoundingClientRect()
      const tileBox = tile.getBoundingClientRect()
      let offY = tileBox.top - boardBox.top
      let rel_position = relY + (spaceY - offY)

      // let rel_position = spaceY
      setLastY(rel_position)
      console.log(rel_position, relY, spaceY, offY, (spaceY - offY))
      return rel_position
    })
  }

  const startDrag = (event) => {
    if(props.dragable){
      props.report_location(null)
      const tile = event.target
      const tileBox = tile.getBoundingClientRect()
      let offX = event.pageX - tileBox.left
      let offY = event.pageY - tileBox.top
      let followFunc = followMouse(tileBox.left, tileBox.top, offX, offY)
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
      window.addEventListener('mousemove',followFunc)
    }
  }

  return <div style={{
    position: 'relative',
    left: relX,
    top: relY,
  }} onMouseDown={startDrag} className={'tile' + (props.dragable?' tile-hover':'')}>
    {props.letter}
  </div>
}
