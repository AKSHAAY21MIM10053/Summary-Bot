import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';





export const Summary = () => {
    const [Message, setMessage] = useState('');
    const [authenticated, setAuthenticated] = useState(false);
    const navigate = useNavigate();

    const[data , setData] = useState([]);

    useEffect(() => {
        if (Message) {
            const timer = setTimeout(() => {
                setMessage('');
            }, 5000);
            return () => clearTimeout(timer); // Cleanup timeout to avoid memory leaks
        }
      }, [Message]);

    useEffect(() => {
        const token = localStorage.getItem('access');
        if (token) {
            axios.get('http://127.0.0.1:8000/Summary', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                setMessage(response.data.Message);
                setAuthenticated(response.data.Authenticated);
                setData(response.data.data);
                if (!response.data.Authenticated) {
                    navigate('/Login');     
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                setMessage('Failed to load data');
                navigate('/Login');
            });
        } else {
            navigate('/Login');
        }
    }, [navigate]);

    const renderData = (data) => {
        if (typeof data === "object" && data !== null) {
            if (Array.isArray(data)) {
                return (
                    <ul>
                        {data.map((item, index) => (
                            <li key={index}>{renderData(item)}</li>
                        ))}
                    </ul>
                );
            } else {
                return (
                    <table className="table table-bordered">
                        <tbody>
                            {Object.entries(data).map(([key, value]) => (
                                <tr key={key}>
                                    <th>{key.replace(/_/g, " ")}</th>
                                    <td>{renderData(value)}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                );
            }
        }
        return data || "N/A"; // Render primitive values (string, number)
    };

  return (
    <>
    <title>Meet Summary</title>
    {Message && (
      <div className=" text-center bgcolour" style={{ minHeight: "20px" }}>
        {Message}
      </div>
    )}
    
      <div className="container" >
                <h2 className="text-center mb-4 rounded" style={{color: "#E2F1E7" }}>Meeting Summary</h2>

                {data.length > 0 ? (
                    data.map((item, index) => (
                        <div key={index} className="card mb-3 shadow-sm">
                            <div className="card-header bg-success text-white d-flex justify-content-between">
                                <h5 className="mb-0">Meeting Details</h5>
                                <span className="small">{item.Formatted_date}</span>
                            </div>

                            <div className="card-body bg-light">
                                {renderData(item)}
                            </div>
                        </div>
                    ))
                ) : (
                    <p className="text-center text-muted">No meeting data available.</p>
                )}
            </div>
        </>
  )
}
