import speech_recognition as sr

def speech_to_text():
    # Initialize recognizer

    recognizer = sr.Recognizer()

    # Use the default microphone as the audio source
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise... Please wait.")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("Listening... Speak now.")

            # Capture the audio
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

        try:
            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text


        except sr.UnknownValueError:

            return "Sorry, I could not understand the audio"
        except sr.RequestError as e:

            return f"Could not request results; check your internet connection. Error: {e}"

    except sr.WaitTimeoutError:

        return "Listening timed out while waiting for phrase to start."
    except OSError as e:

        return f"Microphone not found or not accessible: {e}"

if __name__ == "__main__":
    speech_to_text()