import streamlit as st
import google.generativeai as genai
import requests

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

# Chatbot Interface
def main():
    st.set_page_config(page_title="🌱 Green Guard Bot", layout="centered")
    st.title("🌾 Green Guard Bot - Agricultural Chatbot")

    lang = st.radio("மொழி தேர்வு / Select Language", ["English", "தமிழ்"])
    user_lang = 'ta' if lang == "தமிழ்" else 'en'

    # Take input in Tamil or English
    user_input = st.text_input("உங்கள் கேள்வியை உள்ளிடவும் / Enter your agricultural question")

    if st.button("Send"):
        if not user_input:
            st.warning("Please enter a question.")
            return

        # Process input directly in Tamil (no translation required)
        input_text = user_input.strip()

        # If the user is asking about weather
        if 'weather' in input_text.lower():
            city = "Salem"  # Default city, you can expand this
            weather_response = get_weather_advice(city, lang=user_lang)
            st.success(weather_response)

        else:
            # Handle other types of agricultural questions
            prompt = f"Answer this agricultural question as a chatbot in {lang}: {input_text}"
            result = gemini_agriculture_agent(prompt)
            output = to_tamil(result) if user_lang == 'ta' else result
            st.success(output)

if __name__ == '__main__':
    main()
