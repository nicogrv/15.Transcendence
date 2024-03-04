from django.shortcuts import render

def helloTitou(request):
	return render(request, 'home/index.html')
