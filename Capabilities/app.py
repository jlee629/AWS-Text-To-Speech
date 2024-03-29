from chalice import Chalice
from chalicelib import storage_service
from chalicelib import recognition_service
from chalicelib import translation_service
from chalicelib import speech_service

import base64
import json

#####
# chalice app configuration
#####
app = Chalice(app_name='Capabilities')
app.debug = True

#####
# services initialization
#####
storage_location = 'contentcen301236221.aws.ai'
storage_service = storage_service.StorageService(storage_location)
recognition_service = recognition_service.RecognitionService(storage_service)
translation_service = translation_service.TranslationService()
speech_service = speech_service.SpeechService()

#####
# RESTful endpoints
#####
@app.route('/images', methods = ['POST'], cors = True)
def upload_image():
    """processes file upload and saves file to storage service"""
    request_data = json.loads(app.current_request.raw_body)
    file_name = request_data['filename']
    file_bytes = base64.b64decode(request_data['filebytes'])

    image_info = storage_service.upload_file(file_bytes, file_name)

    return image_info

@app.route('/images/{image_id}/translate-text', methods=['POST'], cors=True)
def translate_image_text(image_id):
    """Detects, translates, and synthesizes speech for text in the specified image."""
    app.log.debug(f"Raw request body: {app.current_request.raw_body.decode('utf-8')}")

    request_data = json.loads(app.current_request.raw_body)
    from_lang = request_data['fromLang']
    to_lang = request_data['toLang']

    MIN_CONFIDENCE = 80.0

    text_lines = recognition_service.detect_text(image_id)

    translated_lines = []
    for line in text_lines:
        if float(line['confidence']) >= MIN_CONFIDENCE:
            translated_line = translation_service.translate_text(line['text'], from_lang, to_lang)

            # response = speech_service.synthesize_speech(text=translated_line['translatedText'])
            response, file_path = speech_service.synthesize_speech(text=translated_line['translatedText'])

            translated_lines.append({
                'text': line['text'],
                'translation': translated_line,
                'boundingBox': line['boundingBox'],
                'audioBase64': response
            })

    return translated_lines

# health check
@app.route('/hello', methods=['GET'], cors=True)
def hello_world():
    """Returns a simple 'Hello World' message"""
    return {'message': 'Hello World!'}
