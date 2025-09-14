"""
Winwood Branding and Styling
===========================
Company branding and styling components.
"""

import streamlit as st


def render_winwood_footer():
    """Render Winwood company footer."""
    st.markdown("---")
    
    # Company footer
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(
            """
            <div style='text-align: center; color: #666; font-size: 0.9em;'>
                <p><strong>🏢 Winwood Business Research Tool</strong></p>
                <p>Powered by Winwood Technology Solutions</p>
                <p><em>Advanced Business Intelligence & Data Analytics</em></p>
            </div>
            """,
            unsafe_allow_html=True
        )


def apply_winwood_theme():
    """Apply Winwood theme styling."""
    st.markdown(
        """
        <style>
        .main {
            padding-top: 1rem;
        }
        .stButton > button {
            width: 100%;
            border-radius: 5px;
            border: 1px solid #ddd;
            padding: 0.5rem 1rem;
            font-weight: 500;
        }
        .stButton > button:hover {
            background-color: #f0f2f6;
            border-color: #1f77b4;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def render_winwood_header():
    """Render Winwood branded header."""
    st.markdown(
        """
        <div style='text-align: center; padding: 1rem 0; background: linear-gradient(90deg, #1f77b4, #ff7f0e); color: white; border-radius: 10px; margin-bottom: 2rem;'>
            <h1 style='margin: 0; font-size: 2rem;'>🏢 Winwood Business Research Tool</h1>
            <p style='margin: 0; font-size: 1.1rem;'>Advanced Business Intelligence & Data Analytics</p>
        </div>
        """,
        unsafe_allow_html=True
    )