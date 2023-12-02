import streamlit as st


def load_css():
    st.markdown("""
        <style>
        html, body, [class*="css"] {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        }
        h1, h2, h3 {
            color: #32CD32; /* Slightly darker green */
        }
        /* Styling for the active tab */
        .st-bb .st-at, .st-bb .st-ae {
            border-color: #32CD32 !important;
        }
        .st-bb .st-at {
            background-color: #32CD32 !important;
            color: white !important;
        }
        /* Styling for the inactive tab */
        .st-bb .st-ae {
            background-color: transparent !important;
        }
        </style>
        """, unsafe_allow_html=True)


def about_us():
    load_css()
    st.title("About Us - Deepfake Detection Service")

    st.write(
        "Welcome to our Deepfake Detection Service! We are a team of dedicated individuals "
        "committed to leveraging our expertise in Data Science to address the challenges posed "
        "by deepfake technology. Our team is comprised of three highly skilled graduate students "
        "from the renowned UC Berkeley, all graduating with master's degrees in Data Science."
    )
    st.header("Our Mission")

    st.write(
        "At our core, we are driven by the mission to combat the rise of deepfake technology. "
        "Our focus is on developing cutting-edge solutions that empower individuals and organizations "
        "to detect and mitigate the impact of manipulated media. We believe in the responsible use of technology "
        "and strive to create a safer digital environment for everyone."
    )

    st.header("Meet the Team")

    # Information about each team member
    team_members = [
        {"name": "Saket Suman", "role": "Co-Founder & Data Scientist", "image": "team/Untitled.jpg"},
        {"name": "Chris Ratsimbazafy", "role": "Co-Founder & Machine Learning Engineer", "image": "team/Untitled.jpg"},
        {"name": "Cheick Sissoko", "role": "Co-Founder & Software Engineer", "image": "team/Untitled.jpg"},
    ]

    for member in team_members:
        st.subheader(member["name"])
        st.image(member["image"], caption=f"{member['role']}")
        st.write(
            f"{member['name']} is our {member['role']} with a strong background in Data Science. "
            "They have demonstrated exceptional skills and dedication throughout their academic journey at UC Berkeley."
        )

    st.header("Contact Us")

    st.write(
        "If you have any questions or would like to learn more about our deepfake detection service, please feel free "
        "to reach out to us at [contact@example.com](mailto:contact@example.com). We appreciate your interest and look "
        "forward to collaborating with you in the fight against deepfake threats."
    )


if __name__ == "__main__":
    about_us()
