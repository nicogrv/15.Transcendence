from django.http import JsonResponse
from pong.models.player import Player
from pong.models.relation import Relation


def updateRelation(req):

	try:
		user = req.GET.get('user')
		relationNeed = req.GET.get('relation')
		if (req.COOKIES and "PongToken" in req.COOKIES and user):
			token = req.COOKIES["PongToken"]
		else:
			return JsonResponse({"C NON" : "KO"})
		me = Player.objects.filter(token_login=token)
		him = Player.objects.filter(username=user)
		if (me.count() != 1 or him.count() != 1):
			return JsonResponse({"error": "error"})
		relation1 = Relation.objects.filter(uid_user_one=me[0].uid, uid_user_two=him[0].uid)
		relation2 = Relation.objects.filter(uid_user_one=him[0].uid, uid_user_two=me[0].uid)
		if (int(relation1.count()) == 1):
			relation = relation1[0]
			if (relationNeed == "friends" and relation.two_to_one_relation != 2):
				relation.one_to_two_relation = 1
				relation.save()
			elif (relationNeed == "block"):
				relation.one_to_two_relation = 2
				relation.save()
		elif (int(relation2.count()) == 1):
			relation = relation2[0]
			if (relationNeed == "friends" and relation.one_to_two_relation != 2):
				relation.two_to_one_relation = 1
				relation.save()
			elif (relationNeed == "block"):
				relation.two_to_one_relation = 2
				relation.save()
		else:
			raise ValueError("plusieur element in db")
		
	except Exception as e:
		print(f"ERROR: {e}")
		return JsonResponse({"error": str(e)})

	return JsonResponse({"ok" : "ok"})
