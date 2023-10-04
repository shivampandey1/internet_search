import { useState, useEffect } from "react";
import axios from 'axios';
import TypingAnimation from "../components/TypingAnimation";

export default function Home() {
  const [inputValue, setInputValue] = useState('');
  const [chatLog, setChatLog] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isSearchEnabled, setIsSearchEnabled] = useState(false); // New state for search toggle

  const handleSubmit = (event) => {
    event.preventDefault();
    setChatLog((prevChatLog) => [...prevChatLog, { type: 'user', message: inputValue }]);
    sendMessage(inputValue);
    setInputValue('');
  }

  const sendMessage = (message) => {
    const url = '/api/chat'; // Always use this endpoint
  
    const data = {
      model: "gpt-3.5-turbo-0301",
      messages: [{ "role": "user", "content": message }],
      useSearchDisabled: !isSearchEnabled // Toggle based on isSearchEnabled
    };

    setIsLoading(true);

    axios.post(url, data).then((response) => {
      setChatLog((prevChatLog) => [...prevChatLog, { type: 'bot', message: response.data.response }]);
      setIsLoading(false);
    }).catch((error) => {
      setIsLoading(false);
      console.log(error);
    });
  };

  return (
    <div className="flex flex-col h-screen bg-gray-100">
      <h1 className="text-gray-800 text-center py-3 font-bold text-3xl">gpt test instance</h1>
      <div className="flex-grow p-6 overflow-y-auto">
        <div className="flex flex-col space-y-4">
          { chatLog.map((message, index) => (
              <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`${message.type === 'user' ? 'bg-gray-300' : 'bg-gray-200'} rounded-lg p-4 text-gray-800 max-w-sm`}>
                  {message.message}
                </div>
              </div>
            ))
          }
          { isLoading &&
            <div className="flex justify-start">
              <div className="bg-gray-200 rounded-lg p-4 text-gray-800 max-w-sm">
                <TypingAnimation />
              </div>
            </div>
          }
        </div>
      </div>
      <form onSubmit={handleSubmit} className="flex-none p-6">
        <div className="flex items-center rounded-lg border border-gray-300 bg-gray-200">  
          <button type="button" 
                  className={`px-4 py-2 ${isSearchEnabled ? 'bg-gray-400' : 'bg-gray-300'} rounded-lg text-gray-800 font-semibold`}
                  onClick={() => setIsSearchEnabled(!isSearchEnabled)}>
            {isSearchEnabled ? "Search On" : "Search Off"}
          </button>
          <input type="text" 
                className="flex-grow px-4 py-2 bg-transparent text-gray-800 focus:outline-none" 
                placeholder="Type your message..." 
                value={inputValue} 
                onChange={(e) => setInputValue(e.target.value)} 
          />
          <button type="submit" 
                  className="bg-gray-300 rounded-lg px-4 py-2 text-gray-800 font-semibold hover:bg-gray-400 transition-colors duration-300">
            Send
          </button>
        </div>
      </form>
    </div>
  );
}
