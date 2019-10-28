
import hug
import modelo_bayesiano


@hug.get("/getmessages/{id}")
def messages(id: str):
    i = modelo_bayesiano.getreputation(id)
    return i
