# Additional imports
import pvporcupine
import numpy as np
import pyaudio
import psutil


# imports...
import os
import openai
import speech_recognition as sr
import pygame
import time
from elevenlabs import generate, play, stream, voices, set_api_key
import subprocess
import threading
import logging
import configparser



# Configurations
config = configparser.ConfigParser()
config.read('config.ini')

# Logging
logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

# Set api keys
set_api_key(config['elevenlabs']['api_key'])
openai.api_key = config['openai']['api_key']

# Initialize ///speech recognizer///nomore and pygame mixer

pygame.mixer.init()

sound_wake= pygame.mixer.Sound('wake_sound.wav')
sound_end= pygame.mixer.Sound('end_sound.wav')



# Initialize Porcupine
def initialize_porcupine():
    
    porcupine = None
    pa = None
    audio_stream = None

    try:
        access_key = config['porcupine']['access_key']  # Replace with the correct section and key in your config.ini
        porcupine = pvporcupine.create(access_key=access_key, keywords=["computer"])  # Replace "picovoice" with your desired wake word
        pa = pyaudio.PyAudio()

        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length)

        logging.info("porcupine init")
        print("porcupine init")

    except Exception as e:
        print(f"Failed to initialize Porcupine: {e}")

    return porcupine, pa, audio_stream

def text_to_speech(text):
    #convert text to speech and plays the audio
    try:
     print("Now converting gpt response to audio")
     
     if not text_to_speech.initial_delay_executed:
            time.sleep(2)
            text_to_speech.initial_delay_executed = True
        
     audio = generate(
         text=text,
         voice = "Domi",
         model = "eleven_monolingual_v1",
        
         )

     print("attempting to play audio")
     play(audio)

    except Exception as e:
         logging.error(f"Error in text_to_speech: {e}")
         print(f"Error in text_to_speech: {e}")

# Initialize the flag variable
text_to_speech.initial_delay_executed = False
        
def process_input(text):
    # Process input text and generate a response
    logging.info('Processing input: %s', text)
    prompt = "In the most humorous tremendous way, let me tell you, as a man who speaks just like Donald Trump, " + text + " - nobody does it better, believe me!"

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=1.0
        )
        
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        logging.error(f"Error calling OpenAI API: {e}")
        raise

    print("GPT-4 response:", response)
    logging.info("GPT-4 response: %s", response)
    response_text = response.choices[0].text.strip()
    print("Processed response:", response_text)
    logging.info("Processed response: %s", response_text)

    return response_text

def main():
    
    #init speech recognizer
    r = sr.Recognizer()

    #init porcupine and pyadui
    porcupine, pa, audio_stream = initialize_porcupine()
    
    try:
        is_wake_word_detected = False  # Flag to track wake word detection
        is_talking = False #flag to track talking state
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = np.frombuffer(pcm, dtype=np.int16)
            result = porcupine.process(pcm)
            
            #not needed as it spams console with -1's: print("Porcupine result:", result)

            if result >= 0:  # Check if wake word is detected
                is_wake_word_detected = True
                print("Wake word detected.")
                logging.info("Wake word detected.")
                sound_wake.play()

            if is_wake_word_detected:
                with sr.Microphone() as source:
                    try:
                        
                        print("listening...")
                        r.energy_threshold = 1500  # Adjust the threshold as needed
                        audio_data = r.listen(source, timeout=5, phrase_time_limit=10)

                        text = r.recognize_google(audio_data)
                        print("Recognized Speech:", text)
                        logging.info("Recognized Speech: %s", text)

                        if text.lower() == "can you repeat that":
                            text_to_speech(previous_response)
                        
                        else:
                            sound_end.play()
                            response = process_input(text)
                            text_to_speech(response)
                            previous_response = response

                        is_wake_word_detected = False  # Reset the flag if silence is detected
                      
                    except sr.UnknownValueError:
                        print("Silence Detected. Stopping...")
                        is_wake_word_detected = False  # Reset the flag if silence is detected
    
                    except sr.WaitTimeoutError:
                        print("No speech detected within the timeout. Stopping...")
                        is_wake_word_detected = False #reset the flag if silence is detected
                                           
            elif result == -1:
                is_wake_word_detected = False  # Reset the flag after processing audio
       




    except KeyboardInterrupt:
        print('Stopping ...')
        logging.info("Stopping...")
        
    finally:
        #clean up resaources in finally 
        if audio_stream is not None:
            audio_stream.close()

        if pa is not None:
            pa.terminate()

        if porcupine is not None:
            porcupine.delete()

if __name__ == "__main__":
    main()
