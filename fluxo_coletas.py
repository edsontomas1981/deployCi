def verifica_state(state):

    match state:
        case "SP":
            return "São Paulo"
        case "RJ":
            return "Rio de Janeiro"
        case "MG":
            return "Minas Gerais"
        case "ES":
            return "Espírito Santo"
        case _:
            return "Outros Estados"
        
        