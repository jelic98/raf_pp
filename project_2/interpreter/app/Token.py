class Token():
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return "<{} {}>".format(self.token_type, self.value)