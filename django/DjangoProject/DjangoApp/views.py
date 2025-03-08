import pymongo
MongoConnection = "mongodb://localhost:27017/"
myclient = pymongo.MongoClient(MongoConnection)
db = myclient["PROJECT2"]

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth import login,  authenticate
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
import random
import re
from .bot import send_mail
import asyncio
from playwright.async_api import async_playwright
import ffmpeg
import subprocess  # To run FFmpeg commands
import time        # For waiting during recording
import signal      # To handle keyboard interrupts (Ctrl+C)
import os          # To handle file paths and create directories
from datetime import datetime
import threading
from .bot import Meetbotprocess
# Create your views here.

class home(APIView):
    permission_classes = (AllowAny,)
    
    def get(self,request):
        if not request.user.is_authenticated:
            return JsonResponse({"Message": "try to register","Authenticated":False})
        user = request.user
        username = user.username
        return JsonResponse({"Message": f"Already Logged in {username}", "Authenticated":True})

class GenerateOtp(APIView):
    
    @csrf_exempt
    def post(self,request):
        try:
            Name = request.data.get('Name')
            Email = request.data.get('Email')
        
            if not Name or not Email:
                return JsonResponse({'Message': 'All fields are required'})
        
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if Email and re.match(email_regex, Email):
                pass
            else:
                return JsonResponse({'Message': "this Email account is invalid"})
            
            try:
                validate_email(Email)
            except ValidationError:
                return JsonResponse({'Message': 'Invalid email format'})
        
            if User.objects.filter(username=Name).exists():
                return JsonResponse({'Message': 'Username already exists'})
        
            if User.objects.filter(email=Email).exists():
                return JsonResponse({'Message': 'Email already registered'})
        
            random_number = random.randint(10000, 99999)
            otp = {'otp':random_number, 'Email':Email}
        
            collection = db["Otp Verification"]
            collection.update_one({"Email": Email},{"$set": {"Otp": random_number}},upsert=True)
        
            send_mail([Email],"Registeration", f"your otp is {random_number} dont share with others")
            return JsonResponse({'Message': f"Otp generated check your mail {Email}"})
        except json.JSONDecodeError:
            return JsonResponse({'Message':'Invalid JSON format'})
        except Exception as e:
            return JsonResponse({'Message': f"An error occurred: {str(e)}"}, status=500)

