import json
import random

class CaseGenerator:

    def __init__(self):
        with open("cases.json") as f:
            self.cases = json.load(f)

    def generate_case(self):

        case = random.choice(self.cases)

        return {
            "title": case["title"],
            "category": case["category"],
            "party_a": case["party_a"],
            "party_b": case["party_b"],
            "facts": case["facts"],
            "hidden_facts": case["hidden_facts"]
        }
    
    from personality_engine import PersonalityEngine

personality_engine = PersonalityEngine()

def generate_case():

    case = random.choice(self.cases)

    case["personality_a"] = personality_engine.assign()
    case["personality_b"] = personality_engine.assign()

    return case