import streamlit as st
import random
import uuid
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

# -----------------------------
# OPENAI
# -----------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI ADR Mediation Platform", layout="wide")

st.title("⚖️ AI ADR Mediation Simulator")

# -----------------------------
# LANGUAGE SELECT
# -----------------------------
language = st.sidebar.selectbox(
    "Language",
    ["English","Hindi","Marathi"]
)

# -----------------------------
# SESSION MODE
# -----------------------------
session_mode = st.sidebar.radio(
    "Mediation Mode",
    ["Single User Mock Session","Multi User Room"]
)

# -----------------------------
# SESSION STATE
# -----------------------------
if "room_id" not in st.session_state:
    st.session_state.room_id = str(uuid.uuid4())[:6]

if "case" not in st.session_state:
    st.session_state.case = None

if "hidden_evidence" not in st.session_state:
    st.session_state.hidden_evidence = []

if "evidence_revealed" not in st.session_state:
    st.session_state.evidence_revealed = False

if "messages_a" not in st.session_state:
    st.session_state.messages_a = []

if "messages_b" not in st.session_state:
    st.session_state.messages_b = []

if "score_history" not in st.session_state:
    st.session_state.score_history = []

# -----------------------------
# ROOM SYSTEM
# -----------------------------
if session_mode == "Multi User Room":

    st.sidebar.subheader("Mediation Room")

    option = st.sidebar.radio(
        "Room Option",
        ["Create Room","Join Room"]
    )

    if option == "Create Room":

        if st.sidebar.button("Generate Room ID"):
            st.session_state.room_id = str(uuid.uuid4())[:6]

        st.sidebar.success(f"Room ID: {st.session_state.room_id}")

    if option == "Join Room":

        join_id = st.sidebar.text_input("Enter Room ID")

        if st.sidebar.button("Join"):
            st.session_state.room_id = join_id
            st.sidebar.success(f"Joined {join_id}")

# -----------------------------
# AI CASE GENERATOR
# -----------------------------
def generate_ai_case():

    prompt = """
Generate a mediation dispute.

Return JSON format:

{
"title":"",
"background":"",
"evidence":[
"evidence1",
"evidence2",
"evidence3"
]
}

Background must be detailed (5-6 lines).
Evidence must contain hidden facts.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    content = response.choices[0].message.content

    return json.loads(content)

# -----------------------------
# GENERATE CASE
# -----------------------------
if st.button("Generate AI Case"):

    case_data = generate_ai_case()

    st.session_state.case = case_data
    st.session_state.hidden_evidence = case_data["evidence"]
    st.session_state.evidence_revealed = False

# -----------------------------
# SHOW CASE
# -----------------------------
if st.session_state.case:

    st.subheader("📁 Case Summary")

    st.write("###",st.session_state.case["title"])
    st.write(st.session_state.case["background"])

# -----------------------------
# EVIDENCE
# -----------------------------
st.subheader("🔎 Evidence")

if st.button("Reveal Evidence"):

    st.session_state.evidence_revealed = True

if st.session_state.evidence_revealed:

    st.success("Hidden Evidence Revealed")

    for ev in st.session_state.hidden_evidence:
        st.write("•",ev)

else:

    st.warning("Evidence hidden until mediator reveals it.")

# -----------------------------
# NEGOTIATION
# -----------------------------
st.subheader("💬 Negotiation")

# SINGLE USER MODE
if session_mode == "Single User Mock Session":

    user_msg = st.text_area("Party A (Your Statement)")

    if st.button("Send Offer"):

        st.session_state.messages_a.append(user_msg)

        transcript = "\n".join(st.session_state.messages_a)

        prompt = f"""
You are Party B negotiating in a mediation.

Case:
{st.session_state.case["background"]}

Conversation:
{transcript}

Respond with a negotiation counter offer.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )

        ai_reply = response.choices[0].message.content

        st.session_state.messages_b.append(ai_reply)

# MULTI USER MODE
if session_mode == "Multi User Room":

    role = st.selectbox(
        "Select Role",
        ["Party A","Party B","Mediator"]
    )

    msg = st.text_input("Enter message")

    if st.button("Send Message"):

        if role == "Party A":
            st.session_state.messages_a.append(msg)

        if role == "Party B":
            st.session_state.messages_b.append(msg)

# -----------------------------
# TRANSCRIPT
# -----------------------------
st.subheader("Negotiation Transcript")

for m in st.session_state.messages_a:
    st.write("🟦 Party A:",m)

for m in st.session_state.messages_b:
    st.write("🟩 Party B:",m)

# -----------------------------
# EMOTION DETECTION
# -----------------------------
def detect_emotion(text):

    text = text.lower()

    anger = ["fight","court","refuse","never"]
    cooperative = ["agree","settle","compromise","solution"]

    if any(w in text for w in anger):
        return "Angry"

    if any(w in text for w in cooperative):
        return "Cooperative"

    return "Neutral"

# -----------------------------
# NEGOTIATION SCORE
# -----------------------------
def negotiation_score():

    score = 50

    messages = st.session_state.messages_a + st.session_state.messages_b

    for m in messages:

        emotion = detect_emotion(m)

        if emotion == "Cooperative":
            score += 10

        if emotion == "Angry":
            score -= 10

    score = max(0,min(score,100))

    return score

# -----------------------------
# EVALUATE NEGOTIATION
# -----------------------------
if st.button("Evaluate Negotiation"):

    score = negotiation_score()

    st.session_state.score_history.append(score)

# -----------------------------
# SETTLEMENT PROBABILITY
# -----------------------------
if st.session_state.score_history:

    score = st.session_state.score_history[-1]

else:

    score = 0

st.subheader("📊 Settlement Probability")

st.progress(score)

st.write(f"Probability of Settlement: {score}%")

# -----------------------------
# MEDIATOR AI SUGGESTION
# -----------------------------
if st.button("AI Mediator Suggestion"):

    transcript = "\n".join(
        st.session_state.messages_a +
        st.session_state.messages_b
    )

    prompt = f"""
You are a professional mediator.

Case:
{st.session_state.case["background"]}

Negotiation:
{transcript}

Provide a settlement suggestion.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    suggestion = response.choices[0].message.content

    st.subheader("Mediator Recommendation")

    st.write(suggestion)

# -----------------------------
# MEDIATOR DASHBOARD
# -----------------------------
st.subheader("📈 Mediator Dashboard")

if st.session_state.score_history:

    df = pd.DataFrame({
        "Round": range(1,len(st.session_state.score_history)+1),
        "Score": st.session_state.score_history
    })

    fig = plt.figure()

    plt.plot(df["Round"],df["Score"],marker="o")

    plt.xlabel("Negotiation Round")
    plt.ylabel("Settlement Score")

    st.pyplot(fig)

# -----------------------------
# REPORT
# -----------------------------
st.subheader("📄 Mediation Report")

report = f"""
AI ADR MEDIATION REPORT

Date: {datetime.now()}

Room ID: {st.session_state.room_id}

Case Title:
{st.session_state.case["title"] if st.session_state.case else ""}

Background:
{st.session_state.case["background"] if st.session_state.case else ""}

Evidence:
{st.session_state.hidden_evidence}

Party A Messages:
{st.session_state.messages_a}

Party B Messages:
{st.session_state.messages_b}

Score History:
{st.session_state.score_history}

Settlement Probability:
{score}%
"""

st.download_button(
    label="Download Mediation Report",
    data=report,
    file_name="mediation_report.txt"
)
