class ProbabilityEngine:

    def __init__(self):

        self.settlement_probability = 50
        self.trust_level = 50
        self.conflict_level = 50

    def update(self, action):

        if "clarify" in action.lower():

            self.trust_level += 10
            self.settlement_probability += 5

        if "settlement" in action.lower():

            self.settlement_probability += 12

        if "threat" in action.lower():

            self.conflict_level += 15
            self.settlement_probability -= 10

        return {

        "settlement_probability":self.settlement_probability,
        "trust_level":self.trust_level,
        "conflict_level":self.conflict_level

        }