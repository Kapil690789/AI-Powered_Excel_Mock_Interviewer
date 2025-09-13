#!/usr/bin/env python3
"""
Setup script for Google Cloud Text-to-Speech API
Run this script to verify your Google Cloud credentials are working correctly.
"""

import os
from google.cloud import texttospeech

def test_tts_setup():
    """Test Google Cloud TTS setup"""
    try:
        # Set credentials path
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-credentials.json'
        
        # Initialize client
        client = texttospeech.TextToSpeechClient()
        
        # Test synthesis
        synthesis_input = texttospeech.SynthesisInput(text="Hello, this is a test of the Text-to-Speech API.")
        
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            name="en-US-Neural2-F",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )
        
        # Save test audio
        with open("test_audio.mp3", "wb") as out:
            out.write(response.audio_content)
        
        print("✅ Google Cloud TTS setup successful!")
        print("📁 Test audio saved as 'test_audio.mp3'")
        return True
        
    except Exception as e:
        print(f"❌ Google Cloud TTS setup failed: {e}")
        print("\n🔧 Troubleshooting steps:")
        print("1. Ensure 'google-credentials.json' exists in the project root")
        print("2. Verify the service account has Text-to-Speech API permissions")
        print("3. Check that the Text-to-Speech API is enabled in your Google Cloud project")
        return False

if __name__ == "__main__":
    test_tts_setup()
