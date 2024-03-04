from django.shortcuts import render
from .models import Article

def blogBd(req):
	test = Article.objects.all()
	data = {'test': test}
	return render(req, 'blog/blog_index.html', data)

def idF(req, id):
	print(id)
	return render(req, 'blog/id.html')