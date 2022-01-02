from typing import Any

from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response

from mastermind_py.mastermind.domain import Game
from mastermind_py.mastermind.repo import Games
from mastermind_py.mastermind.schemas import GameSchema, GuessSchema


class MastermindViewset(viewsets.ViewSet):
    def list(self, request: Any) -> HttpResponse:
        games = Games().all()
        data = GameSchema(many=True).dump(games)
        return Response(data={"results": data})

    def create(self, request: Any) -> HttpResponse:
        data = GameSchema().load(request.data)

        game = Game.new(data["num_slots"], data["num_colors"], data["max_guesses"])
        Games().save(game)

        result = GameSchema().dump(game)

        return Response(status=status.HTTP_201_CREATED, data=result)

    def retrieve(self, request: Any, id: int) -> HttpResponse:
        game = Games().get(id)
        data = GameSchema().dump(game)
        return Response(data=data)


class GuessesViewset(viewsets.ViewSet):
    def create(self, request: Any, id: int) -> HttpResponse:
        data = GuessSchema().load(request.data)

        game = Games().get(id)
        game.add_guess(data["code"])
        Games().save(game)

        result = GameSchema().dump(game)

        return Response(status=status.HTTP_201_CREATED, data=result)
