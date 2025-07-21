import requests
import pandas as pd
from utils.constants import FPL_BASE_URL, ENDPOINTS, LEAGUE_IDS
import streamlit as st

class FPLApiClient:
    def __init__(self):
        self.base_url = FPL_BASE_URL
        self.session = requests.Session()
    
    @st.cache_data(ttl=300)  # Cache for 5 minutes
    def get_bootstrap_data(_self):
        """Get main FPL data (players, teams, gameweeks)"""
        url = f"{_self.base_url}{ENDPOINTS['bootstrap']}"
        response = _self.session.get(url)
        return response.json() if response.status_code == 200 else None
    
    @st.cache_data(ttl=300)
    def get_league_standings(_self, league_id):
        """Get league standings"""
        url = f"{_self.base_url}{ENDPOINTS['league'].format(league_id=league_id)}"
        response = _self.session.get(url)
        return response.json() if response.status_code == 200 else None
    
    @st.cache_data(ttl=60)  # Cache for 1 minute for live data
    def get_team_picks(_self, team_id, gameweek):
        """Get team's picks for a specific gameweek"""
        url = f"{_self.base_url}{ENDPOINTS['picks'].format(team_id=team_id, event_id=gameweek)}"
        response = _self.session.get(url)
        return response.json() if response.status_code == 200 else None
    
    def get_nfo_mini_league(_self):
        """Get NFO Mini League standings"""
        return _self.get_league_standings(LEAGUE_IDS['NFO_MINI'])
    
    def get_qfpl_main_league(_self):
        """Get Main QFPL League standings"""
        return _self.get_league_standings(LEAGUE_IDS['QFPL_MAIN'])
    
    def get_current_gameweek(_self):
        """Get current gameweek number"""
        data = _self.get_bootstrap_data()
        if data:
            events = data['events']
            for event in events:
                if event['is_current']:
                    return event['id']
        return 1