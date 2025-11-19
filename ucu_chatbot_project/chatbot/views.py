import os, json
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import ChatMessage
from .forms import RegisterForm

# Gemini client - optional import to avoid hard crash if not installed.
try:
    from google import genai
except Exception:
    genai = None

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat_home')
    else:
        form = RegisterForm()
    return render(request, 'chatbot/register.html', {'form': form})

@login_required
def chat_home(request):
    return render(request, 'chatbot/index.html')

@csrf_exempt
@login_required
def chat_api(request):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST allowed')
    try:
        payload = json.loads(request.body)
        user_message = payload.get('message','').strip()
        if not user_message:
            return JsonResponse({'error':'empty message'}, status=400)

        ChatMessage.objects.create(role='user', content=user_message)

        # Build system prompt
        system_prompt = (
            "You are UCU Student Assistant. Answer politely and concisely. "
            "Mention when you're unsure and suggest campus resources like the academic registry or student portal."
        )
        prompt = f"""SYSTEM: {system_prompt}\nUSER: {user_message}\nASSISTANT:"""

        assistant_text = "Sorry, AI client not available on server."
        # Call Gemini if available and API key present
        if genai is not None and GEMINI_API_KEY:
            client = genai.Client(api_key=GEMINI_API_KEY)
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                # response may provide text attribute or more complex structure
                assistant_text = getattr(response, 'text', str(response))
            except Exception as e:
                assistant_text = f"Error calling Gemini API: {e}"
        else:
            if genai is None:
                assistant_text = "Gemini client library not installed on server."
            else:
                assistant_text = "GEMINI_API_KEY not set on server."

        ChatMessage.objects.create(role='assistant', content=assistant_text)
        return JsonResponse({'reply': assistant_text})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

