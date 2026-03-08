import random

class TwistEngine:

    def __init__(self):

        self.twists = [

        "A new email appears contradicting earlier testimony",

        "A financial document reveals hidden liabilities",

        "A witness testimony changes the timeline",

        "One party becomes emotionally distressed",

        "A legal clause emerges affecting settlement",

        "External regulatory pressure appears",

        "A third party claims contractual rights"

        ]

    def generate_twist(self):

        return random.choice(self.twists)