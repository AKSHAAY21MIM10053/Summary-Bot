import './App.css'
import {Route , Routes} from 'react-router-dom'
import { Home } from './Home'
import { Register } from './Register'
import { Login } from './Login'
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { UploadData } from './UploadData'
import { Bot } from './Bot'
import 'bootstrap/dist/css/bootstrap.min.css'; // Import styles
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // Import Bootstrap JavaScript
import "bootstrap-icons/font/bootstrap-icons.css";
import { Summary } from './Summary'




function App() {
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const refreshToken = localStorage.getItem('refresh');
    const accessToken = localStorage.getItem('access');
    console.log("refreshToken", refreshToken);  
    console.log("accessToken", accessToken);
    if (!refreshToken) {
        console.log("No refresh token found.")
        setMessage('No refresh token found.');
        navigate('/login');  // Redirect to login if no access token
        return;
    }
    try {
        const response = await axios.post('http://127.0.0.1:8000/Logout',{ refresh_token: refreshToken },{
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            }
    });
    if (response.status === 205) {
        localStorage.clear();
        setMessage('Logout successful');
        navigate('/');
    } else {
        setMessage('Logout failed');
    }
    } catch (error) {
        console.error("POST method error", error);
        setMessage('Logout failed');
        if (error.response && error.response.status === 401) {
            setMessage('Session expired. Please log in again.');
            console.log("session expired ..........")
            localStorage.clear();
            navigate('/login')}
    }
}

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
  
    <nav class="navbar navbarcolour navbar-expand-lg  " aria-label="Thirteenth navbar example">
      <div class="container-fluid">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarsExample11" aria-controls="navbarsExample11" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse d-lg-flex" id="navbarsExample11">
          <a class="navbar-brand col-lg-3 me-0" href="">Interview Bot</a>
          <ul class="navbar-nav col-lg-6 justify-content-lg-center">
            <li class="nav-item">
              <a class="nav-link active"  href="/">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/UploadData">Upload Data</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/Bot">Bot</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/Register">Register</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/Login">Login</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/Summary">Meet Summary</a>
            </li>
          </ul>
          <div class="d-lg-flex col-lg-3 justify-content-lg-end">
          <button onClick={handleSubmit} className='btn btn-sm  me-md-2 btn-secondary'>Logout</button>
          </div>
        </div>
      </div>
    </nav>


    {message && (
      <div className=" text-center" style={{ minHeight: "20px" }}>
        {message}
      </div>
    )}

    {/* <p>{message}</p>
    <button onClick={handleSubmit}>logout</button> */}
    <div className='increasevph bodycolour'>
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/Register" element={<Register/>} />
        <Route path="/Login" element={<Login/>} />
        <Route path="/UploadData" element={<UploadData/>} />
        <Route path="/Bot" element={<Bot/>} />
        <Route path="/Summary" element={<Summary/>}/>
      </Routes>
    </div>
    
   
  <footer class="mt-auto d-flex footbarcolour flex-wrap justify-content-between align-items-center py-3 border-top">
    <div class="col-md-4 d-flex align-items-center">
      <a href="/" class="mb-3 me-2 mb-md-0 text-body-secondary text-decoration-none lh-1">
        <svg class="bi" width="30" height="24"><use xlink:href="#bootstrap"></use></svg>
      </a>
      <span class="mb-3 mb-md-0 text-body-secondary">© 2024 Company, Inc</span>
    </div>

    <ul class="nav col-md-4 justify-content-end list-unstyled d-flex">
      <li class="ms-3"><a class="text-body-secondary" href="https://www.instagram.com/akshaay_10/" target="_blank"><i class="bi bi-instagram"></i></a></li>
      <li class="ms-3"><a class="text-body-secondary" href="https://wa.me/9150854710" target="_blank"><i class="bi bi-whatsapp"></i></a></li>
      <li class="ms-3"><a class="text-body-secondary" href="https://www.linkedin.com/in/akshaay-10-" target="_blank"><i class="bi bi-linkedin"></i></a></li>
      <li class="ms-3"></li>
    </ul>
  </footer>
    </>
  )
}

export default App
