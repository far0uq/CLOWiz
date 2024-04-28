import React, { useState, useEffect } from "react";
import "./style.css";
import { Link } from "react-router-dom";

const Result = () => {
  const [result, setResult] = useState(null);

  useEffect(() => {
    // Retrieve the resultData from session storage
    const resultData = sessionStorage.getItem("resultData");

    // Check if resultData is available
    if (resultData) {
      // Parse the resultData JSON
      const data = JSON.parse(resultData);
      const resultArray = Object.entries(data.questions).map(
        ([question, clo]) => ({ question, clo })
      );
      console.log("🚀 ~ useEffect ~ resultArray:", resultArray);

      // Use the data as needed
      setResult(resultArray);
    } else {
      console.error("resultData not found in session storage");
    }
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
              <th>Questions</th>
            </tr>
          </thead>
          <tbody>
            {result &&
              result.map((item, index) => (
                <tr key={index}>
                  <td>{item.clo}</td>
                  <td>{item.question}</td>
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
