import React, { useState,useEffect } from "react";
import Navbar from "./components/Navbar";
import { Routes, Route, useNavigate } from "react-router-dom";
import "./App.css"
import TypewriterEffect from "components/TypeWriterEffect.jsx";
import axios from "axios";

const Home = () => {
  const navigate=useNavigate();

  // const handleOnClick=()=>{
  //   navigate("/about");
  // }

  return (
    <>
      <Navbar />
      <div className="description1">
      <div className="hero-section-1">
        {/* <div className="hero-section-1-1"> */}
          <h1>Welcome, Star Wars Enthusiast! Ask Anything About Your Favorite Characters!</h1>
        {/* </div> */}
        <div className="hero-section-1-1">
        <p>Unleash your inner Jedi and dive into the expansive Star Wars universe. Whether you’re a seasoned fan or a curious newcomer, ask anything about your favorite characters and get instant answers!. Discover the backstories, powers, and unique traits that make each character an integral part of the Star Wars saga. </p>
        
        </div>
        <button class="awesome-button" onClick={()=>{navigate("/ask")}}>Ask me</button>
      </div>
      <div className="hero-section-2">
      {/* <img src="welcome2.png" alt="welcome-img" className="welcome-img"/> */}
        {/* <button class="custom-ask-button">Ask any question</button> 
        <h1>Search and get to know about your favorite character</h1> */}

      </div>
      </div>
    </>
  );
};

const Ask = () => {

  const [question,setQuestion]=useState("");
  const [answer,setAnswer]=useState("");

  const getResponse=async (e)=>{
    e.preventDefault();
    setAnswer("");

    const response=await axios.post("http://127.0.0.1:8000/ask",{
      question:question
    });

    const data=await response.data;
    console.log(data.response.result);
    setAnswer(data.response.result);
  };

  return (
    <>
      <Navbar />
      <div className="description2">
      <div className="ask-container">
        
        <h2>Have questions? </h2>
        <h3>Just type your query below, and get instant answers about their history, abilities, and more</h3>
        
        <div className="ask-container-1">
        <div className="ask-container-1-1">
          <input type="text" class="input-question" placeholder="Type your question here..." onChange={(e)=>{
            setQuestion(e.target.value);
            console.log(question);
          }}/>
          <button class="search-button" onClick={getResponse}>Ask</button>
        </div>

        {answer && <TypewriterEffect text={answer} />}
        </div>

      </div>
      </div>
    </>
  );
};

// const Service = () => {
//   return (
//     <>
//       <Navbar />
//       <section className="hero-section">
//         <p>Welcome to </p>
//         <h1>Thapa Technical Service Page</h1>
//       </section>
//     </>
//   );
// };

const Contact = () => {
  return (
    <>
      <Navbar />
      <div className="description3">
        <div className="ask-container">
          <h1>Contact Us</h1>
          <p>For any bug reports or other inquiries, please contact us via email</p>
          <p>kalambkar26@gmail.com</p>
        </div>
      </div>
    </>
  );
};

const App = () => {
  return (
    <Routes>
      <Route exact path="/" element={<Home />} />

      <Route path="/ask" element={<Ask />} />

      {/* <Route path="/service" element={<Service />} /> */}

      <Route path="/contact" element={<Contact />} />
    </Routes>
  );
};

export default App;
