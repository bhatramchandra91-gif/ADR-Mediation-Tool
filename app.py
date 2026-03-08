import streamlit as st
import random
import uuid
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from openai import OpenAI

# -----------------------------
# OPENAI CLIENT
# -----------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="AI ADR Mediation Platform", layout="wide")

st.title("⚖️ AI ADR Mediation Platform")

# -----------------------------
# LANGUAGE SELECT
# -----------------------------
language = st.sidebar.selectbox(
    "Select Language",
    ["English","Hindi","Marathi"]
)

# -----------------------------
# TRANSLATION
# -----------------------------
translations = {
"Reveal Evidence":{
"Hindi":"सबूत दिखाएं",
"Marathi":"पुरावे दाखवा"
},
"Negotiation":{
"Hindi":"बातचीत",
"Marathi":"वाटाघाटी"
},
"Mediator Dashboard":{
"Hindi":"मध्यस्थ डैशबोर्ड",
"Marathi":"मध्यस्थ डॅशबोर्ड"
}
}

def translate(text):
    if language=="English":
        return text
    if text in translations:
        return translations[text].get(language,text)
    return text


# -----------------------------
# SESSION STATE
# -----------------------------
if "room_id" not in st.session_state:
    st.session_state.room_id = str(uuid.uuid4())[:6]

if "messages_a" not in st.session_state:
    st.session_state.messages_a=[]

if "messages_b" not in st.session_state:
    st.session_state.messages_b=[]

if "score_history" not in st.session_state:
    st.session_state.score_history=[]

if "case" not in st.session_state:
    st.session_state.case=None

if "evidence_revealed" not in st.session_state:
    st.session_state.evidence_revealed=False


# -----------------------------
# MEDIATION ROOM
# -----------------------------
st.sidebar.subheader("Online Mediation Room")

st.sidebar.write("Room ID:",st.session_state.room_id)

if st.sidebar.button("Generate New Room"):
    st.session_state.room_id=str(uuid.uuid4())[:6]


# -----------------------------
# AI CASE GENERATOR
# -----------------------------
def generate_ai_case():

    prompt="""
    Generate a short mediation dispute with:
    Case title
    Background
    Two hidden evidences
    """

    res=client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"user","content":prompt}]
    )

    return res.choices[0].message.content


if st.button("Generate AI Dispute Case"):

    case_text=generate_ai_case()

    st.session_state.case=case_text

    st.session_state.evidence_revealed=False


if st.session_state.case:

    st.subheader("📁 Mediation Case")

    st.write(st.session_state.case)


# -----------------------------
# EVIDENCE
# -----------------------------
st.subheader("Evidence Phase")

if st.button(translate("Reveal Evidence")):
    st.session_state.evidence_revealed=True

if st.session_state.evidence_revealed:
    st.success("Evidence disclosed to mediator")

else:
    st.warning("Evidence hidden until negotiation progresses")


# -----------------------------
# NEGOTIATION CHATBOTS
# -----------------------------
st.subheader(translate("Negotiation"))

col1,col2=st.columns(2)

with col1:

    st.markdown("### Party A Chat")

    msg_a=st.text_input("Party A message")

    if st.button("Send A"):

        st.session_state.messages_a.append(msg_a)


    for m in st.session_state.messages_a:
        st.write("A:",m)


with col2:

    st.markdown("### Party B Chat")

    msg_b=st.text_input("Party B message")

    if st.button("Send B"):

        st.session_state.messages_b.append(msg_b)

    for m in st.session_state.messages_b:
        st.write("B:",m)


# -----------------------------
# EMOTION DETECTION
# -----------------------------
def detect_emotion(text):

    text=text.lower()

    anger=["fight","court","refuse","never"]

    cooperative=["agree","settle","compromise","solution"]

    if any(w in text for w in anger):
        return "Angry"

    if any(w in text for w in cooperative):
        return "Cooperative"

    return "Neutral"


# -----------------------------
# NEGOTIATION SCORE
# -----------------------------
def negotiation_score():

    score=50

    for m in st.session_state.messages_a+st.session_state.messages_b:

        emotion=detect_emotion(m)

        if emotion=="Cooperative":
            score+=10

        if emotion=="Angry":
            score-=10

    score=max(0,min(score,100))

    return score


if st.button("Evaluate Negotiation"):

    score=negotiation_score()

    st.session_state.score_history.append(score)


# -----------------------------
# SETTLEMENT PROBABILITY
# -----------------------------
if st.session_state.score_history:

    score=st.session_state.score_history[-1]

else:

    score=0


st.subheader("Settlement Probability")

st.progress(score)

st.write("Settlement Probability:",score,"%")



# -----------------------------
# MEDIATOR GPT SUGGESTION
# -----------------------------
if st.button("AI Mediator Suggestion"):

    transcript="\n".join(st.session_state.messages_a+st.session_state.messages_b)

    prompt=f"""
    You are a professional mediator.
    Suggest a settlement based on this negotiation:

    {transcript}
    """

    res=client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role":"user","content":prompt}]
    )

    suggestion=res.choices[0].message.content

    st.subheader("Mediator Recommendation")

    st.write(suggestion)



# -----------------------------
# GRAPH DASHBOARD
# -----------------------------
st.subheader(translate("Mediator Dashboard"))

if st.session_state.score_history:

    df=pd.DataFrame({
    "Round":range(1,len(st.session_state.score_history)+1),
    "Score":st.session_state.score_history
    })

    fig=plt.figure()

    plt.plot(df["Round"],df["Score"],marker="o")

    plt.xlabel("Negotiation Round")

    plt.ylabel("Settlement Score")

    st.pyplot(fig)



# -----------------------------
# MEDIATION REPORT
# -----------------------------
st.subheader("Download Mediation Report")

report=f"""

AI ADR MEDIATION REPORT
-----------------------

Date: {datetime.now()}

Room ID: {st.session_state.room_id}

Case:
{st.session_state.case}

Party A Messages:
{st.session_state.messages_a}

Party B Messages:
{st.session_state.messages_b}

Score History:
{st.session_state.score_history}

Final Settlement Probability:
{score}%

"""


st.download_button(
label="Download Report",
data=report,
file_name="mediation_report.txt"
)
