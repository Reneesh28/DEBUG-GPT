"""
Main workspace component.
"""

import streamlit as st

from components.actions import render_actions

PYTHON_EXAMPLE = """def greet(name):
    print(f"Hello, {name}")

greet("DebugGPT")
"""


CPP_EXAMPLE = """#include <iostream>

using namespace std;

int main()
{
    cout << "Hello DebugGPT";
    return 0;
}
"""


def render_workspace(sidebar_data):
    """
    Render the editable workspace.

    Parameters
    ----------
    sidebar_data : dict

    Returns
    -------
    dict
    """

    st.subheader("Code Workspace")

    language = sidebar_data["language"]

    uploaded_code = sidebar_data["source_code"]

    example = sidebar_data["example"]

    if uploaded_code:

        initial_code = uploaded_code

    elif example == "Python Example":

        initial_code = PYTHON_EXAMPLE

    elif example == "C++ Example":

        initial_code = CPP_EXAMPLE

    else:

        initial_code = ""

    st.caption(f"Selected Language: **{language}**")

    if sidebar_data.get("uploaded_source_name"):
        st.caption(f"Current Source: {sidebar_data['uploaded_source_name']}")

    code = st.text_area(
        label="Source Code",
        value=initial_code,
        height=450,
        placeholder="Paste your source code here...",
        key="code"
    )

    error_text = st.text_area(
        label="Compiler / Runtime Error (Optional)",
        value=sidebar_data["error_log"],
        height=150,
        placeholder="Paste compiler or runtime errors here...",
        key="error"
    )

    st.divider()

    selected_action = render_actions()

    return {
        "language": language,
        "code": code,
        "error": error_text,
        "action": selected_action,
    }