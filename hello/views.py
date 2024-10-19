import uuid
from django.http import JsonResponse
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import numpy as np
from translate import Translator
from gtts import gTTS
import os
import pandas as pd
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from googletrans import Translator
from deep_translator import GoogleTranslator  # type: ignore
import face_recognition
from PIL import Image 


@csrf_exempt 
def translate_text(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            texts = data.get('texts')  
            target_language = data.get('target_language')  

            if not texts or not target_language:
                return JsonResponse({"error": "Invalid data"}, status=400)

            def translate_individual_text(text, target_language):                
                translator = GoogleTranslator(source='auto', target=target_language)
                return translator.translate(text)

            translated_texts = [translate_individual_text(text, target_language) for text in texts]
            return JsonResponse({"translated_texts": translated_texts}, status=200)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "POST method required"}, status=405)




@csrf_exempt
def generate_speech(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            text = data.get('text')
            language = data.get('language')

            if not text or not language:
                return JsonResponse({"error": "Text and language are required"}, status=400)

            
            tts = gTTS(text=text, lang=language)
            audio_file = "translated_speech.mp3"

            
            base_dir = os.path.dirname(os.path.abspath(__file__))
            relative_audio_dir = "generated_audios" 
            audio_dir_path = os.path.join(base_dir, relative_audio_dir)

            
            if not os.path.exists(audio_dir_path):
                os.makedirs(audio_dir_path)

           
            file_path = os.path.join(audio_dir_path, audio_file)
            tts.save(file_path)

            
            with open(file_path, "rb") as f:
                file_data = f.read()

            
            response = HttpResponse(file_data, content_type='audio/mpeg')
            response['Content-Disposition'] = f'attachment; filename="{audio_file}"'

           
            relative_path = os.path.relpath(file_path, base_dir)
            response['X-Audio-File'] = relative_path

            return response

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "POST method required"}, status=405)
    


# @csrf_exempt
# def check_customer_registration(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             customer_name = data.get('customer_name')  # Get customer name from request
#             image = data.get('image')  # Get image from request

#             print(f"Received customer_name: {customer_name}")  # Debug print
#             print(f"Received image path: {image}")  # Debug print

#             if not customer_name:
#                 return JsonResponse({"error": "Customer name is required"}, status=400)

#            
#             excel_path = "D:/Robot/myproject/CustomerData.xlsx"  

#             
#             if not os.path.exists(excel_path):
#                 return JsonResponse({"error": "Excel file does not exist."}, status=404)

#             
#             try:
#                 df = pd.read_excel(excel_path, engine='openpyxl')
#             except Exception as e:
#                 return JsonResponse({"error": f"Failed to read Excel file: {str(e)}"}, status=500)

#             
#             if customer_name in df['CustomerName'].values:
#                 return JsonResponse({"message": f"Welcome {customer_name}!"}, status=200)
#             else:
#               
#                 if image and not os.path.exists(image):
#                     return JsonResponse({"error": "Image file does not exist."}, status=400)

#                
#                 try:
#                     new_customer_data = pd.DataFrame({'CustomerName': [customer_name], 'ImagePath': [image]})
#                 except Exception as e:
#                     return JsonResponse({"error": f"Failed to create DataFrame: {str(e)}"}, status=500)

#                 try:
#                     df = pd.concat([df, new_customer_data], ignore_index=True)  
#                 except Exception as e:
#                     return JsonResponse({"error": f"Failed to append new data: {str(e)}"}, status=500)

#                
#                 try:
#                     df.to_excel(excel_path, index=False)
#                 except Exception as e:
#                     return JsonResponse({"error": f"Failed to save Excel file: {str(e)}"}, status=500)

#                 return JsonResponse({"message": "Looks like you are new to our bank. Please fill in your details."}, status=201)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
#     else:
#         return JsonResponse({"error": "POST method required"}, status=405)



# @csrf_exempt
# def customer_face_recognition(request):
#     if request.method == 'POST':
#         try:
#            
#             image = request.FILES.get('image')
#             customer_name = request.POST.get('customer_name')

#             if not image:
#                 return JsonResponse({"error": "Image file is required"}, status=400)

#           
#             excel_path = "D:/Robot/myproject/CustomerData.xlsx"

