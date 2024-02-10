# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 21:29:34 2024

@author: Jungyu Lee
"""
import boto3
import base64

class SpeechService:
    def __init__(self):
        self.polly_client = boto3.client('polly')
        
    def synthesize_speech(self, text, output_format='mp3', language_code='en-US', voice_id='Matthew'):
        response = self.polly_client.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice_id,
            LanguageCode=language_code)
        
        audio_stream = response.get('AudioStream').read()

        audio_base64 = base64.b64encode(audio_stream).decode('utf-8')

        # save the audio stream
        file_path = f"{text[:5]}.mp3"
        with open(file_path, 'wb') as file:
            file.write(audio_stream)
        
        return audio_base64, file_path
    