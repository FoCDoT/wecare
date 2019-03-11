from django.shortcuts import render
import json
from django.http import HttpResponse
# Create your views here.

def base_demo(response):
    return HttpResponse("Data received")


