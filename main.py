
import hug
import modelo_bayesiano


@hug.get('/getmessages/{id}')
def messages(id: str):
    i = modelo_bayesiano.getreputation("5d997dd8af8eb50017d94c8e")
    return i
