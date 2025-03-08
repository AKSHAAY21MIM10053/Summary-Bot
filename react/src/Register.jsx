import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom';

export const Register = () => {
    const [Message, setMessage] = useState('');
    const [authenticated, setAuthenticated] = useState(false);
    const navigate = useNavigate();
    
    const [Name, setName] = useState('')
    const [MobileNumber, setMobileNumber] = useState('')
    const [Email, setEmail] = useState('')
    const [Otp, setOtp] = useState("")
    const [Password, setPassword] = useState("")

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
    

    const generateotp = async (e) => { 
        e.preventDefault();
        try {
          const response = await axios.post('http://127.0.0.1:8000/GenerateOtp', {
            Name: Name,
            Email: Email
          });
          setMessage(response.data.Message);
        } catch (error) {
          console.error("POST method error", error);
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
    
      
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:8000/Register', {
                Name: Name,
                Email: Email,
                Password: Password,
                MobileNumber: MobileNumber,
                Otp: Otp
            });
            const message = response.data.Message;
            setMessage(message);
            if (message === "Done") {
                alert("Registration successful");
                navigate('/');
            } else {
                setMessage(message);
            }
        } catch (error) {
            console.error("POST method error", error);
            setMessage('Registration failed');
        }
    }


  return (
    <>
    <title>Register</title>
    {Message && (
      <div className=" text-center bgcolour" style={{ minHeight: "20px" }}>
        {Message}
      </div>
    )}

<div className="d-flex justify-content-center align-items-center vh-100" style={{ backgroundColor: "#3C3D37" }}>
  <div className="card p-4 shadow-lg" style={{ width: "40rem", borderRadius: "12px", background: "#E2F1E7" }}>
    <h2 className="text-center mb-4">Register Page</h2>

    <form className="row g-3" onSubmit={handleSubmit}>

      <div className="col-md-6">
        <label htmlFor="Name" className="form-label">Full Name</label>
        <input type="text" className="form-control" placeholder="Enter your name" 
               value={Name} onChange={(e) => setName(e.target.value)} required />
      </div>

      <div className="col-md-6">
        <label htmlFor="MobileNumber" className="form-label">Mobile Number</label>
        <input type="tel" className="form-control" placeholder="Enter your mobile number" 
               value={MobileNumber} onChange={(e) => setMobileNumber(e.target.value)} required />
      </div>

      <div className="col-md-12">
        <label htmlFor="Email" className="form-label">Email Address</label>
        <input type="email" className="form-control" placeholder="Enter your email" 
               value={Email} onChange={(e) => setEmail(e.target.value)} required />
      </div>

      <div className="col-md-12">
        <label htmlFor="Password" className="form-label">Password</label>
        <input type="password" className="form-control" placeholder="Create a password" 
               value={Password} onChange={(e) => setPassword(e.target.value)} required />
      </div>

      {/* OTP Input and Generate Button - Aligned */}
      <div className="col-md-12 d-flex align-items-end">
        <div className="flex-grow-1">
          <label htmlFor="Otp" className="form-label">Enter OTP</label>
          <input type="number" className="form-control" placeholder="Enter OTP" 
                 value={Otp} onChange={(e) => setOtp(e.target.value)} required />
        </div>
        <button type="button" className="btn btn-outline-primary ms-2" onClick={generateotp}>
          Get OTP
        </button>
      </div>

      <div className="col-12 text-center">
        <button type="submit" className="btn btn-primary w-100">Register</button>
      </div>

      <p className="text-center mt-2">
        Already have an account? <Link to="/Login" className="linkdeco text-primary">Login</Link>
      </p>

    </form>
  </div>
</div> 


    {/* <form onSubmit={handleSubmit}>
        <label htmlFor="Name">Name</label>
        <input type="text" placeholder='Your Name' value={Name} onChange={(e)=> setName(e.target.value)} name="Name" id="Name" required></input>
        <label htmlFor="MobileNumber">Number</label>
        <input type="number" placeholder='Yor Mobile Number' value={MobileNumber} onChange={(e)=> setMobileNumber(e.target.value)} name="MobileNumber" id="MobileNumber" required></input>
        <label htmlFor="Email">Email</label>
        <input type="email" placeholder='Yor Email' value={Email} onChange={(e)=> setEmail(e.target.value)} name="Email" id="Email" required></input>
        <label htmlFor="Otp">Enter Otp</label>
        <input type="number" placeholder='Otp ' value={Otp} onChange={(e)=> setOtp(e.target.value)} name="Otp" id="Otp" required></input>
        <label htmlFor="Password">Password</label>
        <input type="password" placeholder='Set Your Password' value={Password} onChange={(e)=> setPassword(e.target.value)} name="Password" id="Password" required></input>

        <button type='button' onClick={generateotp} name='Generate otp'>Generate Otp</button>
        <button type='submit' name='submit'>Register</button>  

    </form>

    <Link to="/Login" className="linkdeco">Already have account ? Login</Link> */}
    
    </>
  )
}
