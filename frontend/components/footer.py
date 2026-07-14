"""
Footer component.
"""


import streamlit as st


def render_footer():
    """
    Render the application footer.
    """

    st.markdown("---")

    st.caption(
        "**DebugGPT** — Version 1.0 — MCA AI/ML Project  \n"
        "Built using: • Streamlit • FastAPI • ChromaDB • Mistral 7B"
    )