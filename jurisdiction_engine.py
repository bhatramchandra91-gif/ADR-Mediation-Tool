class JurisdictionEngine:

    def __init__(self):

        self.jurisdictions = {

        "India":{
        "law":"Arbitration and Conciliation Act, 1996",
        "style":"Interest-based mediation"
        },

        "International":{
        "law":"UNCITRAL Model Law",
        "style":"Facilitative mediation"
        }

        }

    def get_jurisdiction(self, name):

        return self.jurisdictions.get(name)