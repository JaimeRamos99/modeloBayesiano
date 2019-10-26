
import hug
import modelo_bayesiano


@hug.get("/getmessages")
def messages(id: hug.types.text):
    print(modelo_bayesiano.getmessages(id))
