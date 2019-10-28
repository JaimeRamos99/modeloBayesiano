
import hug
import modelo_bayesiano


@hug.get("/getmessages/{id}")
def messages(id: hug.types.text):
    return modelo_bayesiano.getreputation(id)
