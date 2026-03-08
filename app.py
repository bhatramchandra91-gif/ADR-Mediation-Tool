import streamlit as st
import random
from openai import OpenAI

# ---------------- CONFIG ----------------

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="ADR Mediation Simulator", layout="wide")

st.title("⚖️ AI ADR Mediation Training Simulator")

# ---------------- DISCLAIMER ----------------

st.warning(
"""
This ADR simulator is for training and educational purposes only.
It does not provide legal advice. All mediation sessions are simulated.
"""
)

# ---------------- CASE DATABASE ----------------

cases = [

{
"title":"Startup Equity Dispute",
"party_a":"Founder claims investor unfairly diluted equity.",
"party_b":"Investor claims founder failed agreed targets.",
"facts":"Company recently raised Series A funding.",
"hidden_facts":"Side agreement gives investor veto rights."
},

{
"title":"Employment Termination",
"party_a":"Employee claims wrongful termination.",
"party_b":"Employer claims misconduct.",
"facts":"Employee terminated after internal investigation.",
"hidden_facts":"Evidence suggests internal bias."
}

]

# ---------------- PERSONALITIES ----------------

personalities = [

"Aggressive negotiator",
"Emotional party",
"Logical corporate lawyer",
"Defensive employee",
"Strategic negotiator"

]

# ---------------- TWISTS ----------------

twists = [

"New email evidence appears.",
"Financial records contradict testimony.",
"A witness changes the timeline.",
"A hidden clause in the contract is revealed.",
"One party becomes emotionally aggressive."

]

# ---------------- SESSION STATE ----------------

if "case" not in st.session_state:

    case = random.choice(cases)

    case["personality_a"] = random.choice(personalities)
    case["personality_b"] = random.choice(personalities)

    st.session_state.case = case
    st.session_state.messages = []
    st.session_state.turn = 0

    st.session_state.settlement_probability = 50
    st.session_state.trust_level = 50
    st.session_state.conflict_level = 50
    st.session_state.score = 0

case = st.session_state.case

# ---------------- SIDEBAR UX ----------------

if st.sidebar.button("Start New Case"):

    st.session_state.clear()
    st.rerun()

# ---------------- JURISDICTION ----------------

jurisdiction = st.sidebar.selectbox(
"Select Jurisdiction",
["India","International"]
)

if jurisdiction == "India":
    law = "Arbitration and Conciliation Act, 1996"
else:
    law = "UNCITRAL Model Law"

st.sidebar.write("Applicable Law:", law)

# ---------------- NEGOTIATION CONTEXT ----------------

st.sidebar.subheader("BATNA")

st.sidebar.write("Party A BATNA: Proceed to arbitration")
st.sidebar.write("Party B BATNA: File lawsuit")

# ---------------- MEDIATION DASHBOARD ----------------

st.sidebar.subheader("Mediation Metrics")

st.sidebar.metric(
"Settlement Probability",
f"{st.session_state.settlement_probability}%"
)

st.sidebar.metric(
"Trust Level",
st.session_state.trust_level
)

st.sidebar.metric(
"Conflict Level",
st.session_state.conflict_level
)

st.sidebar.metric(
"Mediator Score",
st.session_state.score
)

# ---------------- CASE DISPLAY ----------------

st.subheader("Case Scenario")

st.write("**Case:**", case["title"])
st.write("**Party A:**", case["party_a"])
st.write("Personality:", case["personality_a"])

st.write("**Party B:**", case["party_b"])
st.write("Personality:", case["personality_b"])

st.write("**Facts:**", case.get("facts","No facts available"))

# ---------------- EVIDENCE PANEL ----------------

st.sidebar.subheader("Evidence")

if st.sidebar.button("Reveal Evidence"):
    st.sidebar.write(case.get("hidden_facts","No hidden facts"))

st.divider()

# ---------------- CHAT HISTORY ----------------

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------------- USER INPUT ----------------

user_input = st.chat_input("Mediator: What would you like to say?")

if user_input:

    st.session_state.messages.append({"role":"user","content":user_input})

    prompt = f"""
    You are simulating a professional mediation session.

    Party A personality: {case["personality_a"]}
    Party B personality: {case["personality_b"]}

    Mediator message:

    {user_input}

    Respond as:

    Party A reaction
    Party B reaction
    Mediator observation
    """

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[
            {"role":"system","content":"You are a neutral mediation trainer"},
            {"role":"user","content":prompt}
        ]

    )

    ai_reply = response.choices[0].message.content

    st.session_state.messages.append(
        {"role":"assistant","content":ai_reply}
    )

    # ---------------- TWIST ENGINE ----------------

    if st.session_state.turn % 2 == 1:

        twist = random.choice(twists)

        st.session_state.messages.append({

        "role":"assistant",
        "content":f"⚖️ Case Twist: {twist}"

        })

    # ---------------- PROBABILITY UPDATE ----------------

    if "settlement" in user_input.lower():

        st.session_state.settlement_probability += 10
        st.session_state.score += 8

    if "clarify" in user_input.lower():

        st.session_state.trust_level += 8
        st.session_state.score += 5

    if "threat" in user_input.lower():

        st.session_state.conflict_level += 10
        st.session_state.settlement_probability -= 5

    st.session_state.turn += 1

# ---------------- FINAL SESSION REPORT ----------------

if st.session_state.turn >= 6:

    st.subheader("Final Mediation Report")

    summary_prompt = f"""

Analyze this mediation session.

Conversation:

{st.session_state.messages}

Provide:

1. Good mediator decisions
2. Bad decisions
3. Settlement likelihood
4. Mediator skill rating
5. Advice for improvement

"""

    summary = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[{"role":"user","content":summary_prompt}]

    )

    st.write(summary.choices[0].message.content)
