from mastermind_py.mastermind.domain import Game, Guess
from mastermind_py.mastermind.models import GameModel, GuessModel


class Games:
    def all(self):
        models = GameModel.objects.all()
        return [self._to_domain(model) for model in models]

    def save(self, game):
        model = self._to_model(game)

        model.save()

        GuessModel.objects.filter(game_id=model.id)


        for g in game.guesses:
            GuessModel.objects.create(code=g.code,
                                 black_pegs=g.black_pegs,
                                 white_pegs=g.white_pegs,
                                 game_id=model.id)

        game.id = model.id

    def get(self, id):
        return self._to_domain(GameModel.objects.get(pk=id))

    def _to_domain(self, model):

        guesses = [Guess(g.code, g.black_pegs, g.white_pegs) for g in model.guesses.all()]

        return Game(
            id=model.id,
            reference=model.reference,
            num_colors=model.num_colors,
            num_slots=model.num_slots,
            max_guesses=model.max_guesses,
            status=model.status,
            secret_code=model.secret_code,
            guesses=guesses
        )

    def _to_model(self, game):
        model = GameModel(id=game.id,
                          reference=game.reference,
                          num_colors=game.num_colors,
                          num_slots=game.num_slots,
                          max_guesses=game.max_guesses,
                          status=game.status,
                          secret_code=game.secret_code)

        return model
