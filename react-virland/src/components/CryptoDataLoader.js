import React, { useState, useEffect } from 'react';
import Chart from 'react-apexcharts'; 
import { useSelector } from 'react-redux';

function CryptoDataLoader({ selectedCrypto }) {
  const selectedValue = useSelector(state => state.selection.selectedValue);
  const [chartData, setChartData] = useState({
    options: {
        chart: {
            type: 'line',  // Assuming you want a line chart for simplicity
            height: 350
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
            x: {
                format: 'dd MMM yyyy'
            }
        }
    },
    series: [
        {
            name: 'Historical Data',
            data: []  // This will be filled with historical data
        },
        {
            name: 'Predicted Data',
            data: []  // This will be filled with prediction data
        }
    ]
});

  const [volatility, setVolatility] = useState('');
  const [loading, setLoading] = useState(false);
  const [predictions, setPredictions] = useState([]);

  useEffect(() => {
    console.log(`Selected Crypto from Redux Store: ${selectedValue}`);
    console.log(`selectedCrypto ${selectedCrypto}`)
    /*if (selectedCrypto) {
      loadCryptoData();
    }*/
  }, [selectedCrypto]);

  const loadCryptoData = async () => {
    setLoading(true);
    // Fetch and process historical data, then set it
    const historicalData = ""/* fetched and processed data */;
    const predictionData = ""/* fetched and processed prediction data */;

    setChartData(prevState => ({
        ...prevState,
        series: [
            { ...prevState.series[0], data: historicalData },
            { ...prevState.series[1], data: predictionData }
        ]
    }));
    await showMonthGraph();
    await fetchVolatilityIndex();
    setLoading(false);
  };

  const showMonthGraph = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5005/crypto-data/${selectedCrypto}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log(`APIDATA: {data}`); 
      // Transform data to fit ApexCharts format here
      const seriesData = data.map(item => ({
        x: new Date(item.date),
        y: [item.open_price, item.close_price, item.avg_volume, item.close]
      }));

      setChartData(prevState => ({
        ...prevState,
        series: [{ data: seriesData }]
      }));
    } catch (error) {
      console.error('Fetch error:', error);
    }
  };

  async function predictAndShowGraph() {
    setLoading(true);
    try {
        const response = await fetch(`http://127.0.0.1:5005/crypto-data/${selectedCrypto}`);
        const data = await response.json();

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
        let lastDate = new Date(data[data.length - 1].date);
        const predictionSeries = predictions.map((pred, index) => {
            let newDate = new Date(lastDate);
            newDate.setDate(newDate.getDate() + index + 1);
            return {
                x: newDate.getTime(),
                y: pred
            };
        });

        setPredictions(predictionSeries);
    } catch (error) {
        console.error('Error:', error);
    }
    setLoading(false);
  }

  const fetchVolatilityIndex = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5005/volatility/${selectedCrypto}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setVolatility(`${data.volatility_index.toFixed(2)}%`);
    } catch (error) {
      console.error('Failed to fetch the volatility index:', error);
    }
  };

  function getVolatilityColor(volatility) {
    const value = parseFloat(volatility.replace('%', '')); // Strip the percent sign and convert to float
    if (value <= 20) {
        return 'green'; // Low volatility
    } else if (value <= 40) {
        return 'purple'; // Medium volatility
    } else {
        return 'red'; // High volatility
    }
}

  return (
    <div>
      {loading ? <p>Loading...</p> : (
        <>
          <Chart 
            options={chartData.options}
            series={chartData.series}
            type="candlestick"
            height={350}
            width={1000}
          />
          <div id="volatilityLegend">
            <p>Volatility Index Legend:</p>
            <div className="legend-item"><span className="legend-color" style={{backgroundColor: 'green'}}></span> Low</div>
            <div className="legend-item"><span className="legend-color" style={{backgroundColor: 'purple'}}></span> Medium</div>
            <div className="legend-item"><span className="legend-color" style={{backgroundColor: 'red'}}></span> High</div>
            <div>
            <p id="volatilityIndex">Volatility Index: <span id="volatilityValue" style={{ color: getVolatilityColor(volatility) }}>{volatility}</span></p>
            </div>
          </div>
          
        </>
      )}
    </div>
  );
}

export default CryptoDataLoader;
