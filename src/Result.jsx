import React from "react";
import "./style.css";

import { Link } from "react-router-dom";

const Result = (props) => {
  return (
    <>
      <div className="outer-div">
        <h1>Processed Successfully</h1>
        <br />
        <table>
          <tr>
            <td>CLO-1</td>
          </tr>
          <tr>
            <td>CLO-2</td>
          </tr>
          <tr>
            <td>CLO-3</td>
          </tr>
        </table>
        <Link to="/Sort">
          <button className="btn">SORT AGAIN</button>
        </Link>
      </div>
    </>
  );
};

export default Result;
