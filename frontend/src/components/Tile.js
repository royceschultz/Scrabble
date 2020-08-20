import React, {useState} from 'react'

function Tile(props){
  const[relX, setRelX] = useState(0)
  const[relY, setRelY] = useState(0)

  const offset = (X, Y, boundingBox) => {
    offX = X - boundingBox.left
    offY = Y - boundingBox.top
    return [offX, offY]
  }

  const dragging = (startOffset, boundingBox) => event => {

  }

  const startDrag = (event) => {
    const target = event.target
    const tile_bounding_box = () => target.getBoundingClientRect()
    let bb = tile_bounding_box()
    const drag_event = dragging(offset(event.clientX, event.clientY, bb), bb)
    window.addEventListener('mousemove',drag_event)
  }

}
