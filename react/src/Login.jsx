import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export const Login = () => {
    const [Message, setMessage] = useState('');
    const [authenticated, setAuthenticated] = useState(false);
    const navigate = useNavigate();
    const [Name, setName] = useState('');
    const [Password, setPassword] = useState('');

        useEffect(() => {
            const token = localStorage.getItem('access');
            if (token || authenticated) {
                navigate('/');
            } else {
                axios.get('http://127.0.0.1:8000/CheckAuth')
                    .then(response => {
                        setMessage(response.data.Message);
                        setAuthenticated(response.data.Authenticated);
                        if (response.data.Authenticated) {
                            navigate('/');
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching data:', error);
                        setMessage('Failed to load data');
                    });
            }
        }, [navigate, authenticated]);

        const handleSubmit = async (e) => {
            e.preventDefault();
            
            // Ensure Name and Password are not empty or undefined
            if (!Name || !Password) {
                setMessage('Name and Password are required');
                return;
            }
        
            try {
                const response = await axios.post('http://127.0.0.1:8000/Login', {
                    Name: Name,
                    Password: Password
                });
        
                const message = response.data.Message;
                setMessage(message);
                console.log('Login Response:', response.data);  // Log response for debugging
        
                if (message === "Done") {
                    localStorage.setItem('access', response.data.access);
                    localStorage.setItem('refresh', response.data.refresh);
                    alert("Login successful");
                    navigate('/');
                } else {
                    setMessage(message);
                }
            } catch (error) {
                console.error("POST method error", error);
        
                if (error.response) {
                    // Handle specific error response data
                    const errorMessage = error.response.data.Message || 'Login failed';
                    setMessage(errorMessage);
                } else {
                    setMessage('Login failed due to network/server error');
                }
            }
        };

        useEffect(() => {
                if (Message) {
                    const timer = setTimeout(() => {
                        setMessage('');
                    }, 5000);
                    return () => clearTimeout(timer); // Cleanup timeout to avoid memory leaks
                }
              }, [Message]);
        


  return (
    <>
    
    <title>login</title>
    {Message && (
      <div className=" text-center bgcolour" style={{ minHeight: "20px" }}>
        {Message}
      </div>
    )}

<div className="container d-flex justify-content-center align-items-center min-vh-100">
  <div className="card p-4 shadow-lg rounded" style={{ width: "400px" , background:"#E2F1E7" }}>
    <h2 className="text-center mb-4">Login</h2>
    <form onSubmit={handleSubmit}>
      <div className="mb-3">
        <label htmlFor="Name" className="form-label">Name</label>
        <input
          type="text"
          className="form-control"
          placeholder="Your Name"
          value={Name}
          onChange={(e) => setName(e.target.value)}
          name="Name"
          id="Name"
          required
        />
      </div>

      <div className="mb-3">
        <label htmlFor="Password" className="form-label">Password</label>
        <input
          type="password"
          className="form-control"
          placeholder="Your Password"
          value={Password}
          onChange={(e) => setPassword(e.target.value)}
          name="Password"
          id="Password"
          required
        />
      </div>

      <div className="d-grid">
        <button type="submit" className="btn btn-primary">Login</button>
      </div>
    </form>
  </div>
</div>


    </>
  )
}
