import streamlit as st


def main():
    st.header("Hello world")
    st.balloons()


def sidebar():
    st.sidebar.markdown(
        "<style> .sidebar .sidebar-content { background-color: black; } </style>",
        unsafe_allow_html=True,
    )
    st.sidebar.markdown(
        "<h1 style='text-align: center; color: white;'>ChatGPT Styled Sidebar</h1>",
        unsafe_allow_html=True,
    )
    user_input = st.sidebar.text_input("Enter your message", value="Type here...")
    if st.sidebar.button("Send"):
        st.sidebar.markdown(
            f"<p style='color: white;'>You: {user_input}</p>", unsafe_allow_html=True
        )
        st.sidebar.markdown(
            "<p style='color: white;'>ChatGPT: Here would be the response.</p>",
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
