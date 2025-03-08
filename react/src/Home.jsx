import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import HeroImage from "../src/image/Heroimage.webp";
import { Link } from "react-router-dom";

export const Home = () => {
    const [message, setMessage] = useState('');
    const [authenticated, setAuthenticated] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
      const token = localStorage.getItem('access');
      if (token) {
          axios.get('http://127.0.0.1:8000/CheckAuth', {
              headers: {
                  'Authorization': `Bearer ${token}`
              }
          })
          .then(response => {
            setMessage(response.data.Message);
            setAuthenticated(response.data.Authenticated);
        })
        .catch(error => {
            if (error.response && error.response.status === 401) {
                // Handle 401 specifically
                setMessage('try to register');
            } else {
                console.error('Error fetching data:', error);
                setMessage('Failed to load data');
            }
        });
      } else {
          setMessage('Please login.');
      }
  }, [navigate]);
  

  return (
    <>
    <title>Home Page</title>

    {authenticated ? (
        <>
    <div class="container heroback rounded">
    <div class="row flex-lg-row-reverse align-items-center g-5 py-5">
      <div class="col-10 col-sm-8 col-lg-6">
        <img src={HeroImage} class="d-block mx-lg-auto rounded img-fluid" alt="Bootstrap Themes" width="700" height="500" loading="lazy"/>
      </div>
      <div class="col-lg-6">
        <h1 class="display-5 fw-bold text-body-emphasis lh-1 mb-3">AI Interview Insights</h1>
        <p class="fs-5 text-body-emphasis">A powerful tool designed to help interviewers efficiently summarize candidate performance and make informed hiring decisions. It also provides valuable feedback for candidates, allowing them to identify mistakes and improve for future interviews. Ideal for professional recruitment and self-assessment.</p>
        <div class="d-grid gap-2 d-md-flex justify-content-md-start">
        <Link to="/Bot" className="btn btn-primary btn-lg px-4 me-md-2">Try Bot</Link>
        </div>
      </div>
    </div>
  </div>

  <div class="container px-4 py-5 heroback rounded" id="featured-3">
    <h2 class=" text-body-emphasis lh-1 ">Steps To Use</h2>
    <div class="row g-4 py-5 row-cols-1 row-cols-lg-3">
      <div class="feature col">
        <div class="feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3">
        <i class="bi bi-file-earmark-pdf-fill"></i>
        </div>
        <h3 class="fs-2 text-body-emphasis"> Upload Your Resume & Project Details</h3>
        <p>Simply upload your resume and project documents in PDF format. This allows the bot to understand your background and provide relevant responses during the interview.</p>
        <a href="/UploadData" class="icon-link">
          Upload File
          <svg class="bi"><use xlink:href="#chevron-right"></use></svg>
        </a>
      </div>
      <div class="feature col">
        <div class="feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3">
        <i class="bi bi-globe2"></i>
        </div>
        <h3 class="fs-2 text-body-emphasis">Real-Time Interview Assistance</h3>
        <p>During the interview, the bot joins the meeting and listens to the conversation. When a question is asked, it processes the query and provides appropriate answers in the comments, ensuring a smoother and more confident interview experience.</p>
        <a href="/Bot" class="icon-link">
          Meet Bot
          <svg class="bi"><use xlink:href="#chevron-right"></use></svg>
        </a>
      </div>
      <div class="feature col">
        <div class="feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3">
        <i class="bi bi-clipboard2-data"></i>
        </div>
        <h3 class="fs-2 text-body-emphasis"> Post-Interview Summary & Feedback</h3>
        <p>After the interview, the bot generates a detailed summary, highlighting key discussions, strengths, and areas for improvement. This helps interviewers assess candidates effectively and allows candidates to refine their approach for future interviews.</p>
        <a href="/Summary" class="icon-link">
          Summary
          <svg class="bi"><use xlink:href="#chevron-right"></use></svg>
        </a>
      </div>
    </div>
  </div>     
                
        </>
    ) : (
        <>
    <div class="container heroback rounded">
    <div class="row flex-lg-row-reverse align-items-center g-5 py-5">
      <div class="col-10 col-sm-8 col-lg-6">
        <img src={HeroImage} class="d-block mx-lg-auto rounded img-fluid" alt="Bootstrap Themes" width="700" height="500" loading="lazy"/>
      </div>
      <div class="col-lg-6">
        <h1 class="display-5 fw-bold text-body-emphasis lh-1 mb-3">AI Interview Insights</h1>
        <p class="fs-5 text-body-emphasis">A powerful tool designed to help interviewers efficiently summarize candidate performance and make informed hiring decisions. It also provides valuable feedback for candidates, allowing them to identify mistakes and improve for future interviews. Ideal for professional recruitment and self-assessment.</p>
        <div class="d-grid gap-2 d-md-flex justify-content-md-start">
        <Link to="/Login" className="btn Loginbutton btn-primary btn-lg px-4 me-md-2">Login</Link>
        <Link to="/Register" className="btn Registerbutton btn-primary btn-lg px-4 me-md-2">Register</Link>
        </div>
      </div>
    </div>
  </div>

  <div class="container px-4 py-5 heroback rounded" id="featured-3">
    <h2 class=" text-body-emphasis lh-1 ">Steps To Use</h2>
    <div class="row g-4 py-5 row-cols-1 row-cols-lg-3">
      <div class="feature col">
        <div class="feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3">
        <i class="bi bi-file-earmark-pdf-fill"></i>
        </div>
        <h3 class="fs-2 text-body-emphasis"> Upload Your Resume & Project Details</h3>
        <p>Simply upload your resume and project documents in PDF format. This allows the bot to understand your background and provide relevant responses during the interview.</p>
        <a href="/UploadData" class="icon-link">
          Upload File
          <svg class="bi"><use xlink:href="#chevron-right"></use></svg>
        </a>
      </div>
      <div class="feature col">
        <div class="feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3">
        <i class="bi bi-globe2"></i>
        </div>
        <h3 class="fs-2 text-body-emphasis">Real-Time Interview Assistance</h3>
        <p>During the interview, the bot joins the meeting and listens to the conversation. When a question is asked, it processes the query and provides appropriate answers in the comments, ensuring a smoother and more confident interview experience.</p>
        <a href="/Bot" class="icon-link">
          Meet Bot
          <svg class="bi"><use xlink:href="#chevron-right"></use></svg>
        </a>
      </div>
      <div class="feature col">
        <div class="feature-icon d-inline-flex align-items-center justify-content-center text-bg-primary bg-gradient fs-2 mb-3">
        <i class="bi bi-clipboard2-data"></i>
        </div>
        <h3 class="fs-2 text-body-emphasis"> Post-Interview Summary & Feedback</h3>
        <p>After the interview, the bot generates a detailed summary, highlighting key discussions, strengths, and areas for improvement. This helps interviewers assess candidates effectively and allows candidates to refine their approach for future interviews.</p>
        <a href="/Summary" class="icon-link">
          Summary
          <svg class="bi"><use xlink:href="#chevron-right"></use></svg>
        </a>
      </div>
    </div>
  </div>
        </>
    )}
    </>
);

}
