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

Remain neutral and encourage fair negotiation.

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

    st.write(summary.choices[0].message.content)]

party_roles = [
    "Aggressive negotiator",
    "Defensive negotiator",
    "Emotional stakeholder",
    "Strategic negotiator",
    "Logical corporate representative",
]

facts_list = [
    "A disagreement arose after a recent business decision.",
    "One party claims financial losses due to the other’s actions.",
    "Both parties disagree on the interpretation of a contract.",
    "A recent event triggered conflict between the parties.",
    "A long-standing partnership has broken down.",
]

def generate_case():

    case_type = random.choice(case_types)

    case = {
        "case": case_type,
        "partyA": f"Party A is a {random.choice(party_roles)} claiming unfair treatment.",
        "partyB": f"Party B is a {random.choice(party_roles)} defending their actions.",
        "facts": random.choice(facts_list)
    }

    return case

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "case" not in st.session_state:
    st.session_state.case = generate_case()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

case = st.session_state.case

# ---------------------------------------------------
# CASE DISPLAY
# ---------------------------------------------------

st.header(translate_text("Case Details", language))

st.write("**Case:**", translate_text(case.get("case","No case available"), language))
st.write("**Party A:**", translate_text(case.get("partyA","Unavailable"), language))
st.write("**Party B:**", translate_text(case.get("partyB","Unavailable"), language))
st.write("**Facts:**", translate_text(case.get("facts","Unavailable"), language))

# ---------------------------------------------------
# NEW CASE BUTTON
# ---------------------------------------------------

if st.button("Generate New Case"):

    st.session_state.case = generate_case()
    st.session_state.chat_history = []
    st.rerun()

# ---------------------------------------------------
# NEGOTIATION DISCUSSION
# ---------------------------------------------------

st.header(translate_text("Negotiation Discussion", language))

user_input = st.text_input(
    translate_text("Enter your mediation message", language)
)

# ---------------------------------------------------
# HANDLE USER MESSAGE
# ---------------------------------------------------

if st.button("Send Message") and user_input:

    if language == "Marathi":
        user_input_for_ai = GoogleTranslator(source='mr', target='en').translate(user_input)
    else:
        user_input_for_ai = user_input

    st.session_state.chat_history.append(("User", user_input))

    if client:

        prompt = f"""
You are an AI mediator helping resolve a dispute.

Case: {case['case']}
Party A: {case['partyA']}
Party B: {case['partyB']}
Facts: {case['facts']}

User message:
{user_input_for_ai}

Respond as a neutral mediator encouraging constructive dialogue.
"""

        try:

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )

            mediator_reply = response.output_text

        except:
            mediator_reply = "Mediator response unavailable."

    else:

        mediator_reply = "AI mediator disabled (API key missing)."

    translated_reply = translate_text(mediator_reply, language)

    st.session_state.chat_history.append(("Mediator", translated_reply))

# ---------------------------------------------------
# CHAT DISPLAY
# ---------------------------------------------------

for role, message in st.session_state.chat_history:

    if role == "User":
        st.write(f"🧑 {message}")
    else:
        st.write(f"⚖️ {message}")

# ---------------------------------------------------
# FINAL MEDIATION REPORT
# ---------------------------------------------------

st.header(translate_text("Final Session Report", language))

if st.button("Generate Mediation Report"):

    conversation = "\n".join(
        [f"{r}: {m}" for r,m in st.session_state.chat_history]
    )

    report = f"""
Case: {case['case']}

Party A Position:
{case['partyA']}

Party B Position:
{case['partyB']}

Facts:
{case['facts']}

Discussion Summary:
{conversation}

Mediator Observation:
Both parties participated in mediation discussions. Further negotiation may help reach mutual agreement.
"""

    translated_report = translate_text(report, language)

    st.write(translated_report)

# ---------------------------------------------------
# DASHBOARD (Basic Analytics)
# ---------------------------------------------------

st.sidebar.header("Mediation Dashboard")

st.sidebar.write(
    "Messages exchanged:",
    len(st.session_state.chat_history)
)

if len(st.session_state.chat_history) > 6:
    st.sidebar.success("Negotiation progressing")
else:
    st.sidebar.info("Early stage discussion")
