import React from 'react';
import ReactDOM from 'react-dom';
import {Glyphicon} from 'react-bootstrap';
function Thumbnail(props) {
  return (
    <div className="thumbnail">
      <div className="caption">
        <h3><Glyphicon glyph={props.glyph} style={{margin:'0px 10px 0px 10px'}}/>{props.title}</h3>
        <p>{props.desc}</p>
        <p>
          {props.children}
        </p>
      </div>
    </div>
  );
}
export default Thumbnail;
