# from django.urls import path

# from .views import hello, translate_text

# urlpatterns = [
#     path('translate', translate_text, name='translate_text'),
#     path('hello', hello, name='hello'),
# ]



from django.urls import path
from .views import hello, translate_text, generate_speech, customer_face_recognition, customer_registration

urlpatterns = [
    path('translate', translate_text, name='translate_text'),
    path('hello', hello, name='hello'),
    path('generate-speech', generate_speech, name='generate_speech'), 
    path('face', customer_face_recognition, name='customer_face_recognition'),
    path('register', customer_registration, name='customer_registration'),
]
