#removing a task
import pymongo
MongoConnection = "mongodb://localhost:27017/"
myclient = pymongo.MongoClient(MongoConnection)
db = myclient["PROJECT2"]
import smtplib
from email.message import EmailMessage
import asyncio
import random
import aiosmtplib
from playwright.async_api import async_playwright
import datetime
import ffmpeg
import subprocess  # To run FFmpeg commands
import time        # For waiting during recording
import signal      # To handle keyboard interrupts (Ctrl+C)
import os          # To handle file paths and create directories
from datetime import datetime
import random
import datetime
from playwright.async_api import async_playwright
import requests
import genai
from datetime import datetime
import asyncio
import pyaudio
import aiofiles
import wave
from pypdf import PdfReader
import smtplib
from email.message import EmailMessage
import json
from langchain_core.output_parsers import JsonOutputParser #pip install langchain 
import google.generativeai as genai



def send_mail(to_email, subject, message, server='smtp.gmail.com',
              from_email='akshaay.kg2021@vitbhopal.ac.in'):
    # import smtplib
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = ', '.join(to_email)
    msg.set_content(message)
    print(msg)
    try:
        # Connect using TLS
        server = smtplib.SMTP(server, 587)
        server.starttls()  # Secure the connection with TLS
        server.set_debuglevel(1)
        server.login(from_email, 'jvuu kwss mneg aklz')  # Use actual password or app password
        server.send_message(msg)
        server.quit()
        print('Successfully sent the mail.')
    
    except smtplib.SMTPException as e:
        print(f"Error sending mail: {e}")
        
                
async def Meetbotprocess(user,username,email,BotEmail,BotPassword,MeetLink,CompanyName,output_filename):
    user = user 
    username = username
    CompanyName = CompanyName
    email = email
    BotEmail = BotEmail
    BotPassword = BotPassword
    MeetLink = MeetLink
    output_filename = output_filename
    print("data got from post methord to bot.py")
    
    result = await main(
                        email=BotEmail,
                        password=BotPassword,
                        meetlink=MeetLink,
                        output_filename=output_filename,
                        CompanyName = CompanyName,
                        User_email = email,
                        username = username
                    )
                
    output_file = result
    print("Process done successfully!")
    print("in bot process")
    
    
    
    video_link = output_file  # need to cahnge this 
    
    current_datetime = datetime.now()
    # Format the date and time for the filename
    formatted_date = current_datetime.strftime("%Y-%m-%d_%H-%M")
    inserted_id = await geminicontentdata(CompanyName, video_path = video_link , MeetLink = MeetLink, formatted_date = formatted_date , username = username , email = email)
    

    print("finally gemini data over  ---------------- ------")
    print(inserted_id)
     

async def main(email,password,meetlink,output_filename,User_email,CompanyName,username):
    print("main started")
    output_file  = await meeting(username = f"{username}",email = f"{email}",password = f"{password}" ,meetlink= f"{meetlink}",CompanyName = f'{CompanyName}' ,output_filename = f'{output_filename}' , User_email = f"{User_email}")
    print('--------------00000-------------')
    print("everything overrrrr ----------------------------------------------------")
    return output_file




