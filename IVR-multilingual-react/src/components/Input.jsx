import React, { useState } from "react";
import Vocal from '@untemps/react-vocal'
import Dropdown from 'react-dropdown';

export default function Input({ onSend }) {
  const [text, setText] = useState("");
  const [lang, setLanguage] = useState("en-US");

  const handleInputChange = e => {
    setText(e.target.value);
  };

  const handleSend = e => {
    e.preventDefault();
    onSend(text, lang);
    setText("");
  };


  const [result, setResult] = useState('')

    const _onVocalStart = () => {
        setResult('')
    }

    const _onVocalResult = (result) => {
        setResult(result)
        setText(result)
    }

    function refreshPage() {
      window.location.reload(false);
    }

    const options = [
      'en-US', 'hi-IN'
    ];
    const defaultOption = options[0];

  return (
    <div>
    <div className="input">
      <form onSubmit={handleSend}>
        <input
          type="text"
          onChange={handleInputChange}
          value={text}
          placeholder="Enter your message here"
        />
      
        <button onClick={handleSend}>
          <svg
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            viewBox="0 0 500 500"
          >
            <g>
              <g>
                <polygon points="0,497.25 535.5,267.75 0,38.25 0,216.75 382.5,267.75 0,318.75" />
              </g>
            </g>
          </svg>
        </button>
      </form>
    </div>

    <Vocal
            onStart={_onVocalStart}
            onResult={_onVocalResult}
            // style={{width: 45, position: 'absolute', right: 50, top: 15}}
            lang={lang}
        />
    <div class="relative inline-flex">
            <svg
              class="w-2 h-1 absolute top-0 right-0 m-4 pointer-events-none"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 412 232"
            >
              <path
                d="M206 171.144L42.678 7.822c-9.763-9.763-25.592-9.763-35.355 0-9.763 9.764-9.763 25.592 0 35.355l181 181c4.88 4.882 11.279 7.323 17.677 7.323s12.796-2.441 17.678-7.322l181-181c9.763-9.764 9.763-25.592 0-35.355-9.763-9.763-25.592-9.763-35.355 0L206 171.144z"
                fill="#648299"
                fill-rule="nonzero"
              />
            </svg>
            <select
              onChange={(e) => {
                setLanguage(e.target.value);
              }}
              onClick
              class="border border-gray-300 rounded-full text-gray-600 h-8 pl-5 pr-10 bg-white hover:border-gray-400 focus:outline-none appearance-none"
            >
              <option>Choose Language </option>
              <option>en-US</option>
              <option>hi-IN</option>
            </select>
          </div>

    </div>
  );
}