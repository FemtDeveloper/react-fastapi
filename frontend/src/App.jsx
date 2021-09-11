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
      .get("http://127.0.0.1:8000/api/leads")
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
