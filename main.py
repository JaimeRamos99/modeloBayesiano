
import hug
import modelo_bayesiano


@hug.get("/"/"")
def messages():
    return "hola"
