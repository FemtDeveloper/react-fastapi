import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [message, setMessage] = useState("");
  const getWelcomeMessage = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };
    const response = await axios
      .get("http://ec2-3-141-19-179.us-east-2.compute.amazonaws.com:8000/api")
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
    <div className="App">
      <h1>titulo de los leads</h1>
      <h2>{message}</h2>
    </div>
  );
}

export default App;
