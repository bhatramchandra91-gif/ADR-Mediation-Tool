class ScoringEngine:

    def __init__(self):

        self.score = 0
        self.good_decisions = []
        self.bad_decisions = []

    def evaluate(self, action):

        if action == "Ask clarifying questions":

            self.score += 8
            self.good_decisions.append(action)

        elif action == "Suggest compromise":

            self.score += 10
            self.good_decisions.append(action)

        elif action == "Escalate dispute":

            self.score -= 10
            self.bad_decisions.append(action)

        elif action == "Private caucus":

            self.score += 6
            self.good_decisions.append(action)

    def summary(self):

        return {
            "score": self.score,
            "good": self.good_decisions,
            "bad": self.bad_decisions
        }