import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export const UploadData = () => {
    const [message, setMessage] = useState('');
    const [authenticated, setAuthenticated] = useState(false);
    const navigate = useNavigate();
    const [UploadFile,setUploadFile] = useState(null)

    useEffect(() => {
        const token = localStorage.getItem('access');
        if (token) {
            axios.get('http://127.0.0.1:8000/UploadData', {
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

    const handleSubmit = async (e) => { 
        e.preventDefault();
        try {
            if (!UploadFile) {
                alert("Please upload a document.");
                setMessage("Please upload a document.");
                return;
            }
            const formData = new FormData();
            formData.append('file', UploadFile);

            const token = localStorage.getItem('access');
            const fileUploadResponse = await axios.post('http://127.0.0.1:8000/UploadData', formData, {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'multipart/form-data',
                }
            });
            setMessage(fileUploadResponse.data.Message);
            setUploadFile(null);  // Reset the file input
        } catch (error) {
            console.error('Error uploading file:', error);
            setMessage('Failed to upload file');
        }
    };

    useEffect(() => {
        if (message) {
            const timer = setTimeout(() => {
                setMessage('');
            }, 5000);
            return () => clearTimeout(timer); // Cleanup timeout to avoid memory leaks
        }
      }, [message]);

  return (
    <>
    <title>Upload File</title>
    {message && (
      <div className=" text-center bgcolour" style={{ minHeight: "20px" }}>
        {message}
      </div>
    )}
    <div className="container d-flex justify-content-center align-items-center min-vh-100">
  <div className="card p-4 shadow-lg rounded" style={{ width: "400px", background: "#E2F1E7" }}>
    <h2 className="text-center mb-4">Upload Document</h2>
    <form onSubmit={handleSubmit}>
      <div className="mb-3">
        <label htmlFor="UploadFile" className="form-label">Proof Document</label>
        <input
          type="file"
          className="form-control"
          accept="application/pdf"
          onChange={(e) => setUploadFile(e.target.files[0])}
          name="UploadFile"
          id="UploadFile"
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
