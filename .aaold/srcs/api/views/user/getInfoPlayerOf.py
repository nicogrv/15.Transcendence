from django.http import JsonResponse
from pong.models.player import Player
from pong.models.relation import Relation


def getInfoPlayerOf(req):

    username = req.GET.get('username')
    data = {}
    if (req.COOKIES and "PongToken" in req.COOKIES and username):
        token = req.COOKIES["PongToken"]
    else:
        return JsonResponse({"error": "No cookie or username"})
    try:
        me = Player.objects.filter(token_login=token)
        him = Player.objects.filter(username=username)
        if (me.count() != 1 or him.count() != 1):
            return JsonResponse({"error": "error"})
        relation1 = Relation.objects.filter(uid_user_one=me[0].uid, uid_user_two=him[0].uid)
        relation2 = Relation.objects.filter(uid_user_one=him[0].uid, uid_user_two=me[0].uid)
        if (int(relation1.count()) + int(relation2.count()) == 0):
            relation = Relation(uid_user_one=me[0], uid_user_two=him[0])
            relation.save()
            data['relationMeHim'] = relation.getRelationOneToTwo()
            data['relationHimMe'] = relation.getRelationTwoToOne()
        elif (int(relation1.count()) == 1):
            relation = relation1[0]
            data['relationMeHim'] = relation.getRelationOneToTwo()
            data['relationHimMe'] = relation.getRelationTwoToOne()
        elif (int(relation2.count()) == 1):
            relation = relation2[0]
            data['relationHimMe'] = relation.getRelationOneToTwo()
            data['relationMeHim'] = relation.getRelationTwoToOne()
        else:
            raise ValueError("plusieur element in db")
    except Exception as e:
        print(f"ERROR: {e}")
        return JsonResponse({"error": str(e)})
    data['username'] = him[0].getUsername()
    data['pic'] = him[0].getPic()
    data['elo'] = him[0].getElo()
    data['victories'] = him[0].getVictories()
    data['defeats'] = him[0].getDefeats()
    data['status'] = him[0].getStatus()
    return JsonResponse(data)
