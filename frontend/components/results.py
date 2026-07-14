"""
Results component for DebugGPT.
"""

import streamlit as st


def render_dict(data):
    """
    Render a dictionary into formatted Streamlit elements.
    """
    if not isinstance(data, dict):
        st.write(data)
        return
        
    for key, value in data.items():
        st.subheader(key.replace("_", " ").title())
        if isinstance(value, list):
            for item in value:
                st.markdown(f"- {item}")
        elif isinstance(value, dict):
            st.json(value)
        else:
            st.markdown(str(value))


def render_results(result=None):
    """
    Render result tabs.

    Parameters
    ----------
    result : dict | None
        Backend response (placeholder for now).
    """

    st.divider()

    st.subheader("Results")

    if not result:
        st.info("Run an analysis to view DebugGPT results.")
        return

    analysis_tab, debug_tab, optimization_tab, learning_tab = st.tabs(
        [
            "📊 Analysis",
            "🐞 Debug",
            "⚡ Optimization",
            "🎓 Learning Mode",
        ]
    )

    with analysis_tab:
        if "analysis" in result:
            render_dict(result["analysis"])
        else:
            st.info("No analysis data available.")

    with debug_tab:
        if "debug" in result:
            render_dict(result["debug"])
        else:
            st.info("No debug data available.")

    with optimization_tab:
        if "optimization" in result:
            render_dict(result["optimization"])
        else:
            st.info("No optimization data available.")

    with learning_tab:
        if "learning" in result:
            render_dict(result["learning"])
        else:
            st.info("No learning data available.")