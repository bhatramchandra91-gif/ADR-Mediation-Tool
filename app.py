import streamlit as st
import random
from openai import OpenAI
from deep_translator import GoogleTranslator

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(page_title="ADR Mediation Simulator", layout="wide")

# ---------------------------------------------------
# LANGUAGE SETTINGS
# ---------------------------------------------------

st.sidebar.header("Language Settings")

language = st.sidebar.selectbox(
    "Select Language",
    ["English", "Marathi"]
)

# ---------------------------------------------------
# TRANSLATION FUNCTION
# ---------------------------------------------------

def translate_text(text, lang):
    if lang == "English":
        return text
    try:
        return GoogleTranslator(source='auto', target='mr').translate(text)
    except:
        return text


# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title(translate_text("⚖️ AI ADR Mediation Training Simulator", language))

# ---------------------------------------------------
# OPENAI CLIENT
# ---------------------------------------------------

client = None
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.warning("OpenAI API key not found. AI mediator responses will be disabled.")

# ---------------------------------------------------
# RANDOM CASE GENERATOR
# ---------------------------------------------------

case_types = [
    "Employment Termination",
    "Startup Equity Dispute",
    "Partnership Conflict",
    "Landlord Tenant Dispute",
    "Family Business Disagreement",
    "Intellectual Property Conflict",
    "Contract Breach",
    "Vendor Payment Dispute"
]

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
