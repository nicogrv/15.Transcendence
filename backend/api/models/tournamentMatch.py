from api.models.playerModel import Player
from api.models.tournament import Tournament
from api.models.match import Match
from api.models.playerTournament import playerTournament
from django.db import models
from datetime import datetime, timedelta
import uuid
from django.db.models import F
import json


class tournamentMatch(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
	tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, blank=False, null=False)
	match = models.ForeignKey(Match, on_delete=models.CASCADE, blank=False, null=False)
	player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='matches_as_player1', blank=False, null=False)
	player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='matches_as_player2', blank=False, null=False)
	level = models.PositiveIntegerField(blank=False, null=False, default=2) #(final, 1/2, 1/4, etc)
	duel = models.PositiveIntegerField(blank=False, null=False, default=2) #(1st 1/2, 2nd 1/2)
	date_create = models.DateTimeField(auto_now_add=True)
	date_max = models.DateTimeField()

	def __str__(self):
		if self:
			return f"{self.player1} vs {self.player2} ({self.level}/{self.duel}) {self.tournament}"

	def json(self):
		player1Name = player2Name = "error"
		winner = ""
		try:
			player1Name = playerTournament.objects.get(Tournament=self.tournament, player=self.player1).name
			player2Name = playerTournament.objects.get(Tournament=self.tournament, player=self.player2).name
			if (self.match.status == "FINISH"):
				winner = playerTournament.objects.get(Tournament=self.tournament, player=self.match.winner).name
			else:
				winner = "--"
		except :
			pass

		return {
			"id" : str(self.id),
			"tournament" : str(self.tournament.id),
			"match" : self.match.jsonWithoutTrueName(player1Name, player2Name, winner),
			"player1" : player1Name,
			"player2" : player2Name,
			"level" : self.level,
			"duel" : self.duel,
			"date_create" : str(self.date_create),
			"date_max" : str(self.date_max)
		}
		
	def create(self, tournament, player1, player2, level, duel, matchTime):
		self.match = Match(player1=player1, player2=player2, tournament=True)
		self.match.save()
		self.tournament = tournament
		self.player1 = player1
		self.player2 = player2
		self.level = level
		self.duel = duel
		nouvelle_date = datetime.now() + timedelta(minutes=matchTime)
		self.date_max = nouvelle_date
		print("tournamentMatch.ID --->", self.tournament.id)
		self.save()



from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Match)
def createNextRoundTournament(sender, instance, **kwargs):
	print(f"instance.tournament = {instance.tournament}")
	if not (instance.tournament):
		return
	try:
		matchTournois = tournamentMatch.objects.get(match=instance) # recup du lien match <-> tournois
		links = tournamentMatch.objects.filter(tournament=matchTournois.tournament) # search tt lien avec le tournois grace a la ligne d avant"
	except:
		print("error in createNextRoundTournament")
		return

	currentLevel = 999999
	for link in links:
		if (link.match.status != 'FINISH'):
			return
		if (link.level < currentLevel):
			currentLevel = link.level
		print(currentLevel)
	if (currentLevel == 1):
		print("iciiii")
		print(matchTournois.tournament)
		matchTournois.tournament.def_END()
		matchTournois.tournament.winner = matchTournois.match.winner.username
		matchTournois.tournament.save(update_fields=['winner'])
		if matchTournois.match.winner == matchTournois.player1:
			player1_win = F('tournaments_won') + 1
		else:
			player2_win = F('tournaments_won') + 1
		Player.objects.filter(id=matchTournois.player1.id).update(
			tournaments_won=player1_win if matchTournois.match.winner == matchTournois.player1 else F('tournaments_won')
		)

		Player.objects.filter(id=matchTournois.player2.id).update(
			tournaments_won=player2_win if matchTournois.match.winner == matchTournois.player2 else F('tournaments_won')
		)
		return
	
	print("je passe iciiiii")
	filterLink = []
	nextLevel = currentLevel/2
	for link in links:
		if (link.level == currentLevel):
			filterLink.append(link)
	filterLink.sort(key=lambda item: item.duel)
	print(int(len(filterLink)/2))
	for index in range(int(len(filterLink)/2)):
		Tmatch = tournamentMatch()
		Tmatch.create(filterLink[0].tournament, filterLink[index*2].match.winner, filterLink[index*2+1].match.winner, nextLevel, int(index+1), filterLink[0].tournament.timeBetweenMatches)
	

# def create(self, tournament, player1, player2, level, duel, matchTime):