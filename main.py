import streamlit as st
import pandas as pd
from utils.constants import TEAMS, TEAM_COLORS
from utils.fpl_api import FPLApiClient
import os

# Page config
st.set_page_config(
    page_title="NFO QFPL Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load centralized CSS
css_file = 'assets/styles/style.css'
if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.markdown('<div class="nfo-main-header"><h1>⚽ NFO QFPL Dashboard</h1></div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("🏆 QFPL Central")
        st.info("Dashboard & Analytics for NFO Team")
        
        # Quick stats placeholder
        st.metric("Current Gameweek", "12")
        st.metric("NFO Team Rank", "3rd")
        st.metric("Points This Week", "78")
    
    # Main content
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.header("📊 Team Overview")
        st.info("Team performance metrics and standings")
        
    with col2:
        st.header("⚔️ Upcoming Fixtures")
        st.info("Next gameweek predictions and analysis")
        
    with col3:
        st.header("🔥 Hot Topics")
        st.info("Transfer insights and trending players")
    
    st.markdown("---")
    st.markdown("**Navigate using the sidebar to explore different analytics views!**")

if __name__ == "__main__":
    main()