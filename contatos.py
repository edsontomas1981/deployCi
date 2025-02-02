class Contato():
    def __init__(self, phone, nome):
        self.nome = nome
        self.phone = phone
        self.messages = {'sent':[],'received':[]}
        self.state = 'aberto'

    def __str__(self):
        return f"[Nome: {self.nome}, Telefone: {self.phone}], {self.messages}"
    
    def __repr__(self):
        return f"[Nome: {self.nome}, Telefone: {self.phone}],  {self.messages} "
    
    def add_messages_sent(self, message):
        self.messages['sent'].append(message)

    def set_state(self, state):
        self.state = state