#            
#             try:
#                 df = pd.read_excel(excel_path)
#             except Exception as e:
#                 return JsonResponse({"error": f"Failed to read Excel file: {str(e)}"}, status=500)

#            
#             existing_image = df[df['ImagePath'].apply(lambda x: os.path.basename(x) == image.name)]

#             if not existing_image.empty:
#                
#                 existing_customer_name = existing_image.iloc[0]['CustomerName']
#                 return JsonResponse({"message": f"Welcome {existing_customer_name}!"}, status=200)
#             else:
#                
#                 if not customer_name:
#                     return JsonResponse({"error": "Customer name is required for new registration"}, status=400)

#                
#                 image_save_path = f"D:/Robot/myproject/images/{image.name}"
#                 image_path = default_storage.save(image_save_path, ContentFile(image.read()))

#                
#                 new_customer_data = pd.DataFrame({
#                     'CustomerName': [customer_name],
#                     'ImagePath': [image_save_path]
#                 })

#         
#                 df = pd.concat([df, new_customer_data], ignore_index=True)

#                
#                 df.to_excel(excel_path, index=False)

#                 return JsonResponse({"message": "You are successfully registered"}, status=201)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
#     else:
#         return JsonResponse({"error": "POST method required"}, status=405)

IMAGE_FOLDER = 'images/'

# @csrf_exempt
# def customer_face_recognition(request):
#     if request.method == 'POST':
#         try:
#             image = request.FILES.get('image')

#             if not image:
#                 return JsonResponse({"error": "Image file is required"}, status=400)

#             base_dir = os.path.dirname(os.path.abspath(__file__))

#             excel_path = os.path.join(base_dir, "CustomerData.xlsx")

#             try:
#                 df = pd.read_excel(excel_path)
#             except Exception as e:
#                 return JsonResponse({"error": f"Failed to read Excel file: {str(e)}"}, status=500)

#             existing_image = df[df['ImagePath'].apply(lambda x: os.path.basename(x) == image.name)]

#             if not existing_image.empty:
#                 existing_customer_name = existing_image.iloc[0]['CustomerName']
#                 return JsonResponse({"message": f"Welcome {existing_customer_name}!"}, status=200)
#             else:
#                 return JsonResponse({"message": "Looks like you are new to our bank. Please register."}, status=400)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
#     else:
#         return JsonResponse({"error": "POST method required"}, status=405)



# @csrf_exempt
# def customer_face_recognition(request):
#     if request.method == 'POST':
#         try:
#             image = request.FILES.get('image')
#             language = request.POST.get('language', 'en') 

#             if not image:
#                 return JsonResponse({"error": "Image file is required"}, status=400)

#             # Define welcome and registration messages
#             welcome_messages = {
#                 'en': "Welcome!",
#                 'ta': "வணக்கம்!",
#                 'te': "స్వాగతం!",
#                 'hi': "स्वागत है!",
#                 'pa': "ਸੁਆਗਤ ਹੈ!"
#             }

#             registration_messages = {
#                 'en': "Looks like you are new to our bank. Please register.",
#                 'ta': "நீங்கள் எங்கள் வங்கியில் புதியவராக இருப்பீர்கள். தயவுசெய்து பதிவு செய்யவும்.",
#                 'te': "మీరు మా బ్యాంకుకు కొత్తగా ఉన్నారు. దయచేసి నమోదు చేసుకోండి.",
#                 'hi': "आप हमारे बैंक में नए हैं। कृपया पंजीकरण करें।",
#                 'pa': "ਤੁਸੀਂ ਸਾਡੇ ਬੈਂਕ ਵਿੱਚ ਨਵੇਂ ਹੋ। ਕਿਰਪਾ ਕਰਕੇ ਰਜਿਸਟਰ ਕਰੋ।"
#             }

#             if language not in welcome_messages:
#                 return JsonResponse({"error": f"Unsupported language code: {language}"}, status=400)

#             base_dir = os.path.dirname(os.path.abspath(__file__))
#             excel_path = os.path.join(base_dir, "CustomerData.xlsx")

#             try:
#                 df = pd.read_excel(excel_path)
#             except Exception as e:
#                 return JsonResponse({"error": f"Failed to read Excel file: {str(e)}"}, status=500)

