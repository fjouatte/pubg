from django.shortcuts import render
from django.http import HttpResponse
import requests
from pubg_stats.models import Player, Season

def get_all_seasons(shards='pc-eu'):
    seasons = []
    response = requests.get(
        Season.get_full_url("shards/{}/seasons".format(shards)), headers=Season.get_headers()
    ).json()
    data = response.get('data', False)
    if not data:
        return False
    for season in data:
        seasons.append(dict(id=season.get('id'), is_current_season=season.get('attributes').get('isCurrentSeason')))
    return seasons

def index(request):
    seasons = get_all_seasons()
    players = Player.get_players_from_api(name='Heart90')
    import pdb
    pdb.set_trace()
    matches = response['data'][0]['relationships']['matches']['data']
    response = requests.get(
        'https://api.playbattlegrounds.com/shards/pc-eu/matches/{}'.format(matches[0]['id']),
        headers=get_headers()
    )
    data = response.json()
    count = 0
    for match in data.get('included'):
        count += 1
    return HttpResponse("You played {} match(es) during this season".format(count))