class CheckAuth(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        if request.user.is_authenticated:
            return Response({"Message": "Already Logged in", "Authenticated": True})
        return Response({"Message": "Please Login", "Authenticated": False})
       
class Register(APIView):
    permission_classes = (AllowAny,)
    
    @csrf_exempt
    def post(self, request):
        Name = request.data.get('Name')
        Email = request.data.get('Email')
        Password = request.data.get('Password')
        MobileNumber = request.data.get('MobileNumber')
        Otp = request.data.get('Otp')
        
        if not Name or not Email or not Password or not MobileNumber or not Otp:
            return JsonResponse({'Message': 'All fields are required'})
        
        try:
            validate_email(Email)
        except ValidationError:
            return JsonResponse({'Message': 'Invalid email format'})
        
        if User.objects.filter(username=Name).exists():
            return JsonResponse({'Message': 'Username already exists'})
        
        if User.objects.filter(email=Email).exists():
            return JsonResponse({'Message': 'Email already registered'})
        
        if len(Password) < 8:
            return JsonResponse({'Message': "Password should be at least 8 characters long"})
        
        collection = db["Otp Verification"]
        record = collection.find_one({"Email": Email })
        if record:
            OtpGenerated = record.get("Otp")
        else:
            return JsonResponse({'Message':"Generate Otp first"})
        if int(OtpGenerated) != int(Otp):
            return JsonResponse({'Message': "Invalid OTP"})
        
        try:
            user = User.objects.create_user(username=Name, email=Email, password=Password)
            user.save()
                
            Dict = {'Name':Name,'Email':Email,'MobileNumber':MobileNumber, 'Password':Password }
            collection = db["UserData"]
            collection.insert_one(Dict)
            send_mail([Email],"Account Created successfully",
                  f"""your account created Sucessfully
                      Company name 
                      Heare are your Credentials
                        User Name : {Name}
                        Email : {Email}
                        Number : {MobileNumber}
                        Password : {Password}
                      thanks for choosing our product , keep Credentials safe""")
            return JsonResponse({'Message': 'Done'}, status=201)
        except Exception as e:
            return JsonResponse({'Message': f"User registration failed: {str(e)}"}, status=500)


class Login(APIView):
    permission_classes = (AllowAny,)
    
    def post(self, request):
        try:
            Name = request.data.get('Name')
            Password = request.data.get('Password')
        
            user = authenticate(username = Name, password = Password)
        
            if user is None:
                return JsonResponse({'Message': "Invalid credentials"})

            else:
                login(request,user)
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'Message':'Done'})
        except Exception as e:
                return JsonResponse({'Message': f'Error in Login {str(e)}'}, status=500)

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")

            if not refresh_token:
                return Response({"error": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)

            # Decode and validate refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token

            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({"error": f"Logout failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)


class UploadData(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.is_authenticated:
            return Response({"Message": "Already Logged in", "Authenticated": True})
        return Response({"Message": "Please Login", "Authenticated": False})
    
    def post(self,request):
        if 'file' not in request.FILES:
            return JsonResponse({'Message': 'No file uploaded'})
        
        Doc = request.FILES['file']
        user = request.user 
        Name = user.username
        
        uploaded_file = Doc
        File_content = uploaded_file.read()
        
        upload_folder = r"D:\PROJECT2\storage"
        os.makedirs(upload_folder, exist_ok=True)  # Ensure folder exists
        
        _, ext = os.path.splitext(uploaded_file.name)  # Extract original extension
        file_name = f"{Name}{ext}"
        file_path = os.path.join(upload_folder, file_name)
        
        if os.path.exists(file_path):
            base, ext = os.path.splitext(file_name)
            new_name = f"{base}_copy{ext}"
            file_path = os.path.join(upload_folder, new_name)
            
        try:
            with open(file_path, 'wb') as destination:
                destination.write(File_content)
        except Exception as e:
            return JsonResponse({'Message': f'Error saving file: {str(e)}'}, status=500)
        
        return JsonResponse({'Message': 'File uploaded successfully'})
    

loop = asyncio.new_event_loop()    # run async function process     pass this with func to run in async

def start_loop():
    """
    Starts an asyncio event loop in a separate thread.
    """
    asyncio.set_event_loop(loop)
    loop.run_forever()

# Start the loop in a separate thread
threading.Thread(target=start_loop, daemon=True).start()


class Bot(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.is_authenticated:
            return Response({"Message": "Already Logged in", "Authenticated": True})
        return Response({"Message": "Please Login", "Authenticated": False}) 
    
    
    
    def post(self, request):
        try:
            user = request.user
            Name = user.username
            username = user.username
            email = user.email
            MeetLink = request.data.get('MeetLink')
            CompanyName = request.data.get('CompanyName')
            
            BotEmail = "akshaaykg1@gmail.com"
            BotPassword = "PASSWORD 10"
            
            current_datetime = datetime.now()
            formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M")
            output_filename = f"{Name}{CompanyName}{formatted_datetime}"
            
            print("Starting the bot")
        
            asyncio.run_coroutine_threadsafe(Meetbotprocess(user,username,email,BotEmail,BotPassword,MeetLink,CompanyName,output_filename),loop) 
            return JsonResponse({"Message": "Bot Started"},status=200)

        except Exception as e:
                return JsonResponse({'Message': f'{str(e)}'}, status=500)
            

class Summary(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            Name = user.username
            email = user.email
            
            collection = db['meetingdatacollection']
            pipeline = [{"$match": {"CandidateName": f"{Name}", "Email": f"{email}"}},
                        { "$sort": { "Formatted_date": -1 } },  # Sort by "amount" in descending order
                        {"$project" : { "_id": 0}}]
            
            data = list(collection.aggregate(pipeline))
            
            
            return Response({"Message": "Already Logged in", "Authenticated": True, "data":data})
        return Response({"Message": "Please Login", "Authenticated": False}) 