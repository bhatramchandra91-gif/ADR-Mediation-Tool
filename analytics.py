class Analytics:

    def generate_report(self, score):

        if score > 40:

            level = "Advanced Mediator"

        elif score > 20:

            level = "Intermediate Mediator"

        else:

            level = "Beginner"

        return {

        "Mediator Skill Level":level,

        "Recommendations":[
        "Use more open-ended questions",
        "Identify emotional triggers",
        "Encourage collaborative settlement"
        ]

        }