#             existing_image = df[df['ImagePath'].apply(lambda x: os.path.basename(x) == image.name)]

#             if not existing_image.empty:
#                 existing_customer_name = existing_image.iloc[0]['CustomerName']

#                 try:
#                     transliterated_name = GoogleTranslator(source='en', target=language).translate(existing_customer_name)
#                 except Exception as e:
#                     return JsonResponse({"error": f"Failed to transliterate name: {str(e)}"}, status=500)

#                 message = f"{welcome_messages[language]} {transliterated_name}!"
#             else:
#                 message = registration_messages[language]

#             tts = gTTS(text=message, lang=language, slow=False)
#             unique_filename = f"speech_{language}_{os.path.splitext(image.name)[0]}_{str(uuid.uuid4())[:8]}.mp3"
#             audio_dir = os.path.join(base_dir, "generated_audios", language)
#             if not os.path.exists(audio_dir):
#                 os.makedirs(audio_dir)

#             audio_file_path = os.path.join(audio_dir, unique_filename)
#             tts.save(audio_file_path)

#             relative_audio_path = os.path.relpath(audio_file_path, base_dir)

#             response = JsonResponse({
#                 "message": message,
#                 "language": language
#             })
#             response['X-Audio-File'] = relative_audio_path

#             return response

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
#     else:
#         return JsonResponse({"error": "POST method required"}, status=405)


@csrf_exempt
def customer_face_recognition(request):
    if request.method == 'POST':
        try:
            image = request.FILES.get('image')
            language = request.POST.get('language', 'en') 

            if not image:
                return JsonResponse({"error": "Image file is required"}, status=400)

            welcome_messages = {
                'en': "Welcome!",
                'ta': "வணக்கம்!",
                'te': "స్వాగతం!",
                'hi': "स्वागत है!",
                'pa': "ਸੁਆਗਤ ਹੈ!"
            }

            registration_messages = {
                'en': "Looks like you are new to our bank. Please register.",
                'ta': "நீங்கள் எங்கள் வங்கியில் புதியவராக இருப்பீர்கள். தயவுசெய்து பதிவு செய்யவும்.",
                'te': "మీరు మా బ్యాంకుకు కొత్తగా ఉన్నారు. దయచేసి నమోదు చేసుకోండి.",
                'hi': "आप हमारे बैंक में नए हैं। कृपया पंजीकरण करें।",
                'pa': "ਤੁਸੀਂ ਸਾਡੇ ਬੈਂਕ ਵਿੱਚ ਨਵੇਂ ਹੋ। ਕਿਰਪਾ ਕਰਕੇ ਰਜਿਸਟਰ ਕਰੋ।"
            }

            if language not in welcome_messages:
                return JsonResponse({"error": f"Unsupported language code: {language}"}, status=400)

            base_dir = os.path.dirname(os.path.abspath(__file__))
            excel_path = os.path.join(base_dir, "CustomerData.xlsx")
            
            try:
                df = pd.read_excel(excel_path)
            except Exception as e:
                return JsonResponse({"error": f"Failed to read Excel file: {str(e)}"}, status=500)

            # Load the uploaded image directly
            uploaded_image = face_recognition.load_image_file(image)
            uploaded_face_encodings = face_recognition.face_encodings(uploaded_image)

            if not uploaded_face_encodings:
                return JsonResponse({"error": "No faces detected in the uploaded image."}, status=400)

            uploaded_face_encoding = uploaded_face_encodings[0]

            customer_found = False
            existing_customer_name = ""

            for index, row in df.iterrows():
                stored_image_path = row['ImagePath']  # This should be the relative path
                stored_image_path_full = os.path.join(base_dir, stored_image_path)

                # Load the stored image using the relative path
                if os.path.exists(stored_image_path_full):
                    stored_image = face_recognition.load_image_file(stored_image_path_full)
                    stored_face_encodings = face_recognition.face_encodings(stored_image)

                    if stored_face_encodings:
                        stored_face_encoding = stored_face_encodings[0]

                        # Compare faces
                        match = face_recognition.compare_faces([stored_face_encoding], uploaded_face_encoding)

                        if match[0]:
                            customer_found = True
                            existing_customer_name = row['CustomerName']
                            break

            if customer_found:
                try:
                    transliterated_name = GoogleTranslator(source='en', target=language).translate(existing_customer_name)
                except Exception as e:
                    return JsonResponse({"error": f"Failed to transliterate name: {str(e)}"}, status=500)

                message = f"{welcome_messages[language]} {transliterated_name}!"
                status_code = 200
            else:
                message = registration_messages[language]
                status_code = 401

            # Generate audio response
            tts = gTTS(text=message, lang=language, slow=False)
            unique_filename = f"speech_{language}_{str(uuid.uuid4())[:8]}.mp3"
            audio_dir = os.path.join(base_dir, "generated_audios", language)
            if not os.path.exists(audio_dir):
                os.makedirs(audio_dir)

            audio_file_path = os.path.join(audio_dir, unique_filename)
            tts.save(audio_file_path)

            relative_audio_path = os.path.relpath(audio_file_path, base_dir)

            response = JsonResponse({
                "message": message,
                "language": language
            }, status=status_code)
            response['X-Audio-File'] = relative_audio_path

            return response

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "POST method required"}, status=405)


