import random

class PersonalityEngine:

    def __init__(self):

        self.personalities = [

        "Aggressive litigant",
        "Emotional party",
        "Logical corporate counsel",
        "Defensive employee",
        "Strategic negotiator"

        ]

    def assign(self):

        return random.choice(self.personalities)