async def meeting(email,password ,meetlink, output_filename, User_email, CompanyName, username):
    print("Meeting started")
    output_folder = r"D:\PROJECT2\storage\recordings"
    # Ensure the folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_file = os.path.join(output_folder, f"{output_filename}.flv")
    audio_device = 'Stereo Mix (Realtek(R) Audio)'
    
    print("ffmpeg command started")
    ffmpeg_command = [
        "C:/Users/AKSHAAY KG/Downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe",
        "-y",
        "-video_size", "1920x1080",
        "-framerate", "30",
        "-f", "gdigrab",
        "-i", "desktop",
        "-f", "dshow",
        "-i", f"audio={audio_device}",
        "-probesize", "20000000",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-strict", "experimental",
        output_file
    ]
    print("ffmpeg command over")

    delay = random.randint(100, 300)
    start_time = datetime.now()

    print("playwright starting")
    async with async_playwright() as p:
        print("inside playwright")
        browser = await p.chromium.launch(headless=False,devtools = True, channel='chrome', args=['--disable-blink-features=AutomationControlled'])
        context = await browser.new_context()  # record_video_dir="C:/Users/AKSHAAY KG/Videos/Captures"
        page = await context.new_page()
        await context.grant_permissions(['camera', 'microphone'])
        await page.mouse.move(100, 100)
        
        process = subprocess.Popen(ffmpeg_command) # start recording 
        
        await page.goto('https://workspace.google.com/products/meet/',timeout=60000)
        await page.mouse.move(200, 200)
        await page.wait_for_timeout(5000)
        
        signin = await page.wait_for_selector("//span[contains(text(),'Sign in')]")
        await signin.click()  # sign in button
        await page.wait_for_timeout(2000)
        await page.mouse.move(300, 300)
        email_in = await page.wait_for_selector('//input[@type="email"]')
        await email_in.type(email, delay=delay)  # email box
        await page.wait_for_timeout(2000)
        click_to_pass = await page.wait_for_selector("//span[contains(text(),'Next')]")
        await click_to_pass.click(delay=delay)  # click next to pass
        await page.wait_for_timeout(2000)
        await page.mouse.move(400, 400)
        password_in = await page.wait_for_selector('//input[@type="password"]')
        await password_in.type(password, delay=delay)  # pass box
        await page.wait_for_timeout(2000)
        enter_pass = await page.wait_for_selector("//span[contains(text(),'Next')]")
        await enter_pass.click(delay=delay)  # pass enter
        await page.wait_for_timeout(2000)
        await page.mouse.move(500, 500)
        
        await page.wait_for_timeout(5000)
        meet = await page.wait_for_selector('//input[@id="i6"]')
        await meet.type(meetlink, delay=1000)  # meetid enter
        await page.wait_for_timeout(2000)
        await page.mouse.move(600, 600)
        join = await page.wait_for_selector("//span[contains(text(),'Join')]", timeout=10000)
        await join.click(delay=1000)  # meet join button
        await page.wait_for_timeout(2000)
        await page.mouse.move(500, 500)
        
        div_selector_wrongmeetlink = '[jscontroller="m2Zozf"]'
        div_present = await page.locator(div_selector_wrongmeetlink).count() > 0
        
        if div_present:
            print("You can't join this call. Wrong meet link. check link ")
            process.terminate()  # Stop recording
            process.wait()
            print(f"Recording saved to {output_file}")
            await page.close()
            
            msg = EmailMessage()
            msg['Subject'] = f"Error during Meeting"
            msg['From'] = 'akshaay.kg2021@vitbhopal.ac.in'
            msg['To'] = ', '.join([User_email])
            message = "Wrong Gmeet link . if you could not even copy paste link properly dont use bot leave"
            msg.set_content(message)
            try:
                server='smtp.gmail.com'
                from_email='akshaay.kg2021@vitbhopal.ac.in'
                server = smtplib.SMTP(server, 587)
                print("selected server")
                print("connected server")
                server.ehlo()
                server.starttls()
                server.set_debuglevel(1)
                server.login('akshaay.kg2021@vitbhopal.ac.in', 'jvuu kwss mneg aklz')  # Use actual password or app password
                print("loginnn")
                server.send_message(msg)
                print("msg send")
                server.quit()
                print("quittt")
                print('Successfully sent the mail.')
                
            except aiosmtplib.SMTPException as e:
                print(f"Error sending mail: {e}")
            except Exception as e:
                print(f" Error occured while processing mail {e}")
            
            return
        else:
            pass
        
        await page.wait_for_timeout(6000)
        cam_element = await page.wait_for_selector('//div[@jsname="psRWwc"]')
        cam_value = await cam_element.get_attribute("data-is-muted")
        if cam_value == 'true':
            print('muted')
        else:
            cam_button = await page.wait_for_selector('//div[@jsname="psRWwc"]')
            await cam_button.click(delay=delay)  # on camera
         
            
        mic_element = await page.wait_for_selector('//div[@jsname="hw0c9"]')
        mic_value = await mic_element.get_attribute("data-is-muted")
        if mic_value == 'true':
            print('muted')
        else:
            mic_button = await page.wait_for_selector('//div[@jsname="hw0c9"]')
            await mic_button.click(delay=delay)  # on mike
            
        req_join = await page.wait_for_selector('[jsname="Qx7uuf"]', timeout=10000)
        await req_join.click(delay=delay)  # req to join button
        
        wait_time = random.randint(5, 10)
        print("sleep for 10 seconds")
        time.sleep(10)
        

        try:
            caption_element = await page.wait_for_selector('//button[@jsname="r8qRAd"]', timeout=wait_time * 1000)
            print("Element found, continuing...")
            
        except Exception as e:
            print("caption Element not found")# Proceed with the next block of code if the element is not found
            try:        # Wait for the "Asking to be let in..." message to appear
                print("Waiting for 'Asking to be let in...' message...")
                await page.locator('div.dHFSie:text("Asking to be let in...")').wait_for(timeout=5000)  # 15 seconds timeout
                print("'Asking to be let in...' message is visible. Monitoring...")
                
                while True:
                    asking_to_be_let_in = await page.locator('div.dHFSie:text("Asking to be let in...")').is_visible()  # Check for the "Asking to be let in..." message
                    if asking_to_be_let_in:
                        print("Asking to be let in... Waiting for 5 seconds.")
                        await page.wait_for_timeout(500)  # Wait for 5 seconds and check again
                        continue  # Recheck the state
                    # If "Asking to be let in..." is no longer visible, check the next condition
                    cannot_join = await page.locator('div.dHFSie:text("You can\'t join this call")').is_visible()
                    if cannot_join:
                        print("You can't join this call. Ending the process.")
                        process.terminate()  # Stop recording
                        process.wait()
                        print(f"Recording saved to {output_file}")
                        await page.close()
                        msg = EmailMessage()
                        msg['Subject'] = f"Error during Meeting"
                        msg['From'] = 'akshaay.kg2021@vitbhopal.ac.in'
                        msg['To'] = ', '.join([User_email])
                        message = "You can't join this call. Someone denied your request or no one accepted your request"
                        msg.set_content(message)
                        try:
                            server='smtp.gmail.com'
                            from_email='akshaay.kg2021@vitbhopal.ac.in'
                            server = smtplib.SMTP(server, 587)
                            server.ehlo()
                            server.starttls()
                            server.set_debuglevel(1)
                            server.login('akshaay.kg2021@vitbhopal.ac.in', 'jvuu kwss mneg aklz')  # Use actual password or app password
                            server.send_message(msg)
                            server.quit()
                            print('Successfully sent the mail.')
                
                        except aiosmtplib.SMTPException as e:
                            print(f"Error sending mail: {e}")
                            
                        except Exception as e:
                           print(f" Error occured while processing mail {e}")
                           
                        return  # Exit the loop and function
                    # If neither "Asking to be let in..." nor "You can't join this call" is visible, continue
                    print("Neither 'Asking to be let in...' nor 'You can't join this call' is visible. Proceeding...")
                    break
            except Exception as e:
                print(f"Error while waiting for locators: {e}")  

        
        await oncaptions(page)
        await page.wait_for_timeout(10)    #waiting time
        
        await asyncio.sleep(2)
        message_button = await page.wait_for_selector('//button[@aria-label="Chat with everyone"]')
        message_val = await message_button.get_attribute("aria-pressed")
        if message_val == 'true':
            print('on messages')
        else:
            await message_button.click()
        
        await asyncio.sleep(1)
        messenger = await page.wait_for_selector('//textarea[@jsname="YPqjbf"]')
        await messenger.type("hello i am bot , i am heare to help you")
        await page.wait_for_timeout(2000)
        await asyncio.sleep(1)
        msg_send = await page.wait_for_selector('//button[@jsname="SoqoBf"]')
        await msg_send.click(delay=delay)
        await page.wait_for_timeout(2000)
        await asyncio.sleep(3)
        
        fetch_task_answers = asyncio.create_task(fetch_answers(page,username))
        await asyncio.sleep(11)
        monitor_time_task = asyncio.create_task(monitor_meeting_time(page, start_time))
        await asyncio.sleep(7)
        monitor_task = asyncio.create_task(monitor_page(page, monitor_time_task,fetch_task_answers))
        await asyncio.sleep(2)
        
        
        try:
            while True:
                await asyncio.sleep(20)
                message_end = await page.query_selector('[jsname="r4nke"]')
                
                if message_end:
                    message_text_end = await message_end.text_content()
                    if message_text_end != "Ready to join?":
                        print("Meeting disconnected or ended.")
                        break  # Exit the loop to reach `finally`
                    else:
                        print("Ready to join message detected, continuing.")
        except Exception as e:
            print(f"Error in meeting simulation: {e}")
            
        finally:
            process.terminate() # stop
            process.wait()
            print(f"Recording saved to {output_file}")
            for task in [monitor_task, monitor_time_task, fetch_task_answers]:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            print("Tasks cancelled. Meeting ended.")
            await page.close()
            return output_file


