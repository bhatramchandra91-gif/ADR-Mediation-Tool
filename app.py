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
    st.sidebar.info("Early stage discussion")# -----------------------------
# Case Data
# -----------------------------
cases = [
    {
        "case": "Payment dispute between contractor and homeowner",
        "facts": "The contractor completed work but the homeowner claims delays and poor finishing."
    },
    {
        "case": "Land boundary disagreement between neighbors",
        "facts": "Survey documents show unclear boundary markings between both properties."
    }
]

# -----------------------------
# Case Selection
# -----------------------------
case_names = [c["case"] for c in cases]

selected_case = st.selectbox(
    "Select a Case",
    case_names
)

# Get selected case dictionary
case = next(c for c in cases if c["case"] == selected_case)

# -----------------------------
# Display Case
# -----------------------------
st.subheader("Case Description")

st.write(
    translate_text(case["case"], language)
)

# -----------------------------
# Evidence Phase
# -----------------------------
st.subheader("Evidence Phase")

if "evidence_revealed" not in st.session_state:
    st.session_state.evidence_revealed = False

if st.button(translate_text("Reveal Evidence", language)):
    st.session_state.evidence_revealed = True

if st.session_state.evidence_revealed:
    st.success(translate_text("New Evidence Revealed", language))
    st.write(
        translate_text(case["facts"], language)
    )
else:
    st.warning(
        translate_text("Evidence hidden. Try negotiating first.", language)
    )

# Reset Evidence Button
if st.button(translate_text("Reset Evidence", language)):
    st.session_state.evidence_revealed = False


# -----------------------------
# Negotiation Section
# -----------------------------
st.subheader(
    translate_text("Negotiation", language)
)

party_a = st.text_area("Party A Position")

party_b = st.text_area("Party B Position")

# -----------------------------
# Mediator Suggestion
# -----------------------------

if st.button("Generate Mediator Suggestion"):

    if party_a and party_b:
        st.subheader(
            translate_text("Mediator Suggestion", language)
        )

        st.write(
            "Consider a compromise where both parties adjust expectations and agree on a mutually acceptable resolution."
        )

    else:
        st.warning("Please enter both party positions.")
        
twists = [
    "New email evidence appears.",
    "Financial records contradict testimony.",
    "A witness changes the timeline.",
    "A hidden clause in the contract is revealed.",
    "One party becomes emotionally aggressive."
]

# ---------------- CASE GENERATOR ----------------

def generate_case():

    case_type = random.choice(case_types)

    if client:

        prompt = f"""
Create a realistic mediation dispute.

Case Type: {case_type}

Format:

Title:
Party A:
Party B:
Facts:
Hidden Facts:
"""

        try:

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":"You generate ADR mediation cases"},
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

        except:

            case = {}

    else:

        case = {}

    if not case:

        case = {
            "title": case_type,
            "party_a": "Party A claims unfair treatment.",
            "party_b": "Party B denies wrongdoing.",
            "facts": "A dispute arose between the parties.",
            "hidden_facts": "A confidential email may change the outcome."
        }

    case["personality_a"] = random.choice(personalities)
    case["personality_b"] = random.choice(personalities)

    return case

# ---------------- SESSION STATE ----------------

if "case" not in st.session_state:

    st.session_state.case = generate_case()
    st.session_state.messages = []
    st.session_state.turn = 0

    st.session_state.settlement_probability = 50
    st.session_state.trust_level = 50
    st.session_state.conflict_level = 50
    st.session_state.score = 0

case = st.session_state.case

# ---------------- NEW CASE BUTTON ----------------

if st.sidebar.button("Start New Case"):
    st.session_state.clear()
    st.rerun()

# ---------------- JURISDICTION ----------------

jurisdiction = st.sidebar.selectbox(
    "Jurisdiction",
    ["India","International"]
)

if jurisdiction == "India":
    law = "Arbitration and Conciliation Act, 1996"
else:
    law = "UNCITRAL Model Law"

st.sidebar.write("Applicable Law:", law)

# ---------------- MEDIATION METRICS ----------------

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

st.subheader(translate_text("Case Scenario", language))

st.write("**Case:**", translate_text(case.get("title",""), language))
st.write("**Party A:**", translate_text(case.get("party_a",""), language))
st.write("**Party B:**", translate_text(case.get("party_b",""), language))
st.write("**Facts:**", translate_text(case.get("facts",""), language))

# ---------------- EVIDENCE ----------------

st.subheader("Evidence Phase")

if "evidence_revealed" not in st.session_state:
    st.session_state.evidence_revealed = False

if st.button("Reveal Evidence"):
    st.session_state.evidence_revealed = True

if st.session_state.evidence_revealed:
    st.success("New Evidence Revealed")
    st.write(translate_text(case["facts"], language))
else:
    st.warning("Evidence hidden. Try negotiating first.")


# Negotiation Section
st.subheader("Negotiation")
party_a = st.text_area("Party A Position")
party_b = st.text_area("Party B Position")

# ---------------- CHAT HISTORY ----------------

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# ---------------- USER INPUT ----------------

user_input = st.chat_input(translate_text("Enter mediation message", language))

if user_input:

    st.chat_message("user").write(user_input)

    st.session_state.messages.append({
        "role":"user",
        "content":user_input
    })

    with st.spinner("Mediator thinking..."):

        prompt = f"""
Simulate mediation.

Party A personality: {case["personality_a"]}
Party B personality: {case["personality_b"]}

Mediator message:
{user_input}

Respond with:
Party A reaction
Party B reaction
Mediator observation
"""

        if client:

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role":"system","content":"You simulate mediation training"},
                    {"role":"user","content":prompt}
                ]
            )

            ai_reply = response.choices[0].message.content

        else:

            ai_reply = "AI mediator unavailable."

    st.chat_message("assistant").write(ai_reply)

    st.session_state.messages.append({
        "role":"assistant",
        "content":ai_reply
    })

    # ---------------- TWIST ENGINE ----------------

    if st.session_state.turn % 2 == 1:

        twist = random.choice(twists)

        twist_text = f"⚖️ Case Twist: {twist}"

        st.chat_message("assistant").write(twist_text)

        st.session_state.messages.append({
            "role":"assistant",
            "content":twist_text
        })

    # ---------------- SCORE UPDATE ----------------

    text = user_input.lower()

    if "settlement" in text:
        st.session_state.settlement_probability += 10
        st.session_state.score += 8

    if "clarify" in text:
        st.session_state.trust_level += 8
        st.session_state.score += 5

    if "threat" in text:
        st.session_state.conflict_level += 10
        st.session_state.settlement_probability -= 5

    st.session_state.turn += 1

# ---------------- FINAL REPORT ----------------

if st.session_state.turn >= 6:

    st.subheader(translate_text("Final Session Report", language))

    conversation = ""

    for msg in st.session_state.messages:
        conversation += msg["content"] + "\n"

    report = f"""
Case: {case.get("title")}

Discussion Summary:
{conversation}

Mediator Observation:
The mediation session progressed through multiple negotiation exchanges.
Further dialogue may help reach a mutually acceptable settlement.
"""

    st.write(translate_text(report, language))
