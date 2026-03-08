import streamlit as st
import random
from openai import OpenAI
from deep_translator import GoogleTranslator

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------

st.set_page_config(page_title="ADR Mediation Simulator", layout="wide")

# -------------------------------------------------
# LANGUAGE SETTINGS
# -------------------------------------------------

st.sidebar.header("Language Settings")

language = st.sidebar.selectbox(
    "Select Language",
    ["English", "Marathi"]
)

# -------------------------------------------------
# TRANSLATION FUNCTION
# -------------------------------------------------

def translate_text(text, lang):
    if lang == "English":
        return text
    try:
        return GoogleTranslator(source="auto", target="mr").translate(text)
    except:
        return text


# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title(translate_text("⚖️ AI ADR Mediation Training Simulator", language))

# -------------------------------------------------
# OPENAI CLIENT
# -------------------------------------------------

client = None

try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.warning("OpenAI API key missing. AI mediator disabled.")


# -------------------------------------------------
# CASE GENERATOR
# -------------------------------------------------

case_types = [
    "Employment Termination",
    "Startup Equity Dispute",
    "Partnership Conflict",
    "Landlord Tenant Dispute",
    "Family Business Disagreement",
    "Contract Breach"
]

roles = [
    "Aggressive negotiator",
    "Strategic negotiator",
    "Emotional stakeholder",
    "Defensive negotiator",
    "Logical corporate representative"
]

facts = [
    "A disagreement arose after a recent business decision.",
    "One party claims financial losses.",
    "Contract interpretation disagreement occurred.",
    "Conflict escalated after a management decision.",
    "Both parties accuse each other of violating agreements."
]


def generate_case():

    return {
        "case": random.choice(case_types),
        "partyA": f"Party A is a {random.choice(roles)} claiming unfair treatment.",
        "partyB": f"Party B is a {random.choice(roles)} defending their actions.",
        "facts": random.choice(facts)
    }


# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------

if "case" not in st.session_state:
    st.session_state.case = generate_case()

if "chat" not in st.session_state:
    st.session_state.chat = []

case = st.session_state.case


# -------------------------------------------------
# CASE DETAILS
# -------------------------------------------------

st.header(translate_text("Case Details", language))

st.write("**Case:**", translate_text(case.get("case","Unavailable"), language))
st.write("**Party A:**", translate_text(case.get("partyA","Unavailable"), language))
st.write("**Party B:**", translate_text(case.get("partyB","Unavailable"), language))
st.write("**Facts:**", translate_text(case.get("facts","Unavailable"), language))


# -------------------------------------------------
# NEW CASE BUTTON
# -------------------------------------------------

if st.button("Generate New Case"):

    st.session_state.case = generate_case()
    st.session_state.chat = []

    st.rerun()


# -------------------------------------------------
# DISCUSSION AREA
# -------------------------------------------------

st.header(translate_text("Negotiation Discussion", language))

user_input = st.text_input(
    translate_text("Enter your mediation message", language)
)

if st.button("Send Message") and user_input:

    if language == "Marathi":
        user_input_ai = GoogleTranslator(source="mr", target="en").translate(user_input)
    else:
        user_input_ai = user_input

    st.session_state.chat.append(("User", user_input))

    mediator_reply = "Mediator response unavailable."

    if client:

        prompt = f"""
You are a professional mediator helping resolve disputes.

Case: {case['case']}
Party A: {case['partyA']}
Party B: {case['partyB']}
Facts: {case['facts']}

User message:
{user_input_ai}

Respond as a neutral mediator encouraging constructive negotiation.
"""

        try:

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )

            mediator_reply = response.output_text

        except:
            mediator_reply = "Mediator response error."

    mediator_reply = translate_text(mediator_reply, language)

    st.session_state.chat.append(("Mediator", mediator_reply))


# -------------------------------------------------
# CHAT DISPLAY
# -------------------------------------------------

for role, msg in st.session_state.chat:

    if role == "User":
        st.write(f"🧑 {msg}")
    else:
        st.write(f"⚖️ {msg}")


# -------------------------------------------------
# FINAL REPORT
# -------------------------------------------------

st.header(translate_text("Final Session Report", language))

if st.button("Generate Mediation Report"):

    conversation = ""

    for role, msg in st.session_state.chat:
        conversation += f"{role}: {msg}\n"

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
Both parties participated in negotiation discussions. Continued dialogue may help achieve settlement.
"""

    report = translate_text(report, language)

    st.write(report)


# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------

st.sidebar.header("Mediation Dashboard")

st.sidebar.write(
    "Messages exchanged:",
    len(st.session_state.chat)
)

if len(st.session_state.chat) > 6:
    st.sidebar.success("Negotiation progressing")
else:
    st.sidebar.info("Early stage mediation")]

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
    st.sidebar.info("Early stage discussion")"Family inheritance dispute",
"Real estate property dispute",
"Partnership conflict",
"Vendor payment dispute",
"Shareholder disagreement",
"Intellectual property conflict",
"Joint venture breakdown"

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

def generate_case():

    case_type = random.choice(case_types)

    prompt = f"""
Create a realistic Alternative Dispute Resolution mediation case.

Case Type: {case_type}

Provide output in this format:

Title:
Party A:
Party B:
Facts:
Hidden Facts:

Make the facts different every time.
"""

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[
            {"role":"system","content":"You create legal mediation scenarios"},
            {"role":"user","content":prompt}
        ]

    )

    text = response.choices[0].message.content

    case = {}

    for line in text.split("\n"):

        if "Title:" in line:
            case["title"] = line.replace("Title:","").strip()

        if "Party A:" in line:
            case["party_a"] = line.replace("Party A:","").strip()

        if "Party B:" in line:
            case["party_b"] = line.replace("Party B:","").strip()

        if "Facts:" in line:
            case["facts"] = line.replace("Facts:","").strip()

        if "Hidden Facts:" in line:
            case["hidden_facts"] = line.replace("Hidden Facts:","").strip()

    return case

# ---------------- SESSION STATE ----------------

if "case" not in st.session_state:

    case = generate_case()

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

st.write("**Case:**", translate_text(case.get("case","No case available"), language))

st.write(
    "**Party A:**",
    translate_text(case.get("partyA","Information unavailable"), language)
)

st.write(
    "**Party B:**",
    translate_text(case.get("partyB","Information unavailable"), language)
)

st.write(
    "**Facts:**",
    translate_text(case.get("facts","Facts not provided"), language)
)

# ---------------- EVIDENCE PANEL ----------------

st.sidebar.subheader("Evidence")

if st.sidebar.button("Reveal Evidence"):
    st.sidebar.write(case.get("hidden_facts","No hidden facts"))

st.divider()

# ---------------- CHAT HISTORY ----------------

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------------- USER INPUT ----------------

user_input = st.text_input(translate_text("Your message", language))

if language == "Marathi":
    user_input_for_ai = GoogleTranslator(source='mr', target='en').translate(user_input)
else:
    user_input_for_ai = user_input

if user_input:

    # Display user message immediately
    st.chat_message("user").write(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("Mediator thinking..."):

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

    # Show AI message immediately
    st.chat_message("assistant").write(ai_reply)

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_reply
    })
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

    st.subheader(translate_text("Final Session Report", language))

report = f"""
Case Summary:
{case.get["case"]}

Discussion Points:
{discussion_summary}

Outcome:
{resolution}
"""

translated_report = translate_text(report, language)

st.write(translated_report)
