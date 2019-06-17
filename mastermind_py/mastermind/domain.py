import random
import uuid

from pydash import py_


class Colors:
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'
    YELLOW = 'yellow'
    ORANGE = 'orange'
    BLACK = 'black'
    WHITE = 'white'
    PURPLE = 'purple'
    TURQUOISE = 'turquoise'


colors = [Colors.RED, Colors.BLUE, Colors.GREEN, Colors.YELLOW, Colors.ORANGE,
          Colors.WHITE, Colors.PURPLE, Colors.TURQUOISE]


class GameStatus:
    RUNNING = 'running'
    WON = 'won'
    LOST = 'lost'


def create_reference():
    """Generate a default stream name.

    The stream name will be completely random, based on the UUID generator
    passed onto hex format and cutr down to 8 characters. Remeber, UUID4's
    are 32 characters in length, so we cut it
    """
    divider = 3  # Divided by 3 generates 8 characters, by 2, 16 characters
    random_uuid = uuid.uuid4()
    stream_name = random_uuid.hex[:int(len(random_uuid.hex) / divider)]
    return stream_name


class Guess:
    def __init__(self, code, black_pegs, white_pegs):
        self.code = code
        self.black_pegs = black_pegs
        self.white_pegs = white_pegs


class Game:
    def __init__(self, id, reference, num_slots, num_colors,
                 secret_code, max_guesses,
                 status, guesses):
        self.id = id
        self.reference = reference
        self.num_slots = num_slots
        self.num_colors = num_colors
        self.secret_code = secret_code
        self.max_guesses = max_guesses
        self.status = status
        self.colors = py_.take(colors, num_colors)
        self.guesses = guesses

    def add_guess(self, code):
        if self.status != GameStatus.RUNNING:
            raise Exception('Cannot add a new guess, the game is already finished')

        black_pegs, white_pegs = self._feedback(code)
        self.guesses.append(Guess(code, black_pegs, white_pegs))

        if black_pegs == self.num_slots:
            self.status = GameStatus.WON
        elif len(self.guesses) >= self.max_guesses:
            self.status = GameStatus.LOST
        else:
            self.status = GameStatus.RUNNING

    def _feedback(self, code):
        return 4, 0

    @staticmethod
    def new(num_slots, num_colors, max_guesses):
        reference = create_reference().upper()
        chosen_colors = py_.take(colors, num_colors)
        secret_code = random.choices(chosen_colors, k=num_slots)
        return Game(None, reference, num_slots, num_colors,
                    secret_code, max_guesses, GameStatus.RUNNING,
                    [])
