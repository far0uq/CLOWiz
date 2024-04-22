import Sort from './Sort';
import React from 'react'
import Result from './Result';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
 
 const App = () => {



   return (
    <>



<Router>

          <Routes>
            <Route path="/" element={<Sort />} />
            <Route path="/Result" element={<Result />} />
            <Route path="/Sort" element={<Sort />} />
          </Routes>
          
        </Router>
      
      

    </>
   )
 }


 
 export default App