"""
Sidebar component.
"""

import streamlit as st

from utils.helpers import (
    read_uploaded_file,
    validate_extension,
    format_file_size,
    SUPPORTED_SOURCE_EXTENSIONS,
    SUPPORTED_LOG_EXTENSIONS,
)


def render_sidebar():
    """
    Render the application sidebar.

    Returns
    -------
    dict
        User-selected sidebar values.
    """

    with st.sidebar:

        st.header("Configuration")

        language = st.selectbox(
            "Programming Language",
            ["Python", "C++"],
        )

        uploaded_source = st.file_uploader(
            "Upload Source Code",
            type=["py", "cpp", "ipynb"],
        )

        st.caption(
            "Supported source files: .py .cpp .ipynb"
        )

        source_code = ""

        if uploaded_source:

            if validate_extension(
                uploaded_source.name,
                SUPPORTED_SOURCE_EXTENSIONS,
            ):

                source_code = read_uploaded_file(uploaded_source)

                st.success("Source code uploaded successfully.")

                st.caption(f"File: {uploaded_source.name}")

                st.caption(
                    f"Size: {format_file_size(uploaded_source.size)}"
                )

            else:

                st.error(
                    "Unsupported file.\n\n"
                    "Please upload one of:\n\n"
                    "• .py\n"
                    "• .cpp\n"
                    "• .ipynb"
                )

        uploaded_log = st.file_uploader(
            "Upload Error Log",
            type=["log"],
        )

        st.caption(
            "Supported log files: .log"
        )

        error_log = ""

        if uploaded_log:

            if validate_extension(
                uploaded_log.name,
                SUPPORTED_LOG_EXTENSIONS,
            ):

                error_log = read_uploaded_file(uploaded_log)

                st.success("Error log uploaded successfully.")

                st.caption(uploaded_log.name)

                st.caption(
                    format_file_size(uploaded_log.size)
                )

            else:

                st.error(
                    "Unsupported log file.\n\n"
                    "Supported:\n\n"
                    "• .log"
                )

        example = st.selectbox(
            "Load Example",
            [
                "None",
                "Python Example",
                "C++ Example",
            ],
        )

        with st.expander("About DebugGPT"):

            st.markdown(
                """
                **DebugGPT**

                AI-Powered Code Error Explanation &
                Debugging Assistant

                **Supported Languages**

                - Python
                - C++

                **Frontend**

                Streamlit

                **Backend**

                FastAPI
                """
            )

        if st.button(
            "Reset Session",
            use_container_width=True,
        ):
            st.session_state.clear()
            st.rerun()

        return {
            "language": language,
            "source_code": source_code,
            "error_log": error_log,
            "example": example,
            "uploaded_source_name": uploaded_source.name if uploaded_source else None,
        }