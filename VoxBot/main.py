import streamlit as st
import pyttsx3
import random
import requests
import datetime
import webbrowser
import os

# Initialize the TTS engine
engine = pyttsx3.init()

# Function to convert text to speech and save to a file
def speak(text, filename='response.mp3'):
    """Convert text to speech and save as an audio file."""
    engine.save_to_file(text, filename)
    engine.runAndWait()

# Function to tell a random joke
def tell_joke():
    jokes = [
        "Why don’t scientists trust atoms? Because they make up everything!",
        "Why did the math book look sad? Because it had too many problems.",
        "What do you call fake spaghetti? An impasta!",
        "Why did the computer go to the doctor? Because it had a virus!"
    ]
    return random.choice(jokes)

# Function to get weather information
def get_weather(city):
    api_key = "2dcda6d4c1689eda73354f64d3506603"  # Replace with your API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        weather = data['weather'][0]
        temp = main['temp']
        description = weather['description']
        return f"The current temperature in {city} is {temp} degrees Celsius with {description}."
    else:
        return "Sorry, I couldn't fetch the weather information."

# Function to tell the current time
def tell_time():
    return datetime.datetime.now().strftime("%H:%M")

# Function to tell the current date
def tell_date():
    return datetime.datetime.now().strftime("%B %d, %Y")

# Function to perform a basic calculation
def calculate(expression):
    try:
        result = eval(expression)
        return f"The result is {result}."
    except Exception as e:
        return "There was an error in the calculation."

# Function to perform a web search
def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    return f"Here are the results for {query}."

# Streamlit user interface
def main():
    st.title("Voice Assistant")
    st.write("### How can I assist you today?")

    # Continuous input for user command
    command = st.text_input("Enter your command here:", "")

    if st.button("Submit"):
        if command:
            if "hello" in command.lower():
                response = "Hello! How can I assist you today?"
            elif "your name" in command.lower():
                response = "I am your voice assistant."
            elif "how are you" in command.lower():
                response = "I am just a computer program, but thanks for asking!"
            elif "joke" in command.lower():
                response = tell_joke()
            elif "weather" in command.lower():
                city = command.split("in")[-1].strip() if "in" in command else "London"
                response = get_weather(city)
            elif "time" in command.lower():
                response = f"The current time is {tell_time()}."
            elif "date" in command.lower():
                response = f"Today's date is {tell_date()}."
            elif "calculate" in command.lower():
                expression = command.replace("calculate", "").strip()
                response = calculate(expression)
            elif "search" in command.lower():
                query = command.replace("search", "").strip()
                response = search_web(query)
            elif "bye" in command.lower():
                response = "Goodbye!"
            else:
                response = "Sorry, I cannot assist with that."

            st.write("### Response:")
            st.write(response)

            # Save the response to an audio file and play it
            audio_filename = 'response.mp3'
            speak(response, audio_filename)  # Speak and save the response

            # Provide a link to play the audio in Streamlit
            st.audio(audio_filename, format='audio/mp3')

            # Optionally, remove the file after playing to save space
            os.remove(audio_filename)

if __name__ == "__main__":
    main()
