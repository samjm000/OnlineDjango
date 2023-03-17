from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from .models import Question
from . import q_a_system
import asyncio

def result(request):
    search_data = request.GET["search_data"]
    search_response = "hello"
    pinecone_testing.test_pinecone()
    #search_response = asyncio.run(q_a_system.get_answers(search_data))
    return render(request, "result.html", {"home_input": search_response},)


class KaiListView(ListView):
    model = Question
    template_name = "result.html"


class QuestionDetailView(DetailView):
    model = Question
    template_name = "question_detail.html"
    fields = ["title", "author", "result"]
