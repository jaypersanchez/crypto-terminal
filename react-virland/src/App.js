import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';
import CryptoDataLoader from './components/CryptoDataLoader';
import { useSelector, useDispatch } from 'react-redux';
import { setSelectedValue } from './actions';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  // this should be setup in the redux
  const [crypto, setCrypto] = useState('bitcoin'); // Default selection
  const selectedValue = useSelector(state => state.selection.selectedValue);
  const dispatch = useDispatch();

  const performSearch = async () => {
    console.log(query);
    const url = `http://127.0.0.1:5005/search`;
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      const data = await response.json();
      console.log(data);
      setResults(data); // Assuming data is an array of strings or objects
    } catch (error) {
      console.error('Error:', error);
    }
  };

  
  const handleChange = e => {
    console.log("Selected Crypto: ", e.target.value);  // This will log the crypto selected
    dispatch(setSelectedValue(e.target.value)) //for redux
    setCrypto(e.target.value);
  };

  return (
    <div className="App">
      <div className='Top-content'>
          <div className="search-box">
            <textarea
              className="sort-box cursor-pointer align-self-center"
              id="query"
              placeholder="Ask Virland"
              rows="4"
              value={query}
              onChange={e => setQuery(e.target.value)}
            ></textarea>
            <div className="row row-no-gutter">
              <button onClick={performSearch}>Ask Virland</button>
            </div>
          </div>
          <div className="results">
            <h4>Virland's Response</h4>
            <ul id="searchResults">
              {results.map((item, index) => (
                <li key={index}>{item}</li> // Adjust according to the structure of 'item' if it's an object
              ))}
            </ul>
          </div>
      </div>
      <div className="Analytics">
        <div className="Analytics-left">
        <div className="controls">
            <select
              id="cryptoSelect"
              className="dropdown-sort"
              value={selectedValue}
              onChange={handleChange}
            >
              <option value="bitcoin">BTC</option>
              <option value="ethereum">ETH</option>
              <option value="solana">SOL</option>
              <option value="matic-network">MATIC</option>
            </select>
            
          </div>
        </div>
        <div className="Analytics-right">
          <div className='controls'>
            <div className="row row-no-gutter">
              <CryptoDataLoader selectedCrypto={selectedValue} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}


export default App;
