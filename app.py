import streamlit as st
import uuid
import json
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

# -------------------------
# OPENAI
# -------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Indian ADR Mediation Simulator", layout="wide")

st.title("⚖️ Indian ADR Mediation Simulator")

# -------------------------
# SIDEBAR SETTINGS
# -------------------------
language = st.sidebar.selectbox(
    "Language",
    ["English", "Hindi", "Marathi"]
)

session_mode = st.sidebar.radio(
    "Session Mode",
    ["Single User Mock Session", "Multi User Room"]
)

case_category = st.sidebar.selectbox(
    "Dispute Category",
    [
        "Property Dispute",
        "Family Property Settlement",
        "Landlord Tenant Conflict",
        "Consumer Complaint",
        "Startup Partnership Dispute",
        "Employment Conflict",
        "MSME Contract Payment Dispute"
    ]
)

# -------------------------
# SESSION STATE INIT
# -------------------------
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

# -------------------------
# ROOM SYSTEM
# -------------------------
if session_mode == "Multi User Room":

    st.sidebar.subheader("Online Mediation Room")

    option = st.sidebar.radio(
        "Room Option",
        ["Create Room", "Join Room"]
    )

    if option == "Create Room":

        if st.sidebar.button("Generate Room ID"):
            st.session_state.room_id = str(uuid.uuid4())[:6]

        st.sidebar.success(f"Room ID: {st.session_state.room_id}")

    if option == "Join Room":

        join_id = st.sidebar.text_input("Enter Room ID")

        if st.sidebar.button("Join"):
            st.session_state.room_id = join_id
            st.sidebar.success(f"Joined Room: {join_id}")

# -------------------------
# AI CASE GENERATOR
# -------------------------
def generate_indian_case():

    prompt = f"""
Generate a realistic mediation dispute occurring in India.

Category: {case_category}

Use Indian names and cities.
Dispute should be suitable for mediation under the Arbitration and Conciliation Act, 1996 or Lok Adalat.

Return JSON ONLY:

{{
"title":"",
"background":"",
"evidence":[
"evidence1",
"evidence2",
"evidence3"
]
}}

Background must be detailed (5-6 lines).
Evidence must be hidden facts influencing settlement.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return json.loads(response.choices[0].message.content)

# -------------------------
# GENERATE CASE
# -------------------------
if st.button("Generate Indian ADR Case"):

    case_data = generate_indian_case()

    st.session_state.case = case_data
    st.session_state.hidden_evidence = case_data["evidence"]
    st.session_state.evidence_revealed = False
    st.session_state.messages_a = []
    st.session_state.messages_b = []
    st.session_state.score_history = []

# -------------------------
# CASE DISPLAY
# -------------------------
if st.session_state.case:

    st.subheader("📁 Case Summary")

    st.write("###", st.session_state.case["title"])

    st.write(st.session_state.case["background"])

# -------------------------
# EVIDENCE
# -------------------------
st.subheader("🔎 Evidence")

if st.button("Reveal Evidence"):
    st.session_state.evidence_revealed = True

if st.session_state.evidence_revealed:

    st.success("Hidden Evidence Revealed")

    for ev in st.session_state.hidden_evidence:
        st.write("•", ev)

else:

    st.warning("Evidence hidden until mediator reveals it.")

# -------------------------
# NEGOTIATION
# -------------------------
st.subheader("💬 Negotiation")

if session_mode == "Single User Mock Session":

    user_msg = st.text_area("Party A (Your Position)")

    if st.button("Send Offer"):

        st.session_state.messages_a.append(user_msg)

        transcript = "\n".join(st.session_state.messages_a)

        prompt = f"""
You are Party B in an Indian mediation dispute.

Case Background:
{st.session_state.case["background"]}

Negotiation:
{transcript}

Respond with a realistic counter proposal.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}]
        )

        ai_reply = response.choices[0].message.content

        st.session_state.messages_b.append(ai_reply)

if session_mode == "Multi User Room":

    role = st.selectbox("Select Role", ["Party A", "Party B", "Mediator"])

    msg = st.text_input("Enter message")

    if st.button("Send Message"):

        if role == "Party A":
            st.session_state.messages_a.append(msg)

        if role == "Party B":
            st.session_state.messages_b.append(msg)

# -------------------------
# TRANSCRIPT
# -------------------------
st.subheader("Negotiation Transcript")

for m in st.session_state.messages_a:
    st.write("🟦 Party A:", m)

for m in st.session_state.messages_b:
    st.write("🟩 Party B:", m)

# -------------------------
# EMOTION DETECTION
# -------------------------
def detect_emotion(text):

    text = text.lower()

    anger_words = ["fight","court","refuse","never"]
    cooperative_words = ["agree","settle","compromise","solution"]

    if any(w in text for w in anger_words):
        return "Angry"

    if any(w in text for w in cooperative_words):
        return "Cooperative"

    return "Neutral"

# -------------------------
# NEGOTIATION SCORE
# -------------------------
def negotiation_score():

    score = 50

    messages = st.session_state.messages_a + st.session_state.messages_b

    for m in messages:

        emotion = detect_emotion(m)

        if emotion == "Cooperative":
            score += 10

        if emotion == "Angry":
            score -= 10

    score = max(0, min(score, 100))

    return score

# -------------------------
# EVALUATE
# -------------------------
if st.button("Evaluate Negotiation"):

    score = negotiation_score()

    st.session_state.score_history.append(score)

# -------------------------
# SETTLEMENT PROBABILITY
# -------------------------
if st.session_state.score_history:
    score = st.session_state.score_history[-1]
else:
    score = 0

st.subheader("📊 Settlement Probability")

st.progress(score)

st.write(f"Probability of Settlement: {score}%")

# -------------------------
# AI MEDIATOR
# -------------------------
if st.button("AI Mediator Suggestion"):

    transcript = "\n".join(
        st.session_state.messages_a +
        st.session_state.messages_b
    )

    prompt = f"""
You are a professional mediator in India.

Case:
{st.session_state.case["background"]}

Negotiation:
{transcript}

Provide a settlement suggestion consistent with Indian ADR practices.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    suggestion = response.choices[0].message.content

    st.subheader("Mediator Recommendation")

    st.write(suggestion)

# -------------------------
# DASHBOARD
# -------------------------
st.subheader("📈 Mediator Dashboard")

if st.session_state.score_history:

    df = pd.DataFrame({
        "Round": range(1,len(st.session_state.score_history)+1),
        "Score": st.session_state.score_history
    })

    fig = plt.figure()

    plt.plot(df["Round"], df["Score"], marker="o")

    plt.xlabel("Negotiation Round")
    plt.ylabel("Settlement Score")

    st.pyplot(fig)

# -------------------------
# REPORT
# -------------------------
st.subheader("📄 Mediation Report")

report = f"""
INDIAN ADR MEDIATION REPORT

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
    file_name="indian_mediation_report.txt"
)
