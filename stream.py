import streamlit as st
import sounddevice as sd
import speech_recognition as sr
import numpy as np
import wavio

def record_audio(filename, duration=5, samplerate=16000):
    """
    Records audio using sounddevice and saves it as a WAV file.
    """
    st.write("Recording... Please speak now!")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    wavio.write(filename, audio_data, samplerate, sampwidth=2)  # Save audio in WAV format
    st.write("Recording completed.")
    return filename

def process_audio(file_path):
    """
    Converts audio to text using speech_recognition.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            st.write("Loading and processing audio...")
            audio = recognizer.record(source)  # Read the entire audio file
            text_output = recognizer.recognize_google(audio)
            st.success(f"Recognized Text: {text_output}")
            return text_output

    except sr.UnknownValueError:
        st.error("Sorry, the audio could not be understood.")
        return None
    except sr.RequestError as e:
        st.error(f"Error with the recognition service: {e}")
        return None

# Streamlit App
def main():
    st.title("Speech-to-Text Converter")
    st.write("This app records your voice and converts it to text.")

    duration = st.slider("Select the recording duration (seconds):", min_value=1, max_value=10, value=5)
    audio_file = "recorded_audio.wav"

    if st.button("Start Recording"):
        with st.spinner("Recording..."):
            record_audio(audio_file, duration)
        st.success("Recording completed! Click 'Process Audio' to extract text.")

    if st.button("Process Audio"):
        with st.spinner("Processing audio..."):
            process_audio(audio_file)

if __name__ == "__main__":
    main()
