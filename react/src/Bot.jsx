import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';


export const Bot = () => {
    const [Message, setMessage] = useState('');
    const [authenticated, setAuthenticated] = useState(false);
    const navigate = useNavigate();

    const [MeetLink, setMeetLink] = useState('')
    const [CompanyName, setCompanyName] = useState('')

    useEffect(() => {
        const token = localStorage.getItem('access');
        if (token) {
            axios.get('http://127.0.0.1:8000/Bot', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            .then(response => {
                setMessage(response.data.Message);
                setAuthenticated(response.data.Authenticated);
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


    useEffect(() => {
        if (Message) {
            const timer = setTimeout(() => {
                setMessage('');
            }, 5000);
            return () => clearTimeout(timer); // Cleanup timeout to avoid memory leaks
        }
      }, [Message]);


    const handleSubmit = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('access');
        try {
            const response = await axios.post('http://127.0.0.1:8000/Bot', {MeetLink:MeetLink,CompanyName:CompanyName} ,{
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'multipart/form-data',
                }
            });
            const message = response.data.Message;
            setMessage(message);
        } catch (error) {
            console.error("POST method error", error);
            setMessage('failed to send data');
        }
    }


  return (
    <>
    <title>Bot</title>
    {Message && (
      <div className=" text-center bgcolour" style={{ minHeight: "20px" }}>
        {Message}
      </div>
    )}
    <div className="container d-flex justify-content-center align-items-center min-vh-100">
  <div className="card p-4 shadow-lg rounded" style={{ width: "400px", background: "#E2F1E7" }}>
    <h2 className="text-center mb-4">Meeting Details</h2>
    <form onSubmit={handleSubmit}>
      <div className="mb-3">
        <label htmlFor="MeetLink" className="form-label">Meet Link</label>
        <input
          type="text"
          className="form-control"
          placeholder="Your Meet Link"
          value={MeetLink}
          onChange={(e) => setMeetLink(e.target.value)}
          name="MeetLink"
          id="MeetLink"
          required
        />
      </div>

      <div className="mb-3">
        <label htmlFor="CompanyName" className="form-label">Company Name</label>
        <input
          type="text"
          className="form-control"
          placeholder="Company Name"
          value={CompanyName}
          onChange={(e) => setCompanyName(e.target.value)}
          name="CompanyName"
          id="CompanyName"
          required
        />
      </div>

      <div className="d-grid">
        <button type="submit" className="btn btn-primary">Submit</button>
      </div>
    </form>
  </div>
</div>

    </>
  )
}
