async function performSearch() {
    const query = document.getElementById('query').value;
    console.log(`${query}`)
    const resultsElement = document.getElementById('searchResults');
    resultsElement.innerHTML = ''; // Clear previous results
    const url = `http://127.0.0.1:5005/search`;
    // Here, you'd typically make an API call to get search results based on the query
    // For demonstration, we're just adding a mock result:
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Assuming data is an array of strings or objects
        data.forEach(item => {
            const listItem = document.createElement('li');
            // If 'item' is a string:
            listItem.textContent = item;
            // If 'item' is an object, adjust accordingly, e.g.:
            // listItem.textContent = `Input: ${item.input}, Output: ${item.output}`;
            resultsElement.appendChild(listItem);
        });
    })
    .catch(error => console.error('Error:', error));
}

async function calculateSMA(data, period) {
    let sma = data.map((val, index, arr) => {
        if (index < period - 1) return null; // Not enough data to calculate SMA
        let sum = 0;
        for (let i = 0; i < period; i++) {
            sum += arr[index - i].y[3]; // Assuming the 'close' price is at index 3
        }
        return { x: val.x, y: parseFloat((sum / period).toFixed(2)) };
    }).filter(v => v); // Remove initial null values

    return sma;
}

async function showCurrentPrice() {
    const priceInfoElement = document.getElementById('priceInfo');
    const recentDataElement = document.getElementById('recentData');
    const selectedCrypto = document.getElementById('cryptoSelect').value;
    try {
        // Replace 'bitcoin' with a variable if needed, or fetch it from another element
        const response = await fetch(`http://127.0.0.1:5005/crypto-price/${selectedCrypto}`);
        
        if (!response.ok) {
            // If the response is not successful, throw an error
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Assuming the data structure includes 'current_price_usd' or adjust based on actual structure
        // Example: { "current_price_usd": 12345.67 }
        priceInfoElement.textContent = `Bitcoin Current Price: $${data.current_price_usd}`;
        
    } catch (error) {
        console.error('Fetch error:', error);
        priceInfoElement.textContent = 'Failed to fetch current prices.';
    }
}

async function showMonthGraph() {
    const priceInfoElement = document.getElementById('priceInfo');
    const recentDataElement = document.getElementById('recentData');
    const selectedCrypto = document.getElementById('cryptoSelect').value;
    try {
        const response = await fetch(`http://127.0.0.1:5005/crypto-data/${selectedCrypto}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        const currentDate = new Date().toISOString().split('T')[0]; // Current date in YYYY-MM-DD format

        // Display the basic price info as before
        /*priceInfoElement.textContent = `${selectedCrypto.toUpperCase()} Current Price: $${data.current_price_usd} as of ${currentDate}\n` +
                                        `Market Cap: $${data.market_cap_usd}\n` +
                                        `24h Trading Volume: $${data["24h_volume_usd"]}`;*/

        // Additionally, display the most recent data for the cryptocurrency
        // Assuming the data structure includes keys like 'date', 'open_price', 'close_price', and 'avg_volume'
        // And assuming there might be multiple records, we concatenate them into a single string
        /*let recentDataText = "Recent Data:\n";
        data.forEach((record) => {
            recentDataText += `Date: ${record.date}, Open Price: $${record.open_price}, Close Price: $${record.close_price}, Avg. Volume: $${record.avg_volume}\n`;
        });
        recentDataElement.textContent = recentDataText;*/
        // Transform the fetched data into the format ApexCharts expects
        let chartData = data.map(record => {
            let date = new Date(record.date).getTime(); // Convert date to timestamp
            // Assuming open_price and close_price can serve as high and low for simplicity
            let open = parseFloat(record.open_price);
            let high = open; // Simplify, ideally use actual high
            let low = parseFloat(record.close_price); // Simplify, ideally use actual low
            let close = low; // Simplify, ideally use actual close
            return {x: date, y: [open, high, low, close]};
        });
        // Empty the chart container before rendering a new chart
        // Assuming chartData is already prepared
        let sma20 = calculateSMA(chartData, 20);
        let sma50 = calculateSMA(chartData, 50);
        document.querySelector("#chart").innerHTML = '';
        // Setup and render the chart
        // Setup and render the chart with SMAs
        var options = {
            series: [
                {
                    name: 'Candlestick',
                    type: 'candlestick',
                    data: chartData
                },
                {
                    name: 'SMA 20 Days',
                    type: 'line',
                    data: sma20
                },
                {
                    name: 'SMA 50 Days',
                    type: 'line',
                    data: sma50
                }
            ],
            chart: {
                height: 350,
                type: 'line' // Set to 'line' to enable mixing types
            },
            stroke: {
                width: [1, 2, 2], // Adjust line widths as needed
                curve: 'smooth'
            },
            title: {
                text: `${selectedCrypto.toUpperCase()} Price Chart`,
                align: 'left'
            },
            xaxis: {
                type: 'datetime'
            },
            yaxis: {
                tooltip: {
                    enabled: true
                }
            },
            tooltip: {
                shared: true,
                intersect: false,
                y: {
                    formatter: function (y) {
                        if (typeof y !== "undefined") {
                            return `${y.toFixed(2)}`;
                        }
                        return y;
                    }
                }
            }
        };
        
        var chart = new ApexCharts(document.querySelector("#chart"), options);
        chart.render();
        showCurrentPrice() 
    } catch (error) {
        console.error('Fetch error:', error);
        priceInfoElement.textContent = 'Failed to fetch current prices.';
        recentDataElement.textContent = ''; // Clear the recent data section on error
    }
}

async function connectWallet() {
    if (window.ethereum) { // Check if MetaMask is installed
        try {
            const accounts = await window.ethereum.request({ method: 'eth_requestAccounts' }); // Request account access
            const account = accounts[0]; // Get the first account
            // Get the chain ID
            const chainId = await window.ethereum.request({ method: 'eth_chainId' });

            // Map the chain ID to a network name
            const networkName = getNetworkName(chainId);
            document.getElementById('connectWalletButton').innerText = `${networkName}: ${account}`;
            
            // Optionally, get and display the wallet's balance
            const balance = await window.ethereum.request({
                method: 'eth_getBalance',
                params: [account, 'latest']
            });
            const formattedBalance = ethers.utils.formatEther(balance); // Format balance
            document.getElementById('connectWalletButton').innerText += ` - Balance: ${formattedBalance} ETH`;
            
        } catch (error) {
            console.error(error);
        }
    } else {
        console.log('MetaMask is not installed!');
    }
}

function getNetworkName(chainId) {
    // Mapping of common chain IDs to network names
    const networkMap = {
        '0x1': 'Ethereum Mainnet',
        '0x3': 'Ropsten Testnet',
        '0x4': 'Rinkeby Testnet',
        '0x5': 'Goerli Testnet',
        '0x2a': 'Kovan Testnet',
        '0x89': 'Polygon Mainnet',
        '0x13881': 'Polygon Mumbai Testnet',
        // Add other networks as needed
    };

    return networkMap[chainId] || 'Unknown Network';
}

async function fetchSwapQuote(sellToken, buyToken) {
    // Example URL, adjust according to the actual API you're using
    const apiUrl = `https://api.example.com/swap?sellToken=${sellToken}&buyToken=${buyToken}`;
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        return { price: data.price }; // Simplified, adjust based on the real data structure
    } catch (error) {
        console.error('Fetch error:', error);
        return null;
    }
}

async function fetchBestSwapPrices(sellToken) {
    // Define a list of assets for swapping. This could also be dynamic based on your app's context.
    const buyTokens = ['ETH', 'DAI', 'USDC'];
    const sellAmount = ethers.utils.parseUnits('1.0', '18').toString(); // Example: selling 1.0 token. Adjust the decimals as needed.

    const promises = buyTokens.map(async (buyToken) => {
        const response = await fetch(`https://api.0x.org/swap/v1/quote?sellToken=${sellToken}&buyToken=${buyToken}&sellAmount=${sellAmount}`);
        if (response.ok) {
            const data = await response.json();
            return { buyToken, price: data.price, to: data.to, estimatedGas: data.estimatedGas };
        }
        return { buyToken, error: 'Failed to fetch price' };
    });

    return Promise.all(promises);
}

async function showBestSwapPrices() {
    const selectedCrypto = document.getElementById('cryptoSelect').value;
    // Define a few example assets to swap to or make this dynamic
    const assetsToCheck = ['ETH', 'DAI', 'USDC']; // Example tokens

    const swapPricesContainer = document.getElementById('swapPrices');
    swapPricesContainer.innerHTML = ''; // Clear previous results

    for (let asset of assetsToCheck) {
        const quote = await fetchSwapQuote(selectedCrypto, asset);
        if (quote) {
            // Display the swap price. Adjust according to the data structure
            const priceElement = document.createElement('p');
            priceElement.textContent = `Swap ${selectedCrypto} to ${asset}: ${quote.price} ${asset}`;
            swapPricesContainer.appendChild(priceElement);
        } else {
            // Handle the error or no data case
            swapPricesContainer.textContent = 'Could not fetch swap prices.';
        }
    }
}

async function predictAndShowGraph() {
    const selectedCrypto = document.getElementById('cryptoSelect').value;
    try {
        const response = await fetch(`http://127.0.0.1:5005/crypto-data/${selectedCrypto}`);
        const data = await response.json();

        // Now send this data to the Flask endpoint for prediction
        const predictResponse = await fetch('http://127.0.0.1:5005/predict-close-price', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!predictResponse.ok) {
            throw new Error(`HTTP error! status: ${predictResponse.status}`);
        }

        const predictions = await predictResponse.json();
        
        // Assuming the dates are sequential and starting from the last date in `data`
        let lastDate = new Date(data[data.length - 1].date); // Assuming `data` has a `date` property
        const predictionDates = predictions.map((_, index) => {
            let newDate = new Date(lastDate);
            newDate.setDate(newDate.getDate() + index + 1); // Increment date by 1 for each prediction
            return newDate.getTime(); // Convert to timestamp
        });

        // Creating a series for ApexCharts
        const predictionSeries = predictions.map((pred, index) => {
            return {
                x: predictionDates[index],
                y: pred
            };
        });

        // Graphing with ApexCharts
        var options = {
            chart: {
                type: 'scatter',
                height: 350
            },
            series: [{
                name: 'Predicted Close Price',
                data: predictionSeries
            }],
            xaxis: {
                type: 'datetime',
                title: {
                    text: 'Date'
                }
            },
            yaxis: {
                title: {
                    text: 'Close Price'
                }
            },
            tooltip: {
                x: {
                    format: 'dd MMM yyyy'
                }
            }
        };

        var chart = new ApexCharts(document.querySelector("#predictionChart"), options);
        chart.render();
        
    } catch (error) {
        console.error('Error:', error);
    }
}

// Don't forget to call predictAndShowGraph() when needed, for example after selecting a crypto

document.getElementById('connectWalletButton').addEventListener('click', connectWallet);
