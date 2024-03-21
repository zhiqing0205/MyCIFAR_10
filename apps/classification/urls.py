
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('img/', upload_img_to_classify, name='classify'),
    path('records/', classifyRecords, name='records'),
]
