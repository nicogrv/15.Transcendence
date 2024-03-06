from django.shortcuts import render
from django.http import HttpResponse
from .models import Person

def person_detail(request, slug):
    try:
        person = Person.objects.get(username=slug)
        return render(request, 'person.html', {'person' : person})
    except Exception as e:
        return render(request, 'person.html')

def say_hello(request):
    persons = Person.objects.all().order_by('username')
    return render(request, 'hello.html', {'persons' : persons})
