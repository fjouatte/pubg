from django.db import models
import requests

BASE_URL = "https://api.playbattlegrounds.com/{}"


class BasePubgModel(models.Model):

    id = models.CharField(primary_key=True, max_length=128)

    @classmethod
    def get_full_url(cls, url):
        return BASE_URL.format(url)

    @classmethod
    def get_headers(cls):
        return dict(
            Authorization="Bearer {}".format(API_KEY),
            Accept="application/vnd.api+json",
        )

    def cached(function):
        def use_cached_or_not(*args, **kwargs):
            import pdb
            pdb.set_trace()
            return function(*args, **kwargs)
        return use_cached_or_not


class Player(BasePubgModel):

    name = models.CharField(max_length=128)

    @classmethod
    @BasePubgModel.cached
    def get_players_from_api(cls, shards='pc-eu', name=False):
        import pdb
        pdb.set_trace()
        players = []
        players_url = "shards/{}/players"
        if name:
            players_url = players_url+"?filter[playerNames]={}".format(name)
        response = requests.get(
            cls.get_full_url(players_url.format(shards)), headers=cls.get_headers()
        ).json()
        data = response.get('data', False)
        if not data:
            return False
        for player in data:
            players.append(dict(id=player.get('id'), name=player.get('attributes').get('name')))
        return players

class Season(BasePubgModel):

    name = models.CharField(max_length=128)
    is_current = models.BooleanField(default=False)


class Update(models.Model):

    last_update = models.DateTimeField()
