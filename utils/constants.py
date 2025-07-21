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

# QFPL League IDs - SEASON 2024/25
LEAGUE_IDS = {
    'QFPL_MAIN': 65689,      # Main QFPL League
    'NFO_MINI': 72659,       # NFO Mini League
    # Other mini leagues will be added here
}

# API endpoints
FPL_BASE_URL = "https://fantasy.premierleague.com/api/"
ENDPOINTS = {
    'bootstrap': 'bootstrap-static/',
    'fixtures': 'fixtures/',
    'league': 'leagues-classic/{league_id}/standings/',
    'entry': 'entry/{team_id}/',
    'picks': 'entry/{team_id}/event/{event_id}/picks/',
    'league_h2h': 'leagues-h2h/{league_id}/standings/',
    'transfers': 'entry/{team_id}/transfers/',
}