@csrf_exempt
def customer_registration(request):
    if request.method == 'POST':
        try:
            customer_name = request.POST.get('customer_name')
            image = request.FILES.get('image')

            if not customer_name or not image:
                return JsonResponse({"error": "Customer name and image are required"}, status=400)

            base_dir = os.path.dirname(os.path.abspath(__file__))
            excel_path = os.path.join(base_dir, "CustomerData.xlsx")

            # Create the images directory if it doesn't exist
            IMAGE_FOLDER = os.path.join(base_dir, 'images/')
            if not os.path.exists(IMAGE_FOLDER):
                os.makedirs(IMAGE_FOLDER)

            # Save the uploaded image file
            image_save_path = os.path.join(IMAGE_FOLDER, image.name)

            # Check if the image already exists
            if os.path.exists(image_save_path):
                return JsonResponse({"error": "This face is already registered with another customer."}, status=400)
            else:
                default_storage.save(image_save_path, ContentFile(image.read()))

            # Load the uploaded image for face recognition
            uploaded_image = face_recognition.load_image_file(image_save_path)
            uploaded_face_encodings = face_recognition.face_encodings(uploaded_image)

            if not uploaded_face_encodings:
                return JsonResponse({"error": "No faces detected in the uploaded image."}, status=400)

            uploaded_face_encoding = uploaded_face_encodings[0]

            # Try to read the Excel file
            try:
                df = pd.read_excel(excel_path)
            except Exception as e:
                return JsonResponse({"error": f"Failed to read Excel file: {str(e)}"}, status=500)

            # Check if the customer already exists by comparing faces
            for index, row in df.iterrows():
                stored_image_path = row['ImagePath']
                stored_image_path_full = os.path.join(base_dir, stored_image_path)  # Construct the full path

                # Load the stored image
                if os.path.exists(stored_image_path_full):
                    stored_image = face_recognition.load_image_file(stored_image_path_full)
                    stored_face_encodings = face_recognition.face_encodings(stored_image)

                    if stored_face_encodings:
                        stored_face_encoding = stored_face_encodings[0]

                        # Compare the uploaded face with stored face encoding
                        match = face_recognition.compare_faces([stored_face_encoding], uploaded_face_encoding)

                        if match[0]:
                            return JsonResponse({"error": "This face is already registered with another customer."}, status=400)

            # Add the new customer data to the Excel file
            new_customer_data = pd.DataFrame({
                'CustomerName': [customer_name],
                'ImagePath': [f"images/{image.name}"]  # Store only the relative path
            })

            # Append the new customer data to the existing DataFrame
            df = pd.concat([df, new_customer_data], ignore_index=True)

            # Save the updated DataFrame back to the Excel file
            df.to_excel(excel_path, index=False)

            return JsonResponse({"message": "You are successfully registered"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "POST method required"}, status=405)
    


@csrf_exempt
def hello(request):
    if request.method == 'GET':
        return JsonResponse({"message": "Hello, Django!"}, status=200)
    else:
        return JsonResponse({"error": "GET method required"}, status=405)
