import React, { useState, useEffect } from "react";
import ReactDOM from "react-dom";

import BotMessage from "./components/BotMessage";
import UserMessage from "./components/UserMessage";
import Messages from "./components/Messages";
import Input from "./components/Input";

import API from "./ChatbotAPI";
import axios from "axios"

import "./styles.css";
import Header from "./components/Header";

function Chatbot() {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    async function loadWelcomeMessage() {
      setMessages([
        <BotMessage
          key="0"
          fetchMessage={() => "Hi, Welcome to ABInBev Bot"}
        />
      ]);
    }
    loadWelcomeMessage();
  }, []);

  const send = async (text, lang) => {
    // setMessages(messages.concat(<UserMessage key={messages.length + 1} text={text} />))
    // var r = []
    // axios({
    //   method: 'post',
    //   url: 'http://127.0.0.1:8000/abinbev',
    //   data: {
    //       "msg": text,
    //       "lang": "en"
    //   }
    // }).then((res)=> {
    //   console.log(res.data);
    //     r.push(res.data[i])
    //     if (res.data.length > 1)
    //       setMessages(messages.concat(
    //         <BotMessage
    //           key={messages.length + 2}
    //           fetchMessage={async () => res.data[0]}
    //         />
    //       ))
          
    //       if (res.data.length > 2)
    //         resolve(res.data[2])

    //       if (res.data.length > 3)
    //         resolve(res.data[3])
            
       
    // }, (e) => {
    //   console.log(e);
    // });


    const newMessages = messages.concat(
      <UserMessage key={messages.length + 1} text={text} />,
      <BotMessage
        key={messages.length + 2}
        fetchMessage={async () => await API.GetChatbotResponse(text, lang)}
      />
    );
    setMessages(newMessages);
  };

  return (
    <div className="chatbot">
      <Header />
      <Messages messages={messages} />
      <Input onSend={send} />
    </div>
  );
}

const rootElement = document.getElementById("root");
ReactDOM.render(<Chatbot />, rootElement);
