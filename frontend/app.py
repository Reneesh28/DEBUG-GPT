"""
frontend/app.py

Main entry point for the DebugGPT Streamlit application.
"""

import streamlit as st

from api_client import (
    analyze,
    debug,
    explain,
    optimize,
    health,
    APIClientError,
)
from components.sidebar import render_sidebar
from components.workspace import render_workspace
from components.footer import render_footer
from components.results import render_results


st.set_page_config(
    page_title="DebugGPT",
    page_icon="🐞",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🐞 DebugGPT")
st.caption("AI-Powered Code Error Explanation & Debugging Assistant")

st.divider()

try:
    health()
    st.sidebar.success("🟢 Backend Connected")
except APIClientError:
    st.sidebar.error("🔴 Backend Offline")

sidebar_data = render_sidebar()

workspace_data = render_workspace(sidebar_data)

result = None

if workspace_data["action"]:

    if workspace_data["action"] != "explain":
        if not workspace_data["code"].strip():
            st.warning("Please enter or upload source code.")
            st.stop()

    if workspace_data["action"] == "explain":
        if not workspace_data["error"].strip():
            st.warning("Please enter an error message.")
            st.stop()

    try:

        action = workspace_data["action"]
        spinner_msg = {
            "analyze": "Analyzing your code...",
            "debug": "Debugging code...",
            "explain": "Explaining error...",
            "optimize": "Optimizing code..."
        }.get(action, "Contacting DebugGPT...")

        with st.spinner(spinner_msg):

            if workspace_data["action"] == "analyze":

                result = {
                    "analysis": analyze(
                        workspace_data["language"],
                        workspace_data["code"],
                    )
                }

            elif workspace_data["action"] == "debug":

                result = {
                    "debug": debug(
                        workspace_data["language"],
                        workspace_data["code"],
                    )
                }

            elif workspace_data["action"] == "optimize":

                result = {
                    "optimization": optimize(
                        workspace_data["language"],
                        workspace_data["code"],
                    )
                }

            elif workspace_data["action"] == "explain":

                result = {
                    "learning": explain(
                        workspace_data["error"],
                    )
                }

        st.success("Operation completed successfully.")

    except APIClientError as exc:

        st.error(
            "Unable to process your request.\n\n"
            "Please ensure the backend is running."
        )
        with st.expander("Technical Details"):
            st.code(str(exc))

render_results(result)

render_footer()