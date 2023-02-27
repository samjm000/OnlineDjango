from django.contrib import admin
from django.urls import path
from .views import KaiListView, QuestionDetailView

from . import views


urlpatterns = [
    path('result/', views.result, name="result"),
    path('', KaiListView.as_view(), name="results"),
]
