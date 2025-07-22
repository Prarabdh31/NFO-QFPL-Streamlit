import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import os

# Import our utilities
from utils.fpl_api import FPLApiClient
from utils.constants import LEAGUE_IDS, TEAM_COLORS

# Page config
st.set_page_config(
    page_title="QFPL Dashboard | QFPL Analytics",
    page_icon="🏆",
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
        st.markdown("### 🏆 QFPL Dashboard")
        st.success("Main League Analytics")
        
        st.markdown("### 📊 Navigation")
        st.page_link("main.py", label="🏠 Home", icon="🏠")
        st.page_link("pages/1_🏠_NFO_Dashboard.py", label="🌲 NFO Dashboard", icon="🌲")
        st.page_link("pages/2_📊_QFPL_Dashboard.py", label="🏆 QFPL Dashboard", icon="🏆")
        st.page_link("pages/3_⚡_GW_Live.py", label="⚡ GW Live", icon="⚡")
        st.page_link("pages/4_🧠_Intelligence.py", label="🧠 Intelligence", icon="🧠")
        
        # Refresh button
        if st.button("🔄 Refresh Data", help="Get latest QFPL data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.markdown("---")
        st.caption("📊 QFPL Analytics")
    
    # Main header
    st.markdown('<div class="nfo-main-header"><h1>🏆 QFPL Main League Dashboard</h1></div>', unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("🏆 Season", "Season 10")
    with col2:
        st.metric("👥 Total Teams", "20")
    with col3:
        st.metric("⚡ Current GW", "GW 1")
    with col4:
        st.metric("📊 Status", "Pre-season")
    with col5:
        st.metric("🎮 League ID", "65689")
    
    st.markdown("---")
    
    # Main content areas
    tab1, tab2, tab3 = st.tabs(["📊 League Overview", "⚔️ Team Analysis", "📈 Performance Trends"])
    
    with tab1:
        st.subheader("🏆 QFPL Main League Overview")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.info("🚧 **Coming Soon!** \n\nFull league standings and team analysis will be available once the season starts. Currently showing pre-season data.")
            
            # Placeholder for league table
            st.write("**📋 League Standings (Preview)**")
            placeholder_data = {
                "Rank": ["1st", "2nd", "3rd", "...", "20th"],
                "Team": ["NFO", "LIV", "MCI", "...", "Team 20"],
                "Players": ["11", "11", "11", "...", "11"],
                "Total Points": ["-", "-", "-", "...", "-"],
                "Status": ["Ready", "Ready", "Ready", "...", "Joining"]
            }
            df = pd.DataFrame(placeholder_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        with col2:
            st.write("**🎯 League Statistics**")
            st.metric("Teams Ready", "15/20")
            st.metric("Total Players", "180+")
            st.metric("Season Format", "H2H + Classic")
            
            st.write("**📈 Progress**")
            progress = 75  # 15/20 teams ready
            st.progress(progress/100)
            st.caption(f"{progress}% teams ready for season start")
    
    with tab2:
        st.subheader("⚔️ Team Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🌲 NFO Team Status**")
            st.success("✅ Squad: 6/11 players joined")
            st.info("📊 League Position: TBD")
            st.warning("⚠️ Status: Needs 5 more players")
        
        with col2:
            st.write("**🏆 Other Mini-Leagues**")
            st.info("📋 **Coming Soon!**\n\nAnalysis of all 20 team mini-leagues will be available here.")
    
    with tab3:
        st.subheader("📈 Performance Trends")
        st.info("🚧 **Season Not Started**\n\nPerformance analytics and trends will be available once gameweeks begin.")
        
        # Placeholder chart
        st.write("**📊 Preview: Team Performance Chart**")
        
        # Sample data for visualization preview
        sample_data = pd.DataFrame({
            'Gameweek': [f"GW{i}" for i in range(1, 11)],
            'NFO': np.random.randint(50, 80, 10),
            'Average': np.random.randint(45, 75, 10)
        })
        
        fig = px.line(sample_data, x='Gameweek', y=['NFO', 'Average'], 
                     title="Team Performance Over Time (Preview)",
                     color_discrete_map={'NFO': '#DD0000', 'Average': '#888888'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption("📊 This is a preview chart. Real data will appear when the season starts.")
    
    # Footer
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.caption(f"📡 Last updated: {datetime.now().strftime('%H:%M:%S')}")
    with col2:
        st.caption(f"🔗 QFPL League ID: {LEAGUE_IDS['QFPL_MAIN']}")

if __name__ == "__main__":
    main()