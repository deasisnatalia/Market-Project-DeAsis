from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import google.generativeai as genai

#API key
genai.configure(api_key="AIzaSyBd1P8cv4uGg2pHyLaBkp_xraQRzfflwPw")

@login_required
def chat_ia(request):
    if request.method == 'POST':
        pregunta = request.POST.get('mensaje', '')
        model = genai.GenerativeModel("gemini-2.5-flash")

        #respuesta
        response = model.generate_content(
            f"Eres un asistente útil para la app de mercado 'Michi Mercado'. "
            f"Responde en español, sé amable y clara. Usuario: {pregunta}"
        )
        return JsonResponse({'respuesta': response.text})
