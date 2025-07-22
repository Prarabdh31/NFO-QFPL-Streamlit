import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os

# Import our utilities
from utils.fpl_api import FPLApiClient
from utils.constants import LEAGUE_IDS, TEAM_COLORS

# Page config
st.set_page_config(
    page_title="GW Live | QFPL Analytics",
    page_icon="⚡",
    layout="wide"
)

# Load centralized CSS
css_file = 'assets/styles/style.css'
if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize API client
@st.cache_resource
def get_api_client():
    return FPLApiClient()

api = get_api_client()

def main():
    # Sidebar Navigation
    with st.sidebar:
        st.markdown("### ⚡ GW Live")
        st.success("Real-time Tracking")
        
        st.markdown("### 📊 Navigation")
        st.page_link("main.py", label="🏠 Home", icon="🏠")
        st.page_link("pages/1_🏠_NFO_Dashboard.py", label="🌲 NFO Dashboard", icon="🌲")
        st.page_link("pages/2_📊_QFPL_Dashboard.py", label="🏆 QFPL Dashboard", icon="🏆")
        st.page_link("pages/3_⚡_GW_Live.py", label="⚡ GW Live", icon="⚡")
        st.page_link("pages/4_🧠_Intelligence.py", label="🧠 Intelligence", icon="🧠")
        
        # Auto-refresh option
        auto_refresh = st.checkbox("🔄 Auto-refresh (30s)", value=False)
        
        if st.button("🔄 Refresh Now", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.caption("⚡ Live Updates")
    
    # Auto-refresh functionality
    if auto_refresh:
        st.rerun()
    
    # Main header
    st.markdown('<div class="nfo-main-header"><h1>⚡ Gameweek Live Tracking</h1></div>', unsafe_allow_html=True)
    
    # Live status indicators
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("⚡ Current GW", "GW 1")
    with col2:
        st.metric("🕐 Status", "Pre-season")
    with col3:
        st.metric("⚽ Matches", "0/10")
    with col4:
        st.metric("🔴 Live Now", "0")
    with col5:
        st.metric("🏁 Completed", "0")
    
    st.markdown("---")
    
    # Check if gameweek is live
    is_live = False  # Will be dynamic based on API data
    
    if not is_live:
        # Pre-season or between gameweeks
        st.info("🚧 **Gameweek Not Active** \n\nLive tracking will be available during active gameweeks. Currently in pre-season mode.")
        
        # Preview of live features
        tab1, tab2, tab3 = st.tabs(["🎯 Live Features Preview", "📊 NFO Live Board", "⚽ Match Center"])
        
        with tab1:
            st.subheader("⚡ What's Coming Live")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**🔴 Real-time Features:**")
                st.markdown("""
                - Live scoring as goals happen
                - Real-time league position updates
                - NFO vs NFO live comparisons
                - Captain performance tracking
                - Bonus points updates
                - Player substitution alerts
                """)
            
            with col2:
                st.write("**📊 Live Analytics:**")
                st.markdown("""
                - Live rank changes
                - Points per minute tracking
                - Best/worst performers
                - Transfer impact analysis
                - Captain choice effectiveness
                - Live mini-league standings
                """)
        
        with tab2:
            st.subheader("📊 NFO Live Leaderboard (Preview)")
            
            # Sample NFO live data
            preview_data = {
                "Player": ["Jay Bansal", "Prarabdh Chaturvedi", "Shiromi Chaturvedi", "Shubham Choudhary", "Ankur Goyal", "Arun Goyal"],
                "Team": ["Bansal11", "Xithan XI", "Pretty Panda Prince", "Fairdevil", "TBD", "arun goyal"],
                "Live Points": ["-", "-", "-", "-", "-", "-"],
                "Captain": ["TBD", "TBD", "TBD", "TBD", "TBD", "TBD"],
                "Rank": ["TBD", "TBD", "TBD", "TBD", "TBD", "TBD"]
            }
            
            df_preview = pd.DataFrame(preview_data)
            st.dataframe(df_preview, use_container_width=True, hide_index=True)
            
            st.caption("📊 Live points and rankings will update automatically during gameweeks")
        
        with tab3:
            st.subheader("⚽ Match Center (Preview)")
            
            # Sample fixture list
            st.write("**📅 Upcoming Fixtures (GW1)**")
            
            fixtures_data = {
                "Match": ["Arsenal vs Wolves", "Everton vs Brighton", "Newcastle vs Southampton", "Nottingham Forest vs Bournemouth"],
                "Date": ["Aug 17", "Aug 17", "Aug 17", "Aug 17"],
                "Time": ["15:00", "15:00", "15:00", "15:00"],
                "Status": ["Scheduled", "Scheduled", "Scheduled", "Scheduled"]
            }
            
            df_fixtures = pd.DataFrame(fixtures_data)
            st.dataframe(df_fixtures, use_container_width=True, hide_index=True)
            
            st.info("🔴 **During Live Gameweeks:**\n\nThis section will show live scores, goal scorers, and FPL points as they happen!")
    
    else:
        # Live gameweek mode (future implementation)
        st.success("🔴 **LIVE GAMEWEEK IN PROGRESS**")
        
        # Live tracking tabs
        tab1, tab2, tab3, tab4 = st.tabs(["🔴 Live Scores", "📊 NFO Live", "🏆 QFPL Live", "⚽ Match Center"])
        
        with tab1:
            st.subheader("🔴 Live FPL Scoring")
            # Real-time scoring implementation will go here
            
        with tab2:
            st.subheader("📊 NFO Live Leaderboard")
            # NFO live tracking implementation will go here
            
        with tab3:
            st.subheader("🏆 QFPL Live Standings")
            # QFPL live tracking implementation will go here
            
        with tab4:
            st.subheader("⚽ Live Match Center")
            # Live match updates implementation will go here
    
    st.markdown("---")
    
    # Footer with live update info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption(f"📡 Last updated: {datetime.now().strftime('%H:%M:%S')}")
    with col2:
        if auto_refresh:
            st.caption("🔄 Auto-refreshing every 30 seconds")
        else:
            st.caption("🔄 Manual refresh mode")
    with col3:
        st.caption("⚡ Live features ready for GW1")

if __name__ == "__main__":
    main()