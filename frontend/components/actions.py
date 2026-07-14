"""
Action buttons for DebugGPT.
"""

import streamlit as st


def clear_editor():
    if "code" in st.session_state:
        st.session_state["code"] = ""
    if "error" in st.session_state:
        st.session_state["error"] = ""


def render_actions():
    """
    Render action buttons.

    Returns
    -------
    str | None
        Selected action.
    """

    col1, col2, col3, col4, col5 = st.columns(5)

    selected_action = None

    with col1:
        if st.button(
            "🔍 Analyze",
            use_container_width=True,
        ):
            selected_action = "analyze"

    with col2:
        if st.button(
            "🐞 Debug",
            use_container_width=True,
        ):
            selected_action = "debug"

    with col3:
        if st.button(
            "📖 Explain",
            use_container_width=True,
        ):
            selected_action = "explain"

    with col4:
        if st.button(
            "⚡ Optimize",
            use_container_width=True,
        ):
            selected_action = "optimize"

    with col5:
        st.button(
            "🗑 Clear Editor",
            use_container_width=True,
            on_click=clear_editor,
        )

    return selected_action