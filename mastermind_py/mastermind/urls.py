from django.urls import path

from mastermind_py.mastermind.views import MastermindViewset, GuessesViewset

app_name = "users"
urlpatterns = [
    path("", view=MastermindViewset.as_view({'get': 'list', 'post': 'create'}), name="games"),
    path("<int:id>/", view=MastermindViewset.as_view({'get': 'retrieve'}), name="games"),
    path("<int:id>/guess", view=GuessesViewset.as_view({'post': 'create'}), name='guesses')
]
