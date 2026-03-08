class NegotiationEngine:

    def __init__(self):

        self.batna_a = "Proceed to arbitration"
        self.batna_b = "File lawsuit"

    def get_batna(self):

        return {

        "Party A BATNA":self.batna_a,
        "Party B BATNA":self.batna_b

        }