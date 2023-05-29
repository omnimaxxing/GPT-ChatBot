# Python Voice Assistant with OpenAI and Eleven Labs

This repository contains a Python-based voice assistant that uses sound effects to add a level of realism to its interactions. The assistant uses OpenAI's GPT-3 model for generating responses and the ElevenLabs API for voice output.

## Overview

The voice assistant is activated by a wake word, in this case, "Computer". Upon detecting the wake word, the assistant listens for a command or query. This input is processed, and a response is generated using GPT-3. The response is then converted to speech using Eleven Labs' text-to-speech capabilities.

## Features

- **Wake-word activation**: The voice assistant is activated by saying the word "Computer".
- **Real-time interaction**: The assistant interacts with users in ~real-time, receiving voice inputs and providing voice responses.
- **Text generation**: The assistant uses OpenAI's GPT-3 model to generate responses to user inputs.
- **Voice Response**: The assistant uses the ElevenLabs API to output the GPT response.
- **Sound effects**: The assistant incorporates sound effects to add responsiveness to the voice interactions.

## Code Structure

The repository contains a single Python script and config file that includes all the necessary code for the voice assistant. The script utilizes the following libraries.

- **'pvporcupine'**: For wake word detection
- **'pyaudio'**: For capturing audio input
- **'speech_recognition'**: For converting speech to text
- **'pygame'**: For playing audio files
- **'openai'**: For interacting with the GPT-4 or GPT-3 API
- **'elevenlabs'**: For text-to-speech conversion

## Requirements

- Python 3.7 or later
- The following Python packages: pvporcupine, numpy, pyaudio, psutil, openai, speech_recognition, pygame, elevenlabs.
- API keys for ElevenLabs and OpenAI and Porcupine/PicoVoice
- Audio files for the sound effects.

## Setup

1. Clone the repository to your local machine.
2. Install the required Python packages.
3. Place your API keys in the `config.ini` file.
4. Place audio files in the same directory as the python file.

## Usage

1. Run the script using Python 3.7 or later.
2. Say the word "Computer" to activate the assistant.
3. Speak your command or question.
4. The assistant will respond in the specified voice model, accompanied by relevant sound effects.
5. Modify the script to utilize GPT-4 if you have GPT-4 access.

## Sound Effects

Sound effects used in this project are sourced from [FreeSounds.org](https://www.freesound.org).

## Ported to Raspberry Pi
This application has been successfully ported to run on a Raspberry Pi 400. Now you can run this voice assistant on a low-cost, high-performance device, making it more accessible and convenient. Please note that you may need to adjust the audio settings on your Raspberry Pi to ensure optimal performance of the assistant.
