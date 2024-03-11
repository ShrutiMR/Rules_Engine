class Customer:
    def __init__(self, name, state='new_state') -> None:
        self.name = name
        self.state = state

    def set_state(self, new_state):
        self.state = new_state