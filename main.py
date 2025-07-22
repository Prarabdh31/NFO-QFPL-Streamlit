import streamlit as st
import pandas as pd
from utils.constants import TEAMS, TEAM_COLORS
from utils.fpl_api import FPLApiClient
import os

# Page config
st.set_page_config(
    page_title="NFO QFPL Dashboard - Home",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load centralized CSS
css_file = 'assets/styles/style.css'
if os.path.exists(css_file):
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.markdown('<div class="nfo-main-header"><h1>🏠 NFO QFPL Dashboard - Home</h1></div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar Navigation
    with st.sidebar:
        st.header("🏆 QFPL Navigation")
        st.info("Navigate through different dashboard views")
        
        st.markdown("### 📊 Dashboard Pages")
        st.page_link("main.py", label="🏠 Home", icon="🏠")
        st.page_link("pages/1_🏠_NFO_Dashboard.py", label="🌲 NFO Dashboard", icon="🌲")
        st.page_link("pages/2_📊_QFPL_Dashboard.py", label="🏆 QFPL Dashboard", icon="🏆")
        st.page_link("pages/3_⚡_GW_Live.py", label="⚡ GW Live", icon="⚡")
        st.page_link("pages/4_🧠_Intelligence.py", label="🧠 Intelligence", icon="🧠")
        
        st.markdown("---")
        st.caption("📱 Mobile optimized")
        st.caption("🖥️ Desktop ready")
    
    # Home page content
    st.markdown("## Welcome to NFO QFPL Command Center")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.header("🌲 NFO Dashboard")
        st.info("Deep dive into NFO team performance, squad analysis, and mini-league standings.")
        if st.button("Go to NFO Dashboard", use_container_width=True):
            st.switch_page("pages/1_🏠_NFO_Dashboard.py")
        
    with col2:
        st.header("🏆 QFPL Dashboard")
        st.info("Overview of the main QFPL league with all 20 teams, fixtures, and cross-team analysis.")
        if st.button("Go to QFPL Dashboard", use_container_width=True):
            st.switch_page("pages/2_📊_QFPL_Dashboard.py")
        
    with col3:
        st.header("⚡ GW Live")
        st.info("Real-time gameweek tracking, live scores, and match-by-match analysis.")
        if st.button("Go to GW Live", use_container_width=True):
            st.switch_page("pages/3_⚡_GW_Live.py")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("🧠 Intelligence")
        st.info("Advanced analytics, transfer intelligence, squad comparisons, and strategic insights.")
        if st.button("Go to Intelligence", use_container_width=True):
            st.switch_page("pages/4_🧠_Intelligence.py")
    
    with col2:
        st.header("📈 Quick Stats")
        st.metric("Current Gameweek", "GW 1")
        st.metric("NFO Squad Size", "6/11")
        st.metric("Season Status", "Pre-season")
    
    st.markdown("---")
    st.markdown("### 🎯 Features Overview")
    
    features_col1, features_col2 = st.columns(2)
    
    with features_col1:
        st.markdown("""
        **📊 Analytics Features:**
        - Real-time squad analysis
        - Transfer intelligence tracking
        - Head-to-head comparisons
        - Popular picks analysis
        - Fixture difficulty ratings
        """)
    
    with features_col2:
        st.markdown("""
        **⚡ Live Features:**
        - Live gameweek scoring
        - Real-time league standings
        - Match-by-match tracking
        - Performance alerts
        - Captain choice analysis
        """)
    
    st.markdown("---")
    st.markdown("**🚀 Ready to explore the most comprehensive QFPL analytics platform!**")

if __name__ == "__main__":
    main()