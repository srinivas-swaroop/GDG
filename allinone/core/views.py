import os
import requests
from django.shortcuts import render
from django.http import JsonResponse

def home(request):
    if request.method == "POST":
        user_input = request.POST.get("input_text", "").strip()
        if not user_input:
            return JsonResponse({"error": "No input provided"}, status=400)

        gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        headers = {"Content-Type": "application/json"}
        params = {"key": os.getenv("GEMINI_API_KEY")}  
        payload = {
            "contents": [{"parts": [{"text": user_input}]}]
        }

        try:
            response = requests.post(gemini_api_url, json=payload, headers=headers, params=params)
            print("\n🔹 API Response Status Code:", response.status_code)
            print("🔹 API Response JSON:", response.text, "\n")
            data = response.json()
            ai_response = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Error generating response")

        except Exception as e:
            ai_response = f"API Error: {str(e)}"

        return JsonResponse({"response": ai_response})

    return render(request, "index.html")
