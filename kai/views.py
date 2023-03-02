from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from .models import Question
from . import machine_learning_model
from . import q_a_system


def result(request):
    search_data = request.GET["search_data"]
    #search_data = machine_learning_model.multiplier(search_data)
    search_response = q_a_system.predictionModel(search_data)
    return render(request, "result.html", {"home_input": search_response})
    #return "hello"


class KaiListView(ListView):
    model = Question
    template_name = "result.html"


class QuestionDetailView(DetailView):
    model = Question
    template_name = "question_detail.html"
    fields = ["title", "author", "result"]
