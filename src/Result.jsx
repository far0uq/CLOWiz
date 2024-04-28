import React, { useState, useEffect } from "react";
import "./style.css";
import { Link } from "react-router-dom";

const Result = () => {
  const [clos, setClos] = useState([]);

  useEffect(() => {
    // Fetch the result from the Flask backend when the component mounts
    const fetchResult = async () => {
      const response = await fetch('/Result');
      const data = await response.json();
      setClos(data.clos);
    };
    fetchResult();
  }, []);

  return (
    <>
      <div className="outer-div">
        <h1>Processed Successfully</h1>
        <br />
        <table>
          <thead>
            <tr>
              <th>CLO</th>
            </tr>
          </thead>
          <tbody>
            {clos.map((clo, index) => (
              <tr key={index}>
                <td>{clo}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <Link to="/Sort">
          <button className="btn">SORT AGAIN</button>
        </Link>
      </div>
    </>
  );
};

export default Result;