async def oncaptions(page):
    caption_element = await page.wait_for_selector('//button[@jsname="r8qRAd"]',timeout=120000)
    caption_value = await caption_element.get_attribute("aria-pressed")
    if caption_value == 'true':
        print('cap on')
    else:
        await caption_element.click()


async def fetch_answers(page, username):
    while True:  # Infinite loop to keep executing
        async def record_and_send(username,page):
            SAVE_PATH = r"D:\PROJECT2\storage\chunks"
            if not os.path.exists(SAVE_PATH):
                os.makedirs(SAVE_PATH)
            
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            
            output_file = os.path.join(SAVE_PATH, f"{username}{timestamp}.flv")
            audio_device = 'Stereo Mix (Realtek(R) Audio)'
            
            ffmpeg_command = [
                "C:/Users/AKSHAAY KG/Downloads/ffmpeg-master-latest-win64-gpl/ffmpeg-master-latest-win64-gpl/bin/ffmpeg.exe",
                "-y",
                "-video_size", "1920x1080",
                "-framerate", "30",
                "-f", "gdigrab",
                "-i", "desktop",
                "-f", "dshow",
                "-i", f"audio={audio_device}",
                "-probesize", "10000000",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-strict", "experimental",
                "-t", "15", #for 15 sec
                output_file
            ]
            
            process = subprocess.Popen(ffmpeg_command)
            process.wait()

            response_llm = await send_to_llm(output_file, username)

            if response_llm:
                try:
                    response_json = response_llm.text  
                    if "response" in response_json:
                    # llm_response = response_json["response"]
                        print(response_json)
                        message_button = await page.wait_for_selector('//button[@aria-label="Chat with everyone"]')
                        message_val = await message_button.get_attribute("aria-pressed")

                        if message_val == "false":
                            await message_button.click()

                                
                        messenger = await page.wait_for_selector('//textarea[@jsname="YPqjbf"]')
                        # await page.wait_for_selector('[id="bfTqV"]').click()
                        print("type should happen ====================================>")
                        await messenger.fill(str(response_json))  # Ensure it's a string
                        await asyncio.sleep(0.75)
                        msg_send = await page.wait_for_selector('//button[@jsname="SoqoBf"]')
                        await msg_send.click()
                        message_button = await page.wait_for_selector('//button[@aria-label="Close"]').click()
                        await page.wait_for_timeout(100)
                            
                    elif "question_detected" in response_json and "answer" in response_json:
                        # question = response_json["question_detected"]  # No need for str() here
                        # answer = response_json["answer"]        # No need for str() here

                        # print(f"Question: {question}")
                        # print(f"Answer: {answer}")
                                
                        message_button = await page.wait_for_selector('//button[@aria-label="Chat with everyone"]')
                        message_val = await message_button.get_attribute("aria-pressed")

                        if message_val == "false":
                            await message_button.click()
                        await asyncio.sleep(0.75)
                        messenger = await page.wait_for_selector('//textarea[@jsname="YPqjbf"]')
                        # await page.wait_for_selector('[id="bfTqV"]').click()
                        print("type should happen ====================================>")
                        await messenger.fill(response_json)  # Use concatenation

                        msg_send = await page.wait_for_selector('//button[@jsname="SoqoBf"]')
                        await msg_send.click()
                        close_button = await page.wait_for_selector('//button[@aria-label="Close"]').click()
                        await page.wait_for_timeout(100)
                            
                    else:
                        print("No valid response structure received from LLM.")
                                
                except json.JSONDecodeError as e:  # Include the exception in the message
                    print(f"Invalid JSON response from LLM: {e}.  Response text was: {response_llm.text if response_llm else 'None'}") # Include the response text for debugging
                except Exception as e:
                    print(f"An unexpected error occurred: {e}") # Catch other potential errors
            else:
                print("No response received from LLM.")

        async def send_to_llm(output_file, username):
            contentformdoc = ""
            directory = r"D:\PROJECT2\storage"

            # Construct file paths
            copy_file = os.path.join(directory, f"{username}_copy.pdf")
            original_file = os.path.join(directory, f"{username}.pdf")
            
            reader = None 

            if os.path.exists(copy_file):
                reader = PdfReader(copy_file)
            elif os.path.exists(original_file):
                reader = PdfReader(original_file)
            
            for page in reader.pages:
                contentformdoc += page.extract_text() + "\n"
            
            PdfData = contentformdoc.strip()
            # print(PdfData)
            
            print(f"Sending {output_file} to Whisper... ==============================> chunk sent")
            os.environ['OPENAI_API_KEY'] = ("AIzaSyBZb-E0LNgp3X3nJ1mi77A_m5ib1B1AMoo")
            genai.configure(api_key=os.environ['OPENAI_API_KEY'])
            model = genai.GenerativeModel("gemini-1.5-flash")
            print(f"Uploading file... to gemini ===========================> chunk ")
            video_file = genai.upload_file(path=output_file, mime_type='video/x-flv')
            print(f"Completed upload: {video_file.uri}")
            print(f"uploading gemi")

            # Check whether the file is ready to be used.
            while video_file.state.name == "PROCESSING":
                print('... processing file', end='')
                time.sleep(5)
                video_file = genai.get_file(video_file.name)
            if video_file.state.name == "FAILED":
                raise ValueError(video_file.state.name)

            def build_prompt(PdfData, username):
                PdfData = PdfData
                username = username
                prompt_data = {
        "role": "You are an advanced AI assistant designed to help a candidate excel in an HR and technical interview. You meticulously process video data second-by-second, accurately identify the speaker (HR or candidate) using captions and the provided username, analyze the speech, and provide precise, professional responses only when necessary. Your goal is to ensure the candidate appears knowledgeable, confident, and well-prepared. You must avoid irrelevant or incorrect responses at all costs, as any mistake could jeopardize the candidate's success.",

        "inputs": {
            "reference_document_content": f"{PdfData} if {PdfData} else No relevant document found.",
            "video_transcript": "",
            "username": f"{username} (used to identify the candidate in video captions)"
        },

        "processing_logic": {
            "step_1": {
                "description": "Process Video Data and Identify Speakers",
                "actions": [
                    "Analyze the video captions and transcript per second to detect speaker changes with 100% accuracy.",
                    "Identify the candidate using the provided username in the captions. If the username is speaking, it is the candidate answering.",
                    "If the speaker is not the candidate, assume it is the HR interviewer asking questions.",
                    "Label each segment accurately before further processing. Ensure no misidentification occurs."
                ]
            },
            "step_2": {
                "description": "Determine the Type of Video Segment",
                "rules": [
                    {"condition": "Segment is spoken by HR and contains a question", "action": "Proceed to Step 3 to generate a detailed, professional response for the candidate."},
                    {"condition": "Segment is spoken by HR and is a greeting or small talk", "examples": ["How are you?", "Where are you from?", "Nice to meet you."], "action": "Generate a general, professional response based on the candidate's document content or standard interview etiquette."},
                    {"condition": "Segment is silent or contains noise only", "action": "response: silent"},
                    {"condition": "Segment is spoken by the candidate and contains an answer", "action": "response: candidate answering (no action needed)"}
                ]
            },
            "step_3": {
                "description": "Understanding the HR Question",
                "actions": [
                    "Extract the exact question spoken by HR, ensuring clarity and precision. Listen carefully and re-analyze if necessary.",
                    "Analyze the intent behind the question to avoid misinterpretation. Cross-check with the context of the interview.",
                    "Classify the question into one of the following categories:"
                ],
                "question_types": [
                    "Technical Questions (e.g., 'Explain machine learning.')",
                    "Conceptual Questions (e.g., 'What is the difference between SQL and NoSQL?')",
                    "Experience-Based Questions (e.g., 'Tell me about your last project.')",
                    "Project-Related Questions (e.g., 'What challenges did you face in your last project?')",
                    "Behavioral Questions (e.g., 'How do you handle conflicts in a team?')",
                    "Personal Details (e.g., 'Tell me about yourself.', 'What are your strengths?')"
                ]
            },
            "step_4": {
                "description": "Generating a Professional Response",
                "rules": [
                    {"action": "Check the resume content for relevant information. Prioritize extracting data from the document."},
                    {"condition": "No relevant data found in the document", "action": "Generate an accurate, detailed, and professional answer based on your knowledge, ensuring it aligns with the candidate's profile."},
                    {"action": "Provide thorough and clear explanations. Do not limit the response length; ensure the answer is comprehensive and professional."},
                    {"condition": "Unsure or lack sufficient information", "action": "response: I am not sure about the answer to this question."},
                    {"condition": "No response is needed (small talk, candidate's answer, silent video)", "action": "response: no response needed candidate can answer"},
                    {"condition": "Question is about personal details (e.g., 'Tell me about yourself.')", "action": "Extract relevant personal details from the document and craft a professional, detailed response."}
                ]
            }
        },

        "response_format": {
            "question_requires_answer": "question_detected: Extracted Question, answer: Generated Professional Response",
            "no_response_needed": "response: none"
        },

        "example_scenarios": [
            {
                "hr_question": "Can you explain your experience with Python?",
                "resume_has_data": {
                    "question_detected": "Can you explain your experience with Python?",
                    "answer": "I have 3 years of experience with Python, mainly in web development and data analysis. I have used frameworks like Django and Flask to build scalable web applications. Additionally, I have applied Python for automation tasks, such as scripting and data processing, and for machine learning projects, where I used libraries like Pandas, NumPy, and Scikit-learn."
                },
                "no_resume_data": {
                    "question_detected": "Can you explain your experience with Python?",
                    "answer": "Python is a versatile programming language used for web development, data science, and automation. I have experience building applications using Django and Flask frameworks, handling data processing with Pandas, and implementing machine learning models with Scikit-learn. I have also used Python for scripting and automation to streamline workflows."
                }
            },
            {
                "hr_question": "What is the difference between SQL and NoSQL?",
                "technical_answer": {
                    "question_detected": "What is the difference between SQL and NoSQL?",
                    "answer": "SQL databases are relational and use structured tables, making them ideal for complex queries and transactions. They are highly consistent and support ACID properties. Examples include MySQL and PostgreSQL. NoSQL databases, on the other hand, are non-relational and handle unstructured or semi-structured data. They are highly scalable and flexible, making them suitable for large-scale applications. Examples include MongoDB and Cassandra."
                }
            },
            {
                "hr_question": "Tell me about yourself.",
                "personal_details_answer": {
                    "question_detected": "Tell me about yourself.",
                    "answer": "I am a software engineer with 4 years of experience specializing in backend development and cloud computing. I hold a Bachelor's degree in Computer Science and have worked on projects involving microservices architecture, REST APIs, and DevOps practices. I am proficient in Python, Java, and cloud platforms like AWS. I am passionate about solving complex problems and continuously improving my skills to deliver high-quality solutions."
                }
            },
            {
                "hr_question": "How are you?",
                "general_response": {
                    "question_detected": "How are you?",
                    "answer": "I'm doing well, thank you. I'm excited about this opportunity and looking forward to discussing how my skills and experiences align with the role."
                }
            }
        ],

        "strict_rules": {
            "do_answer": [
                "Technical, conceptual, experience-based, and project-related questions.",
                "Questions directly related to resume content.",
                "Questions requiring professional, detailed responses.",
                "Personal details questions (extract from document and craft a professional response).",
                "General greetings or small talk (generate a professional, polite response)."
            ],
            "do_not_answer": [
                {"condition": "Transcript is silent", "action": "response: silent"},
                {"condition": "Chunk contains candidate's response", "action": "response: answer from candidate"},
                {"condition": "Unsure about the answer", "action": "response: I am not sure about the answer to this question."}
            ]
        },

        "key_objectives": [
            "Ensure the candidate appears knowledgeable, confident, and well-prepared.",
            "Use resume content first; if unavailable, generate a relevant, detailed answer that aligns with the candidate's profile.",
            "Provide thorough, clear, and professional responses. Do not limit the length of answers; ensure they are comprehensive.",
            "Avoid unnecessary or incorrect responses at all costs. Mistakes are unacceptable.",
            "Process video per second, ensuring no details are missed. Re-analyze if necessary.",
            "Identify and label speakers accurately using captions and the provided username. Misidentification is not allowed.",
            "Prioritize clarity in responses to align with interview expectations.",
            "For personal details, extract from the document and craft a professional, detailed response.",
            "For general greetings or small talk, generate a polite, professional response.",
            "Ensure the candidate passes the interview by providing flawless support."
        ]
    }

                prompt = json.dumps(prompt_data, indent=4)
                return prompt

            prompt = build_prompt(PdfData, username)
            print("Generated Prompt:")
            # print(prompt)
            print("above model comment")
            model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
            print("Making LLM inference request... ==============================> chunk ")
            try:
                print("comming heare ============== working")
                responsefromllm = model.generate_content(contents=[prompt, video_file], request_options={"timeout": 600})
                print("response got ==============================> chunk ")
                print(responsefromllm.text)
                genai.delete_file(video_file.name)
                print(f'Deleted file {video_file.uri}')
                return responsefromllm
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:  # Example: Rate limit exceeded
                    print("Gemini quota exceeded!")
                return None
            except Exception as e:
                print(f"An unexpected error occurred in send_to_llm: {e}")
                return None

        await record_and_send(username,page)


