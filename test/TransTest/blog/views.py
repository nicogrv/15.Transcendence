from django.shortcuts import render
from django.http import JsonResponse
from .models import UserPong
from django.core import serializers

def apiGetUser(req):
    user = serializers.serialize("json", UserPong.objects.all())
    return JsonResponse({"json": user})
def apiUpdateUser(req, uid, elem, value):
	print("id: " + uid)
	print("elem: " + elem)
	print("value: " + value)
	if (elem == "Name"):
		UserPong.objects.filter(uid = uid).update(Name = value)
	elif (elem == "Age"):
		UserPong.objects.filter(uid = uid).update(Age = value)
	return JsonResponse({"json": "ok"})




def blogBd(req):
	return render(req, 'blog/blog_index.html')


def idF(req, id):
	return render(req, 'blog/id.html')

