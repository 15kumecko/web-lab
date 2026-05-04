class Adaptee:
    def specific_request(self):
        return "Legacy system data"

class Adapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def request(self):
        return self.adaptee.specific_request()
