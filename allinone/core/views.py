import os
import requests
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
import markdown
from django.utils.safestring import mark_safe
from datetime import datetime
import os
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt  # For handling POST requests

import asyncio
import aiohttp

from .models import *

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
API_KEY = os.getenv("GEMINI_API_KEY")  # Ensure this is set in your .env file or settings

def signupman(request):
    return render(request, "signupman.html")

def historyview(request):
    return render(request, "history.html")

def homearoma(request):
    return render(request, "homeman.html")

def optionsman(request):
    return render(request, "optionsman.html")

def logout(request):
    logout(request)
    return render(request, "homeman.html")

def histories(request):
    username = request.user.username if request.user.is_authenticated else "Guest"
    data=history.objects.filter(name=username)

    return render(request,'history.html',{'data':data})

@csrf_exempt  # Use this only if CSRF token is not required
async def fetch_response(session, text):
    headers = {"Content-Type": "application/json"}
    params = {"key": API_KEY}
    payload = {"contents": [{"parts": [{"text": text}]}]}

    try:
        async with session.post(GEMINI_API_URL, headers=headers, json=payload, params=params) as response:
            data = await response.json()
            return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
    except Exception:
        return None

async def process_requests(user_input):
    user_input1 = user_input + " Ingredients (with precise measurements) along with Nutritional values, only this no other extra information strictly these as per instruction"
    user_input2 = user_input + " step by step procedure, only this no other extra information strictly these as per instruction include heading"
    user_input3 = user_input + " alternate ingredients for this recipe rather than regular one for health benefits, only this no other extra information strictly these as per instruction include heading while describing also mention how to use it in making brief steps"

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_response(session, text) for text in [user_input1, user_input2, user_input3]]
        responses = await asyncio.gather(*tasks)

    return [markdown.markdown(text) if text else None for text in responses]

def home(request):
    response_text = response_text1 = response_text2 = None  
    username = request.user.username if request.user.is_authenticated else "Guest"
    print("User:", request.user)  # Debugging user authentication
    print("Is Authenticated:", request.user.is_authenticated)

    if request.method == "POST":
        user_input = request.POST.get("input_text", "").strip()
        current_date = datetime.now().date() 
        current_time = datetime.now().strftime("%H:%M:%S")

        history.objects.create(name=username, search=user_input, date=current_date, time=current_time)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        responses = loop.run_until_complete(process_requests(user_input))

        response_text, response_text1, response_text2 = responses

    return render(request, "index.html", {
        "response": mark_safe(response_text) if response_text else None,
        "response1": mark_safe(response_text1) if response_text1 else None,
        "response2": mark_safe(response_text2) if response_text2 else None,
        "username": username,
    })




def register(request):
    if request.method=="POST":
        data=request.POST
        user_name=data.get('username')
        email=data.get('email')
        password=data.get('password1')
        password1=data.get('password2')
        if password1!=password:
            messages.error(request, "Password didnt match")
            return render(request,'signupman.html')
        
        if User.objects.filter(username=user_name).exists():
            messages.error(request, "Username already taken!")
            return render(request, "signupman.html")
        user=User.objects.create(username=user_name,email=email)
        user.set_password(password)
        user.save()
        login(request,user)
        return redirect('home')
    return render(request,'signupman.html')

def login_view(request):
    if request.method=="POST":
        data=request.POST
        user_name=data.get('username')
        password=data.get('password')
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user) 
            return redirect('home')
        else:
            messages.error(request,"Invalid Username or password")
            return redirect('login_view')
    return render(request,'login.html')






