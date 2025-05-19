import pyttsx3

def speak_text(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Speed
        voices = engine.getProperty('voices')

        # Choose a suitable voice
        for voice in voices:
            if 'female' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break  # Use first suitable female voice
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Voice error: {e}")
