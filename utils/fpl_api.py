import requests
import pandas as pd
from utils.constants import FPL_BASE_URL, ENDPOINTS

class FPLApiClient:
    def __init__(self):
        self.base_url = FPL_BASE_URL
        self.session = requests.Session()
    
    def get_bootstrap_data(self):
        """Get main FPL data (players, teams, gameweeks)"""
        url = f"{self.base_url}{ENDPOINTS['bootstrap']}"
        response = self.session.get(url)
        return response.json() if response.status_code == 200 else None
    
    def get_league_standings(self, league_id):
        """Get league standings"""
        url = f"{self.base_url}{ENDPOINTS['league'].format(league_id=league_id)}"
        response = self.session.get(url)
        return response.json() if response.status_code == 200 else None
    
    def get_team_picks(self, team_id, gameweek):
        """Get team's picks for a specific gameweek"""
        url = f"{self.base_url}{ENDPOINTS['picks'].format(team_id=team_id, event_id=gameweek)}"
        response = self.session.get(url)
        return response.json() if response.status_code == 200 else None