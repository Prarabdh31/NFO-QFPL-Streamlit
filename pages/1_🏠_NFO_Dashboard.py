import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
from datetime import datetime
from pathlib import Path
import numpy as np
import os

# Import our utilities
from utils.fpl_api import FPLApiClient
from utils.constants import LEAGUE_IDS, TEAM_COLORS

# Page config
st.set_page_config(
    page_title="NFO Dashboard | QFPL",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load centralized CSS (force UTF‑8, drop any undecodable bytes)
css_path = Path('assets/styles/style.css')
if css_path.exists():
    css = css_path.read_text(encoding='utf-8', errors='ignore')
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# Initialize API client
@st.cache_resource
def get_api_client():
    return FPLApiClient()

api = get_api_client()

def load_nfo_data():
    """Load all NFO-related data"""
    try:
        # Get current gameweek
        bootstrap_data = api.get_bootstrap_data()
        current_gw = api.get_current_gameweek() if bootstrap_data else 1
        
        # Get NFO Mini League
        nfo_league = api.get_nfo_mini_league()
        
        # Get Main QFPL League  
        main_league = api.get_qfpl_main_league()
        
        return {
            'current_gw': current_gw,
            'nfo_league': nfo_league,
            'main_league': main_league,
            'bootstrap': bootstrap_data
        }
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def display_header_metrics(data):
    """Display key metrics in the header - using centralized styles"""
    st.markdown('<div class="nfo-main-header"><h1>🏠 Nottingham Forest FC - QFPL Command Center</h1></div>', unsafe_allow_html=True)
    
    if not data or not data['nfo_league']:
        st.warning("Unable to load league data. Please check API connection.")
        return
    
    # Extract NFO league stats
    nfo_standings = data['nfo_league']['standings']['results'] if data['nfo_league'] else []
    new_entries = data['nfo_league'].get('new_entries', {}).get('results', []) if data['nfo_league'] else []
    
    # Use new_entries if no standings yet
    if not nfo_standings and new_entries:
        nfo_total_players = len(new_entries)
        min_players_needed = 11
        squad_ready = nfo_total_players >= min_players_needed
        avg_total_points = avg_gw_points = top_score_this_gw = 0
        status = "pre_season"
    else:
        nfo_total_players = len(nfo_standings)
        min_players_needed = 11
        squad_ready = nfo_total_players >= min_players_needed
        status = "active"
        
        # Calculate team averages
        if nfo_standings:
            avg_total_points = np.mean([team['total'] for team in nfo_standings])
            avg_gw_points = np.mean([team['event_total'] for team in nfo_standings])
            top_score_this_gw = max([team['event_total'] for team in nfo_standings])
        else:
            avg_total_points = avg_gw_points = top_score_this_gw = 0
    
    # Display metrics in responsive grid
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    
    with col1:
        st.metric(
            label="🏆 Gameweek",
            value=f"GW {data['current_gw']}",
            help="Current Fantasy Premier League gameweek"
        )
    
    with col2:
        if status == "pre_season":
            st.metric(
                label="👥 Squad",
                value=f"{nfo_total_players}/11",
                help="Current players joined / Minimum needed for complete squad"
            )
        else:
            st.metric(
                label="👥 Squad",
                value=str(nfo_total_players),
                help="Total players in NFO Mini League"
            )
    
    with col3:
        if status == "pre_season":
            st.metric(
                label="📊 Status",
                value="Pre-season",
                help="Season hasn't started yet"
            )
        else:
            st.metric(
                label="📊 Avg Total",
                value=f"{avg_total_points:.0f}",
                help="Average total points across all NFO players"
            )
    
    with col4:
        if status == "pre_season":
            st.metric(
                label="⚡ GW Status",
                value="Pending",
                help="Waiting for gameweek to start"
            )
        else:
            st.metric(
                label="⚡ Avg GW",
                value=f"{avg_gw_points:.0f}",
                help="Average gameweek points for NFO team"
            )
    
    with col5:
        if status == "pre_season":
            if squad_ready:
                st.metric(
                    label="🔥 Status",
                    value="Ready",
                    help="Squad is complete and ready!"
                )
            else:
                players_needed = min_players_needed - nfo_total_players
                st.metric(
                    label="🔥 Status",
                    value=f"Need {players_needed}",
                    help=f"Need {players_needed} more players to complete squad"
                )
        else:
            st.metric(
                label="🔥 Top GW",
                value=f"{top_score_this_gw}",
                help="Highest NFO score this gameweek"
            )

def display_nfo_mini_league(data):
    """Display NFO Mini League standings - using centralized styles"""
    st.subheader("🏆 NFO Mini League")
    
    if not data or not data['nfo_league']:
        st.warning("NFO Mini League data not available")
        return
    
    standings = data['nfo_league']['standings']['results']
    new_entries = data['nfo_league'].get('new_entries', {}).get('results', [])
    
    if not standings and new_entries:
        st.info("🎯 Season hasn't started yet, but players are joining! Here are the NFO squad members:")
        
        # Show new entries in a responsive format
        entries_data = []
        for i, player in enumerate(new_entries, 1):
            entries_data.append({
                '#': f"{i}",
                'Team': player['entry_name'],
                'Manager': f"{player['player_first_name']} {player['player_last_name']}",
                'Joined': player['joined_time'][:10],
                'ID': player['entry']
            })
        
        df = pd.DataFrame(entries_data)
        
        # Use container to make table responsive without scrollbars
        st.dataframe(
            df, 
            use_container_width=True, 
            hide_index=True
        )
        
        # Show squad status
        current_players = len(new_entries)
        min_players = 11
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if current_players >= min_players:
                st.success(f"👥 Squad Complete: {current_players}/11 players")
            else:
                st.warning(f"👥 Squad Building: {current_players}/11 players joined")
        with col2:
            st.info(f"⏱️ Awaiting Season Start")
        with col3:
            st.info(f"🆔 League: {LEAGUE_IDS['NFO_MINI']}")
        
        return
    
    if not standings:
        st.info("No standings data available yet. Season may not have started!")
        return
    
    # If we have standings, show them in full responsive format
    standings_data = []
    for i, team in enumerate(standings, 1):
        standings_data.append({
            'Rank': i,
            'Team': team['entry_name'],
            'Manager': team['player_name'],
            'Total': team['total'],
            'GW': team['event_total'],
            'ID': team['entry']
        })
    
    df = pd.DataFrame(standings_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.success(f"🥇 **Leader:** {standings[0]['entry_name']}")
    with col2:
        gw_leader = max(standings, key=lambda x: x['event_total'])
        st.info(f"⚡ **GW Leader:** {gw_leader['entry_name']}")
    with col3:
        total_points = sum(team['total'] for team in standings)
        st.info(f"🎯 **Total:** {total_points:,}")

def display_main_league_position(data):
    """Show NFO's position in main QFPL league - using centralized styles"""
    st.subheader("🌟 Main QFPL League")
    
    if not data or not data['main_league']:
        st.warning("Main QFPL League data not available")
        return
    
    main_standings = data['main_league']['standings']['results']
    nfo_teams = [team for team in main_standings if 'NFO' in team['entry_name'].upper() or 'FOREST' in team['entry_name'].upper()]
    
    if nfo_teams:
        st.success(f"Found {len(nfo_teams)} NFO representatives in main league!")
        
        for team in nfo_teams:
            # Responsive team display
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Rank", f"#{team['rank']}")
                st.metric("Total", team['total'])
            with col2:
                st.metric("Team", team['entry_name'][:20] + "..." if len(team['entry_name']) > 20 else team['entry_name'])
                st.metric("GW", team['event_total'])
    else:
        st.info("NFO teams not yet identified in main league standings. They may be using different team names.")

def display_performance_charts(data):
    """Display performance visualization charts - using centralized styles"""
    if not data or not data['nfo_league']:
        return
    
    standings = data['nfo_league']['standings']['results']
    new_entries = data['nfo_league'].get('new_entries', {}).get('results', [])
    
    st.subheader("📈 Performance Analytics")
    
    if not standings and new_entries:
        # Pre-season analytics
        st.info("🚧 Performance analytics will be available once the season starts!")
        
        # Show team preparation status
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🎯 Squad Readiness**")
            current_players = len(new_entries)
            min_players = 11
            progress_value = min(current_players / min_players, 1.0)
            st.progress(progress_value)
            if current_players >= min_players:
                st.success(f"Squad complete! {current_players}/11 players joined.")
            else:
                st.warning(f"Need {min_players - current_players} more players. Currently {current_players}/11.")
        
        with col2:
            st.write("**📅 Join Timeline**")
            join_dates = [entry['joined_time'][:10] for entry in new_entries]
            unique_dates = list(set(join_dates))
            st.write(f"Players joined on {len(unique_dates)} day(s)")
            st.caption(f"Latest join: {max(join_dates)}")
        
        return
    
    if not standings:
        return
    
    # Create responsive tabs for different charts
    tab1, tab2 = st.tabs(["📊 Points Analysis", "🏃‍♂️ Team Stats"])
    
    with tab1:
        # Points distribution - responsive charts
        points_data = [team['total'] for team in standings]
        gw_points_data = [team['event_total'] for team in standings]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.histogram(
                x=points_data, 
                title="Season Total Points",
                color_discrete_sequence=['#DD0000']
            )
            fig1.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                font=dict(size=10)
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.histogram(
                x=gw_points_data, 
                title="Current GW Points",
                color_discrete_sequence=['#FF6B6B']
            )
            fig2.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=40, b=20),
                font=dict(size=10)
            )
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        # Team comparison
        sorted_teams = sorted(standings, key=lambda x: x['total'], reverse=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🔥 Top Performers**")
            for i, team in enumerate(sorted_teams[:3], 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
                st.write(f"{medal} {team['entry_name'][:15]}... - {team['total']} pts")
        
        with col2:
            st.write("**📊 Quick Stats**")
            total_points = sum(team['total'] for team in standings)
            avg_points = total_points / len(standings) if standings else 0
            st.metric("Team Average", f"{avg_points:.0f}")
            st.metric("Total Combined", f"{total_points:,}")

def main():
    # Sidebar with clean design
    with st.sidebar:
        st.markdown("### 🏠 NFO Dashboard")
        st.success("Dashboard Active")
        
        # Compact refresh button
        if st.button("🔄 Refresh", help="Get latest data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.caption("📱 Mobile optimized")
        st.caption("🖥️ Desktop ready")
    
    # Load data with spinner
    with st.spinner("Loading NFO data..."):
        data = load_nfo_data()
    
    if data:
        # Display all sections with responsive layout
        display_header_metrics(data)
        
        st.markdown("---")
        
        # Responsive two-column layout
        col1, col2 = st.columns([3, 2])
        
        with col1:
            display_nfo_mini_league(data)
        
        with col2:
            display_main_league_position(data)
        
        st.markdown("---")
        
        display_performance_charts(data)
        
        # Responsive footer
        st.markdown("---")
        
        footer_col1, footer_col2 = st.columns(2)
        with footer_col1:
            st.caption(f"📡 Last updated: {datetime.now().strftime('%H:%M:%S')}")
        with footer_col2:
            st.caption(f"🔗 NFO League: {LEAGUE_IDS['NFO_MINI']}")
    
    else:
        st.error("Failed to load dashboard data. Please try refreshing.")
        
        # Debug info in responsive expander
        with st.expander("🔧 Debug Info"):
            debug_col1, debug_col2 = st.columns(2)
            with debug_col1:
                st.code(f"NFO Mini: {LEAGUE_IDS['NFO_MINI']}")
            with debug_col2:
                st.code(f"QFPL Main: {LEAGUE_IDS['QFPL_MAIN']}")

if __name__ == "__main__":
    main()