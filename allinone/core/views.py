import os
import requests
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
import markdown
from django.utils.safestring import mark_safe

import os
import requests
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt  # For handling POST requests

GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
API_KEY = os.getenv("GEMINI_API_KEY")  # Ensure this is set in your .env file or settings

@csrf_exempt  # Use this only if CSRF token is not required
def home(request):
    response_text = None

    if request.method == "POST":
        user_input = request.POST.get("input_text", "").strip()

        # Ensure the input includes instructions
        
        user_input += " Ingredients (with precise measurements) along with Nutritional values, Step-by-step procedure, Alternative ingredients for improved nutritional benefits only this no other extra information strictly these as per instruction"

        # Call Gemini API
        headers = {"Content-Type": "application/json"}
        payload = {"contents": [{"parts": [{"text": user_input}]}]}
        params = {"key": API_KEY}

        gemini_response = requests.post(GEMINI_API_URL, headers=headers, json=payload, params=params)

        if gemini_response.status_code == 200:
            data = gemini_response.json()
            response_text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "No response received")
        else:
            response_text = f"Error: {gemini_response.status_code} - {gemini_response.text}"
        response_text = markdown.markdown(response_text)  # Convert Markdown to HTML
    return render(request, "index.html", {"response": mark_safe(response_text)})
    

def register(request):
    if request.method=="POST":
        data=request.POST
        user_name=data.get('username')
        email=data.get('email')
        password=data.get('password1')
        password1=data.get('password2')
        if password1!=password:
            messages.error(request, "Password didnt match")
            return render(request,'register.html')
        
        if User.objects.filter(username=user_name).exists():
            messages.error(request, "Username already taken!")
            return render(request, "register.html")
        user=User.objects.create(username=user_name,email=email)
        user.set_password(password)
        user.save()
        login(request,user)
        return redirect('home')
    return render(request,'register.html')

def login_view(request):
    if request.method=="POST":
        data=request.POST
        user_name=data.get('username')
        password=data.get('password')
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            return redirect('home')
        else:
            messages.error(request,"Invalid Username or password")
            return redirect('login')
    return render(request,'login.html')