async def monitor_meeting_time(page, start_time):
    while True:
        elapsed_time = (datetime.now() - start_time).total_seconds() / 60  # Calculate elapsed time in minutes
        
        if elapsed_time > 3:#now set as 3
            print("Meeting has been running for over 30 minutes.")
            
            try:
                # Fetch the participant count
                participant_element = await page.query_selector('//div[@class="uGOf1d"]')
                if participant_element:
                    participant_count = int(await participant_element.text_content())
                    print(f"Current participant count: {participant_count}")
                    
                    if participant_count == 1:
                        print("Only one participant left. Leaving the meeting.")
                        end_button = await page.query_selector('//button[@jsname="CQylAd"]')
                        await end_button.click() # Call a function to leave the meeting
                        return
                    else:
                        print(f"{participant_count} participants present. Waiting for 5 more minutes.")
                        await asyncio.sleep(60)  # Wait for 5 minutes
                else:
                    print("Unable to fetch participant count. Retrying.")
            except Exception as e:
                print(f"Error fetching participant count: {e}")
        else:
            print(f"Elapsed time: {elapsed_time:.2f} minutes. Continuing to monitor.")
            await asyncio.sleep(60)  # Check every minute

async def monitor_page(page, monitor_time_task,fetch_task_answers ):
    try:
        while True:
            # Check for the message element to detect meeting status
            message_element = await page.query_selector('[jsname="r4nke"]')
            if message_element:
                message_text = await message_element.text_content()

                # If the message is anything other than "Ready to join?"
                if message_text != "Ready to join?":
                    print("Meeting disconnected or status changed, stopping fetch task participents.")
                    # Stop the fetch task
                    monitor_time_task.cancel()
                    fetch_task_answers.cancel()
                    return  # Exit monitoring task
                else:
                    print("Ready to join message detected, continuing.")
            
            await asyncio.sleep(30)  # Check every 45 seconds
    except Exception as e:
        print(f"Error in monitoring page: {e}")
        monitor_time_task.cancel()
        fetch_task_answers.cancel()
        



