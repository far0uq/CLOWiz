import "./style.css";
import { useState } from "react";

const Sort = () => {
  const [closDescription, setClosDescription] = useState("");
  const [question, setQuestion] = useState("");

  const handleClick = async () => {
    try {
      // Send a POST request to the Flask backend
      const response = await fetch("http://localhost:1800/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ closDescription, question }),
      });

      // Check if the response is successful
      if (!response.ok) {
        throw new Error(`Server responded with status ${response.status}`);
      }

      // Parse the response JSON
      const data = await response.json();
      console.log("Response from server:", data);
      // Store the data in session storage
      sessionStorage.setItem("resultData", JSON.stringify(data));

      // Redirect to the result page
      window.location.href = "/Result";
    } catch (error) {
      console.error("Error occurred:", error);
      // Handle error, show a message to the user, etc.
    }
  };

  return (
    <>
      <div className="outer-div">
        <h1>CLOWIZ</h1>
        <h2 className="form-text">Sort your Questions, Simple and Fast!</h2>

        <h5 className="form-text">CLOS with descriptions:</h5>
        <textarea
          className="textarea-style"
          cols="30"
          rows="3"
          value={closDescription}
          onChange={(e) => setClosDescription(e.target.value)}
          placeholder="CLOS Name - Description"
        />

        <h5 className="form-text">Questions:</h5>
        <textarea
          className="textarea-style"
          cols="30"
          rows="3"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Question"
        />

        <br />

        <button className="btn" onClick={handleClick}>
          SORT
        </button>
      </div>
    </>
  );
};

export default Sort;
