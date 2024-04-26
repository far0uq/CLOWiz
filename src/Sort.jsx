import "./style.css";
import { Link } from "react-router-dom";

const Sort = (props) => {
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
          placeholder="CLOS Name - Description"
        />

        <h5 className="form-text">Questions:</h5>
        <textarea
          className="textarea-style"
          cols="30"
          rows="3"
          placeholder="Question"
        />

        <br />

        <Link to="/Result">
          <button className="btn" onClick={props.handleClick}>
            SORT
          </button>
        </Link>
      </div>
    </>
  );
};

export default Sort;
