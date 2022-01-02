from typing import Any, List

import pytest
from rest_framework.test import APIClient
from rest_framework import status

from mastermind_py.mastermind.domain import Game
from mastermind_py.mastermind.repo import Games
from hamcrest import *


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
class TestMastermindApi:
    @staticmethod
    def create_game(
        num_slots: int,
        num_colors: int,
        max_guesses: int,
        reference: str,
        status: str,
        secret_code: List[str],
    ) -> Game:
        game = Game(
            id=None,
            num_slots=num_slots,
            num_colors=num_colors,
            max_guesses=max_guesses,
            reference=reference,
            status=status,
            secret_code=secret_code,
            guesses=[],
        )

        Games().save(game)
        return game

    def assert_guess(
        self, response: Any, expected_white_peg: int, expected_black_peg: int
    ):
        assert_that(
            response.json()["guesses"][0]["white_pegs"], is_(expected_white_peg)
        )
        assert_that(
            response.json()["guesses"][0]["black_pegs"], is_(expected_black_peg)
        )

    def test_get_games(self, api_client):
        """Check if retrieve all games correctly"""
        self.create_game(
            4,
            4,
            2,
            "MYREF",
            "running",
            ["red", "red", "green", "yellow"],
        )

        response = api_client.get("/api/games/")

        expected_response = {
            "results": contains_exactly(
                has_entries(
                    {
                        "num_colors": 4,
                        "secret_code": ["red", "red", "green", "yellow"],
                        "max_guesses": 2,
                        "reference": "MYREF",
                    }
                )
            )
        }

        assert_that(response.status_code, is_(status.HTTP_200_OK))
        assert_that(response.json(), expected_response)

    def test_get_game(self, api_client):
        """Check if retrieve a game correctly"""
        game = self.create_game(
            4,
            4,
            2,
            "MYREF",
            "running",
            ["red", "red", "green", "yellow"],
        )

        response = api_client.get(f"/api/games/{game.id}/")

        expected_response = has_entries(
            {
                "num_colors": 4,
                "secret_code": ["red", "red", "green", "yellow"],
                "max_guesses": 2,
                "reference": "MYREF",
            }
        )

        assert_that(response.status_code, is_(status.HTTP_200_OK))
        assert_that(response.json(), expected_response)

    def test_create_game(self, api_client):
        """Check if a game is created correctly"""
        response = api_client.post(
            "/api/games/",
            data={"num_slots": 4, "num_colors": 4, "max_guesses": 2},
            format="json",
        )

        expected_response = has_entries(
            {
                "num_colors": 4,
                "max_guesses": 2,
                "status": "running",
            }
        )
        assert_that(response.status_code, is_(status.HTTP_201_CREATED))
        assert_that(response.json(), expected_response)

    def test_create_guess(self, api_client):
        """Check if guess create correctly"""
        game = self.create_game(
            4,
            6,
            2,
            "MYREF",
            "running",
            ["green", "blue", "yellow", "red"],
        )

        api_client.post(
            f"/api/games/{game.id}/guesses/",
            data={"code": ["orange", "orange", "orange", "orange"]},
            format="json",
        )

        response = api_client.get(f"/api/games/{game.id}/")
        expected_response = has_entries(
            {
                "guesses": has_item(
                    {
                        "code": ["orange", "orange", "orange", "orange"],
                        "white_pegs": 0,
                        "black_pegs": 0,
                    }
                )
            }
        )

        assert_that(response.status_code, status.HTTP_201_CREATED)
        assert_that(response.json(), expected_response)

    def test_retrieve_guesses(self, api_client):
        """Check if guesses are retrieved correctly"""
        game = self.create_game(
            4,
            5,
            2,
            "MYREF",
            "running",
            ["green", "blue", "yellow", "red"],
        )

        api_client.post(
            f"/api/games/{game.id}/guesses/",
            data={"code": ["orange", "orange", "orange", "orange"]},
            format="json",
        )
        api_client.post(
            f"/api/games/{game.id}/guesses/",
            data={"code": ["blue", "red", "orange", "orange"]},
            format="json",
        )
        response = api_client.get(f"/api/games/{game.id}/")

        expected_response = has_entries(
            {
                "guesses": contains_exactly(
                    {
                        "code": ["orange", "orange", "orange", "orange"],
                        "white_pegs": 0,
                        "black_pegs": 0,
                    },
                    {
                        "code": ["blue", "red", "orange", "orange"],
                        "white_pegs": 2,
                        "black_pegs": 0,
                    },
                )
            }
        )

        assert_that(response.status_code, status.HTTP_201_CREATED)
        assert_that(response.json(), expected_response)

    @pytest.mark.parametrize(
        "secret_code,guess,white_pegs,black_pegs",
        [
            (
                ["red", "green", "green", "blue"],
                ["red", "green", "green", "blue"],
                0,
                4,
            ),
            (["red", "red", "red", "red"], ["blue", "yellow", "orange", "blue"], 0, 0),
            (["green", "blue", "blue", "red"], ["green", "blue", "red", "blue"], 2, 2),
            (["blue", "blue", "blue", "red"], ["red", "blue", "green", "green"], 1, 1),
            (["red", "blue", "green", "green"], ["blue", "blue", "blue", "red"], 1, 1),
            (["blue", "blue", "blue", "red"], ["blue", "blue", "blue", "red"], 0, 4),
            (
                ["white", "blue", "white", "blue"],
                ["blue", "white", "blue", "white"],
                4,
                0,
            ),
            (
                ["orange", "orange", "orange", "white"],
                ["orange", "white", "white", "white"],
                0,
                2,
            ),
        ],
    )
    def test_one_white_peg(
        self, api_client, secret_code, guess, white_pegs, black_pegs
    ):
        """Check if return one white peg"""
        game = self.create_game(
            4,
            6,
            2,
            "MYREF",
            "running",
            secret_code,
        )

        api_client.post(
            f"/api/games/{game.id}/guesses/",
            data={"code": guess},
            format="json",
        )
        response = api_client.get(f"/api/games/{game.id}/")

        self.assert_guess(response, white_pegs, black_pegs)
