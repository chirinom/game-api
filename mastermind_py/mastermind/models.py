from django.db import models

from django.contrib.postgres.fields import ArrayField


class GuessModel(models.Model):
    code = ArrayField(models.CharField(max_length=10))
    black_pegs = models.IntegerField(null=False)
    white_pegs = models.IntegerField(null=False)
    game = models.ForeignKey('GameModel', on_delete=models.CASCADE, related_name='guesses')


class GameModel(models.Model):
    num_colors = models.IntegerField(null=False)
    reference = models.CharField(null=False, unique=True, max_length=10)
    num_slots = models.IntegerField(null=False)
    secret_code = ArrayField(models.CharField(max_length=10))
    max_guesses = models.IntegerField(null=False)
    status = models.CharField(max_length=10)
