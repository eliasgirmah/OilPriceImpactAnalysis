// src/Dashboard.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { Line } from 'react-chartjs-2';

const Dashboard = () => {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/data')
      .then(response => {
        const fetchedData = response.data.map(item => ({
          ...item,
          date: new Date(item.date).getTime() // Convert date to timestamp
        }));
        setData(fetchedData);
        setFilteredData(fetchedData);
      })
      .catch(error => {
        console.error("Error fetching data:", error);
      });
  }, []);

  useEffect(() => {
    if (startDate && endDate) {
      const filtered = data.filter(item =>
        item.date >= startDate.getTime() && item.date <= endDate.getTime()
      );
      setFilteredData(filtered);
    } else {
      setFilteredData(data);
    }
  }, [startDate, endDate, data]);

  const chartData = {
    labels: filteredData.map(item => new Date(item.date).toLocaleDateString()),
    datasets: [
      {
        label: 'Brent Oil Price',
        data: filteredData.map(item => item.price),
        borderColor: 'rgba(75,192,192,1)',
        fill: false,
      },
    ],
  };

  return (
    <div>
      <h2>Brent Oil Price Dashboard</h2>
      <div>
        <label>Start Date:</label>
        <DatePicker selected={startDate} onChange={(date) => setStartDate(date)} />
        <label>End Date:</label>
        <DatePicker selected={endDate} onChange={(date) => setEndDate(date)} />
      </div>
      <div>
        <Line data={chartData} />
      </div>
    </div>
  );
};

export default Dashboard;
