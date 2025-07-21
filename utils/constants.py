# Team mappings
TEAMS = {
    'NFO': 'Nottingham Forest',
    'LIV': 'Liverpool', 
    'MCI': 'Manchester City',
    'ARS': 'Arsenal',
    # Add all 20 teams...
}

TEAM_COLORS = {
    'NFO': '#DD0000',
    'LIV': '#C8102E',
    'MCI': '#6CABDD',
    'ARS': '#EF0107',
    # Add all team colors...
}

# API endpoints
FPL_BASE_URL = "https://fantasy.premierleague.com/api/"
ENDPOINTS = {
    'bootstrap': 'bootstrap-static/',
    'fixtures': 'fixtures/',
    'league': 'leagues-classic/{league_id}/standings/',
    'entry': 'entry/{team_id}/',
    'picks': 'entry/{team_id}/event/{event_id}/picks/',
}