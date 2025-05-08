from flask import Flask, render_template, request
import google.generativeai as genai
import requests

# Flask app setup
app = Flask(__name__)

# Gemini API key setup
genai.configure(api_key="AIzaSyAz8QCOEusyF_N86j3jC5qFPWGWSHB-gCU")

# OpenWeatherMap API
weather_api_key = "eb9d34e31b5d0ef717eca582e21bee70"

# Tamil/English Translation Helpers (Basic - Extendable)
def to_tamil(text):
    # Placeholder - integrate a real translation model or API here
    return "தமிழில்: " + text

def to_english(text):
    # Placeholder - assumes user typed Tamil; in real case, use translation
    return text

# Gemini-based crop, weather, and harvesting agent
def gemini_agriculture_agent(prompt):
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
    response = model.generate_content(prompt)
    return response.text.strip()

# Weather + irrigation/harvest suggestion agent
def get_weather_advice(city, lang='en'):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric&lang={lang}"
    data = requests.get(url).json()

    if data.get("cod") != 200:
        error_message = "Weather data not available." if lang == 'en' else "வானிலை தரவை பெற முடியவில்லை."
        return error_message

    desc = data['weather'][0]['description']
    temp = data['main']['temp']
    humidity = data['main']['humidity']

    # Constructing weather-related advice
    prompt = f"""The weather in {city} is {desc} with temperature {temp}°C and humidity {humidity}%. 
    Suggest whether today is suitable for irrigation and harvesting in Indian agriculture."""

    result = gemini_agriculture_agent(prompt)
    return to_tamil(result) if lang == 'ta' else result

# Flask routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['question']
        lang = request.form['language']
        user_lang = 'ta' if lang == "தமிழ்" else 'en'

        # Process input directly in Tamil (no translation required)
        input_text = user_input.strip()

        # If the user is asking about weather
        if 'weather' in input_text.lower():
            city = "Salem"  # Default city, you can expand this
            weather_response = get_weather_advice(city, lang=user_lang)
            return render_template('index.html', response=weather_response, lang=lang)

        else:
            # Handle other types of agricultural questions
            prompt = f"Answer this agricultural question as a chatbot in {lang}: {input_text}"
            result = gemini_agriculture_agent(prompt)
            output = to_tamil(result) if user_lang == 'ta' else result
            return render_template('index.html', response=output, lang=lang)
    return render_template('index.html', response=None)

if __name__ == '__main__':
    app.run(debug=True)
