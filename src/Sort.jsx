import React from 'react'
import './style.css'
import { Link } from 'react-router-dom';

const Sort = (props) => {



  return (
    <>
    <div className='outer-div'>
        <h1>CLOWIZ</h1>
        <h2>Sort your Questions, Simple and Fast</h2>

        <h5>CLOS with description</h5>
        <textarea cols="30" rows="3" placeholder='CLOS Name - Description'/>

        <h5>Questions!</h5>
        <textarea cols="30" rows="3" placeholder='Question'/>


        <br/>

        <Link to="/Result"><button className='btn' onClick={props.handleClick}>SORT</button></Link>
        
        

        

      

        </div>
    </>
  )
}

export default Sort