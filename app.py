import streamlit as st

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="ADR Mediation Tool", layout="centered")

st.title("ADR Mediation Simulation Tool")

# -----------------------------
# Language Selection
# -----------------------------
language = st.sidebar.selectbox(
    "Select Language",
    ["English", "Marathi"]
)

# -----------------------------
# Translation Dictionary
# -----------------------------
translations = {
    "Payment dispute between contractor and homeowner":
        "कंत्राटदार आणि घरमालक यांच्यातील देयक वाद",

    "Land boundary disagreement between neighbors":
        "शेजाऱ्यांमधील जमिनीच्या सीमावाद",

    "The contractor completed work but the homeowner claims delays and poor finishing.":
        "कंत्राटदाराने काम पूर्ण केले पण घरमालक विलंब आणि कामाच्या गुणवत्तेबद्दल तक्रार करतो.",

    "Survey documents show unclear boundary markings between both properties.":
        "सर्वेक्षण कागदपत्रांमध्ये दोन्ही मालमत्तांमधील सीमा स्पष्ट नाही.",

    "Reveal Evidence":
        "पुरावे दाखवा",

    "Evidence hidden. Try negotiating first.":
        "पुरावे लपवले आहेत. आधी वाटाघाटी करण्याचा प्रयत्न करा.",

    "New Evidence Revealed":
        "नवीन पुरावे उघड झाले",

    "Negotiation":
        "वाटाघाटी",

    "Mediator Suggestion":
        "मध्यस्थाची सूचना",

    "Reset Evidence":
        "पुरावे रीसेट करा"
}

# -----------------------------
# Translation Function
# -----------------------------
def translate_text(text, lang):
    if lang == "Marathi":
        return translations.get(text, text)
    return text


# -----------------------------
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
