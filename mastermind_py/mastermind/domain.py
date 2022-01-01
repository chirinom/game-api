import random
import uuid
from typing import List, Tuple, Optional

from pydash import py_


class Colors:
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    ORANGE = "orange"
    BLACK = "black"
    WHITE = "white"
    PURPLE = "purple"
    TURQUOISE = "turquoise"


colors = [
    Colors.RED,
    Colors.BLUE,
    Colors.GREEN,
    Colors.YELLOW,
    Colors.ORANGE,
    Colors.WHITE,
    Colors.PURPLE,
    Colors.TURQUOISE,
]


class GameStatus:
    RUNNING = "running"
    WON = "won"
    LOST = "lost"


def create_reference() -> str:
    """Generate a default stream name.

    The stream name will be completely random, based on the UUID generator
    passed onto hex format and cutr down to 8 characters. Remeber, UUID4's
    are 32 characters in length, so we cut it
    """
    divider = 3  # Divided by 3 generates 8 characters, by 2, 16 characters
    random_uuid = uuid.uuid4()
    stream_name = random_uuid.hex[: int(len(random_uuid.hex) / divider)]
    return stream_name


class Guess:
    def __init__(self, code: List[str], black_pegs: int, white_pegs: int) -> None:
        self.code = code
        self.black_pegs = black_pegs
        self.white_pegs = white_pegs


class Game:
    def __init__(
        self,
        id: Optional[int],
        reference: str,
        num_slots: int,
        num_colors: int,
        secret_code: List[str],
        max_guesses: int,
        status: str,
        guesses: List[Guess],
    ):
        self.id = id
        self.reference = reference
        self.num_slots = num_slots
        self.num_colors = num_colors
        self.secret_code = secret_code
        self.max_guesses = max_guesses
        self.status = status
        self.colors = py_.take(colors, num_colors)
        self.guesses = guesses

    def add_guess(self, code: List[str]) -> None:
        if self.status != GameStatus.RUNNING:
            raise Exception("Cannot add a new guess, the game is already finished")

        black_pegs, white_pegs = self._feedback(code)
        self.guesses.append(Guess(code, black_pegs, white_pegs))

        if black_pegs == self.num_slots:
            self.status = GameStatus.WON
        elif len(self.guesses) >= self.max_guesses:
            self.status = GameStatus.LOST
        else:
            self.status = GameStatus.RUNNING

    def _feedback(self, code: List[str]) -> Tuple[int, int]:
        zipped_code = zip(code, self.secret_code)
        black_pegs = sum(1 for c, s in zipped_code if c == s)
        code_counts = py_.count_by(code, lambda x: x)
        secret_counts = py_.count_by(self.secret_code, lambda x: x)

        white_pegs = sum(
            min(code_counts.get(c, 0), secret_counts.get(c, 0)) for c in self.colors
        )
        return black_pegs, white_pegs - black_pegs

    @staticmethod
    def new(num_slots: int, num_colors: int, max_guesses: int) -> "Game":
        reference = create_reference().upper()
        chosen_colors = py_.take(colors, num_colors)
        secret_code = random.choices(chosen_colors, k=num_slots)
        return Game(
            None,
            reference,
            num_slots,
            num_colors,
            secret_code,
            max_guesses,
            GameStatus.RUNNING,
            [],
        )
