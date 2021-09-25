import React, { useContext, useEffect, useState } from "react";
import axios from "axios";
import Register from "./components/Register";
import Header from "./components/Header";
import { UserContext } from "./context/UserContext";
import Login from "./components/Login";
import Table from "./components/Table";

function App() {
  const [message, setMessage] = useState("");
  const [token] = useContext(UserContext);

  const getWelcomeMessage = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };
    const response = await axios
      .get("http://127.0.0.1:8000/api")
      // .get("http://ec2-3-141-19-179.us-east-2.compute.amazonaws.com:8000/api")
      .then((response) => {
        const data = response.data;
        console.log(data);
        setMessage(data.message);
      });
  };

  useEffect(() => {
    getWelcomeMessage();
  }, []);

  return (
    <>
      <Header title={message} />
      <div className="columns">
        <div className="column"></div>
        <div className="column m-5 is-two-thirds">
          {!token ? (
            <div className="columns">
              <Register />
              <Login />
            </div>
          ) : (
            <Table />
          )}
        </div>
        <div className="column">{/* <Login/> */}</div>
      </div>
    </>
  );
}

export default App;
