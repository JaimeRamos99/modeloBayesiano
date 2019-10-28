
import hug


@hug.get("/")
def messages():
    return "hola"
