import streamlit as st
import json
from datetime import datetime
import sys
import os

# ---------------- DATA ----------------
version_float = 1.1

questions = [
    {"q": "How often do you participate in volunteering activities?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
   
    {"q": "How often do you actively seek opportunities to volunteer?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How often do you volunteer even when it is not required for academic or professional reasons?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How often do you choose volunteering over other leisure activities?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How often do you participate in volunteering despite having a busy schedule?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How often do you engage in different types of volunteer activities (e.g., community service, mentoring, environmental work)?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},

    {"q": "How often do you maintain consistent involvement in volunteering over time?",
     "opts": [("Never",0),("Rarely",1),("Sometimes",2),("Often",3),("Always",4)]},
    
    {"q": "To what extent do you feel that volunteering gives your life meaning?",
     "opts": [("Not at all",0),("Slightly",1),("Moderately",2),("Strongly",3),("Very strongly",4)]},

    {"q": "To what extent do you feel that volunteering allows you to contribute to something important?",
     "opts": [("Not at all",0),("Slightly",1),("Moderately",2),("Strongly",3),("Very strongly",4)]},

    {"q": "To what extent does volunteering provide you with a sense of direction in life?",
     "opts": [("Not at all",0),("Slightly",1),("Moderately",2),("Strongly",3),("Very strongly",4)]},

    {"q": "To what extent do you feel fulfilled after participating in volunteer activities?",
     "opts": [("Not at all",0),("Slightly",1),("Moderately",2),("Strongly",3),("Very strongly",4)]},

    {"q": "To what extent has volunteering helped you understand your personal values?",
     "opts": [("Not at all",0),("Slightly",1),("Moderately",2),("Strongly",3),("Very strongly",4)]},

    {"q": "To what extent does volunteering increase your motivation in life?",
     "opts": [("Not at all",0),("Slightly",1),("Moderately",2),("Strongly",3),("Very strongly",4)]},

    {"q": "To what extent do you feel that volunteering supports your long-term goals?",
     "opts": [("Not at all",0),("Slightly",1),("Moderately",2),("Strongly",3),("Very strongly",4)]},

    {"q": "To what extent do you experience a sense of achievement from volunteering?",
     "opts": [("Not at all",0),("Slightly",1),("Moderately",2),("Strongly",3),("Very strongly",4)]}
]

psych_states = {
    "Very Low Purpose from Volunteering": (0, 12),
    "Low Purpose from Volunteering": (13, 24),
    "Moderate Purpose": (25, 36),
    "High Purpose from Volunteering": (37, 48),
    "Very High Purpose and Engagement": (49, 60)
}

# ---------------- HELPERS ----------------
def validate_name(name: str) -> bool:
    return len(name.strip()) > 0 and not any(c.isdigit() for c in name)

def validate_dob(dob: str) -> bool:
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except:
        return False

def interpret_score(score: int) -> str:
    for state, (low, high) in psych_states.items():
        if low <= score <= high:
            return state
    return "Unknown"

def save_json(filename: str, data: dict):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ---------------- STREAMLIT APP ----------------
st.set_page_config(page_title="Volunteer Activity Survey")
st.title("📝 Volunteering Activity & Sense of Purpose Survey")

st.info("Please provide your details and answer all questions honestly based on your volunteering experience.")

if "started" not in st.session_state:
    st.session_state.started = False
# --- User Info ---
name = st.text_input("Given Name")
surname = st.text_input("Surname")
dob = st.text_input("Date of Birth (YYYY-MM-DD)")
sid = st.text_input("Student ID (digits only)")

# --- Start Survey ---
if st.button("Start Survey"):

    # Validate inputs
    errors = []
    if not validate_name(name):
        errors.append("Invalid given name.")
    if not validate_name(surname):
        errors.append("Invalid surname.")
    if not validate_dob(dob):
        errors.append("Invalid date of birth format. Use YYYY-MM-DD.")
    if not sid.isdigit():
        errors.append("Student ID must be digits only.")

    if errors:
        for e in errors:
            st.error(e)
    else:
        st.success("All inputs are valid. Proceed to answer the questions below.")
        st.session_state.started = True
        
if st.session_state.started:

        total_score = 0
        answers = []

        for idx, q in enumerate(questions):
            opt_labels = [opt[0] for opt in q["opts"]]
            choice = st.selectbox(f"Q{idx+1}. {q['q']}", opt_labels, key=f"q{idx}")
            score = next(score for label, score in q["opts"] if label == choice)
            total_score += score
            answers.append({
                "question": q["q"],
                "selected_option": choice,
                "score": score
            })

        status = interpret_score(total_score)

        st.markdown(f"## ✅ Your Result: {status}")
        st.markdown(f"**Total Score:** {total_score}")

        # Save results to JSON
        record = {
            "name": name,
            "surname": surname,
            "dob": dob,
            "student_id": sid,
            "total_score": total_score,
            "result": status,
            "answers": answers,
            "version": version_float
        }

        json_filename = f"{sid}_result.json"
        save_json(json_filename, record)

        st.success(f"Your results are saved as {json_filename}")
        st.download_button("Download your result JSON", json.dumps(record, indent=2), file_name=json_filename)