async def geminicontentdata(CompanyName, video_path , MeetLink , formatted_date ,username , email):
    print("inside gemini")
    os.environ['OPENAI_API_KEY'] = ("AIzaSyBZb-E0LNgp3X3nJ1mi77A_m5ib1B1AMoo")
    genai.configure(api_key=os.environ['OPENAI_API_KEY'])
    model = genai.GenerativeModel("gemini-1.5-flash")
    print(f"Uploading file... to gemini")
    video_file = genai.upload_file(path=video_path,mime_type='video/x-flv')
    print(f"Completed upload: {video_file.uri}")
    # Check whether the file is ready to be used.
    while video_file.state.name == "PROCESSING":
        print('... processing file', end='')
        time.sleep(10)
        video_file = genai.get_file(video_file.name)
    if video_file.state.name == "FAILED":
        raise ValueError(video_file.state.name)
    
    # Create the prompt.
    
    prompt = """
            You are an AI-powered interview analysis assistant. Your task is to process a recorded interview meeting {video_path} between an HR representative and a candidate. Your analysis must be based solely on the spoken words in the audio and captions, excluding visuals, chat messages, or any non-verbal elements. Ensure the report is structured, non-repetitive, and returned as a single valid JSON object.


            🟢 Interview Details
                Extract key details from the interview using audio and captions.

                Candidate Name (if mentioned)
                Total Duration (XX minutes XX seconds)
                Start & End Time (HH:MM format)
                Overall Tone (Formal / Semi-formal / Casual)
                Interview Type (Technical / HR / Behavioral / Mixed)
                {
                    "status": "Completed",
                    "interview_details": {
                        "candidate": "Name (if available)",
                        "total_duration": "XX minutes XX seconds",
                        "start_time": "HH:MM",
                        "end_time": "HH:MM",
                        "overall_tone": "Formal / Semi-formal / Casual",
                        "interview_type": "Technical / HR / Behavioral / Mixed"
                    }
                }

            If no valid conversation occurred, return:
            { "status": "Meeting did not take place." }

            🟡 Candidate Response Analysis
            Analyze only the candidate's responses for each question based on the audio and captions.
            
                For each question:

                Question Number
                Question Text
                Topic
                Difficulty Level
                Candidate's Response
                Answer Accuracy (Correct / Partially Correct / Incorrect)
                Ideal Answer (What a perfect response should be)
                Improvement Suggestions
                Response Score (0-10)
                Related Concepts to Study

                {
                    "questions": [
                        {
                            "question_number": 1,
                            "question_text": "What is polymorphism in OOP?",
                            "topic": "Object-Oriented Programming",
                            "difficulty_level": "Intermediate",
                            "candidate_response": "Polymorphism allows methods to take different forms.",
                            "answer_accuracy": "Partially Correct",
                            "ideal_answer": "Polymorphism allows a function to have multiple implementations depending on the object’s type. It includes method overloading and method overriding.",
                            "improvement_suggestions": "Explain method overloading and overriding with examples.",
                            "response_score": 6,
                            "related_concepts_to_study": ["Method Overloading", "Method Overriding", "Dynamic vs. Static Binding"]
                        }
                    ]
                }


            🔴 Candidate's Performance Breakdown
            Evaluate technical knowledge, communication skills, and coding ability based on the audio and captions.
                Technical Knowledge
                Strengths
                Weaknesses
                Suggestions for Improvement
                Communication Skills
                Clarity (Good / Moderate / Needs Improvement)
                Confidence (Good / Moderate / Needs Improvement)
                Filler Words Detected
                Suggestions for Better Communication
                Coding Skills (if applicable)
                Number of Coding Questions Attempted
                Accuracy (%)
                Mistakes Identified
                Corrections
                Suggested Improvements
                {
                    "performance_analysis": {
                        "technical_knowledge": {
                            "strengths": ["Good understanding of OOP basics", "Strong in database concepts"],
                            "weaknesses": ["Lacks clarity in explaining projects", "Needs more depth in algorithms"],
                            "suggestions": ["Revise key CS topics", "Practice explaining past work in structured ways"]
                        },
                        "communication_skills": {
                            "clarity": "Moderate",
                            "confidence": "Needs Improvement",
                            "filler_words_detected": ["Uh", "Umm", "Like"],
                            "suggestions": ["Reduce filler words", "Use structured answers like the STAR method"]
                        },
                        "coding_skills": {
                            "coding_questions_attempted": 2,
                            "accuracy": "50%",
                            "mistakes": ["Did not optimize the solution", "Syntax errors in code"],
                            "corrections": ["Use better time complexity algorithms", "Revise syntax rules"],
                            "suggestions": ["Practice more LeetCode problems", "Focus on optimization techniques"]
                        }
                    }
                }


            🟠 Final Evaluation
            Generate an overall score and assessment based on the audio and captions.
            Overall Score (0-100)
            Technical Score (0-100)
            Communication Score (0-100)
            Confidence Level (High / Moderate / Low)
            Success Probability (%)
            Summary of Strengths & Areas for Improvement

            {
                "final_evaluation": {
                    "overall_score": 65,
                    "technical_score": 70,
                    "communication_score": 60,
                    "confidence_level": "Moderate",
                    "success_probability": "55%",
                    "summary": "The candidate has a strong foundation but needs to improve clarity and confidence. More practice in project explanations and algorithm-based problem-solving is required."
                }
            }


            🔵 Personalized Improvement Plan
            Suggest areas of focus based on weaknesses identified in the audio and captions.

            Focus Areas (Key skills to improve)
            Recommended Study Materials (Topic & Resource)
            Mock Interview Suggestions

            {
                "improvement_plan_details": {
                    "focus_areas": ["Project Explanation", "Algorithm Optimization", "Communication Confidence"],
                    "recommended_study_materials": [
                        {"topic": "Dynamic Programming", "resource": "NeetCode YouTube Series"},
                        {"topic": "OOP Concepts", "resource": "GeeksforGeeks OOP Guide"},
                        {"topic": "Speaking Confidence", "resource": "Public Speaking Course on Udemy"}
                    ],
                    "mock_interview_suggestion": "Practice with a friend or use an AI mock interview tool."
                }
            }


            🔹 Motivational Closing Statement
            Encourage the candidate with personalized motivation based on the audio and captions.

                {
                    "motivation": "You have a strong foundation, but improving project explanations and technical clarity will help you stand out. Keep practicing, and don't hesitate to refine your answers before your next interview!"
                }

            🔸 Final JSON Output
            The final JSON should be structured, non-repetitive, and complete.
            no keys should be same.
            Return the final output strictly as a valid JSON object with no extra text, explanations, or formatting.

            If the interview took place, return:

                {
                "status": "Completed",
                "interview_details": { ... },
                "questions": [ ... ],
                "performance_analysis": { ... },
                "final_evaluation": { ... },
                "improvement_plan_details": { ... },
                "motivation": { ... }
            }

            Otherwise, return:

            { "status": "Meeting did not take place." }
            """
    # Choose a Gemini model.
    model = genai.GenerativeModel(model_name="gemini-2.0-flash-exp")
    # Make the LLM request.
    print("Making LLM inference request...")
    import json
    LLM_response = model.generate_content(contents=[prompt, video_file], request_options={"timeout": 600})
    print(LLM_response.text)
    genai.delete_file(video_file.name)
    print(f'Deleted file {video_file.uri}')

    MeetLink = MeetLink
    Formatted_date = formatted_date
    Name = username
    Email = email
    CompanyName = CompanyName

    print("Updating for MongoDB")
    output_parser = JsonOutputParser()
    try:
        print("Inside try")
        
        # Ensure LLM response is parsed as JSON
        parsed_response = output_parser.parse(LLM_response.text)
        
        parsed_response.update({
            "MeetLink": MeetLink,
            "Formatted_date": Formatted_date,
            "CandidateName": Name,
            "Email": Email,
            "CompanyName": CompanyName
        })
        
        print("Parsed JSON Response: ======================> ", parsed_response)

    except json.JSONDecodeError:
        print("Error: LLM response is not a valid JSON string.")
        parsed_response = {"error": "Invalid JSON format from LLM"}

    print("Start MongoDB operation")
    try:
        print("Inserting into MongoDB")
        collection = db['meetingdatacollection']
        res = collection.insert_one(parsed_response) 
        inserted_id = res.inserted_id
    except Exception as e:
        print("An error occurred while inserting meeting data:", e)
        
    # print("from function")
    # send_mail([Email],f"Meeting Report {Formatted_date}", f"""
    #     Hello {Name},  

    #     👋 Hope you're doing well!  

    #     Here is your **Interview Summary**:  

    #     📅 **Date:** {Formatted_date}  
    #     🔗 **Meet Link:** [Click Here]({MeetLink})  
    #     🏢 **Company Name:** {CompanyName}  

    #     📌 **AI-Generated Interview Summary:**  
    #     {parsed_response}  

    #     Thank you for choosing our bot!  

    #     Best regards,  
    #     Your Interview Assistant 🤖 
    # """)

    print("Sending email")
    message = f"""
        Hello {Name},  

        👋 Hope you're doing well!  

        Here is your **Interview Summary**:  

        📅 **Date:** {Formatted_date}  
        🔗 **Meet Link:** [Click Here]({MeetLink})  
        🏢 **Company Name:** {CompanyName}  

        📌 **AI-Generated Interview Summary:**  
        {parsed_response}  

        Thank you for choosing our bot!  

        Best regards,  
        Your Interview Assistant 🤖 
    """
    print(message)
    print("Trying to send email")
    msg = EmailMessage()
    msg['Subject'] = f"Meeting Report {Formatted_date}"
    msg['From'] = 'akshaay.kg2021@vitbhopal.ac.in'
    msg['To'] = ', '.join([Email])
        
    msg.set_content(message)
    
    try:
        print("working mail failed")
        smtp_server='smtp.gmail.com'
        smtp_port = 587
        from_email='akshaay.kg2021@vitbhopal.ac.in'
        # Connect using TLS
        server = smtplib.SMTP(smtp_server, smtp_port)
        print("selected server")
        print("connected server")
        server.ehlo()
        server.starttls()  # Secure the connection with TLS
        # print("secured  ")
        server.set_debuglevel(1)
        server.login('akshaay.kg2021@vitbhopal.ac.in', 'jvuu kwss mneg aklz')  # Use actual password or app password
        print("loginnn")
        server.send_message(msg)
        print("msg send")
        server.quit()
        print("quittt")
        print('Successfully sent the mail.')
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {e}")

    except Exception as e:
        print(f"Error occurred while processing mail: {e}")

    return inserted_id


