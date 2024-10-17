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
                translator = Translator(to_lang=target_language)
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

           
            file_path = os.path.join("D:\Robot\myproject\hello", audio_file)  
            tts.save(file_path)

            
            with open(file_path, "rb") as f:
                file_data = f.read()

            
            response = HttpResponse(file_data, content_type='audio/mpeg')
            response['Content-Disposition'] = f'attachment; filename="{audio_file}"'

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

@csrf_exempt
def customer_face_recognition(request):
    if request.method == 'POST':
        try:
            image = request.FILES.get('image')

            if not image:
                return JsonResponse({"error": "Image file is required"}, status=400)

            base_dir = os.path.dirname(os.path.abspath(__file__))

            excel_path = os.path.join(base_dir, "CustomerData.xlsx")

            try:
                df = pd.read_excel(excel_path)
            except Exception as e:
                return JsonResponse({"error": f"Failed to read Excel file: {str(e)}"}, status=500)

            existing_image = df[df['ImagePath'].apply(lambda x: os.path.basename(x) == image.name)]

            if not existing_image.empty:
                existing_customer_name = existing_image.iloc[0]['CustomerName']
                return JsonResponse({"message": f"Welcome {existing_customer_name}!"}, status=200)
            else:
                return JsonResponse({"message": "Looks like you are new to our bank. Please register."}, status=400)

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

           
            try:
                df = pd.read_excel(excel_path)
            except Exception as e:
                return JsonResponse({"error": f"Failed to read Excel file: {str(e)}"}, status=500)

            
            IMAGE_FOLDER = 'images/'
            image_save_path = f"{IMAGE_FOLDER}{image.name}"  # Relative path
            image_absolute_path = default_storage.save(image_save_path, ContentFile(image.read()))

            
            new_customer_data = pd.DataFrame({
                'CustomerName': [customer_name],
                'ImagePath': [image_save_path] 
            })

           
            df = pd.concat([df, new_customer_data], ignore_index=True)

            
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
