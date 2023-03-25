from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from kai.models import Question
from . import q_a_system
from . import haystack_system

def result(request):
    search_data = request.GET["search_data"]
    search_response = "Updating Data"
    search_response = haystack_system.predictionModel(search_data)
    return render(request, "result.html", {"home_input": search_response})


class KaiListView(ListView):
    model = Question
    template_name = "result.html"

class QuestionDetailView(DetailView):
    model = Question
    template_name = "question_detail.html"
    fields = ["title", "author", "result"]
