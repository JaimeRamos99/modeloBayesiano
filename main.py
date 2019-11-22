import hug
import modelo_bayesiano
import requests
import random


def mensajesInicioPregunta(requestM):
    mensajesInicioPreguntas = []
    for i in requestM.json():
        if(i["classMessage"] == "GenericoInicio" and i["isQorA"]
           == "Pregunta"):
            mensajesInicioPreguntas.append(i)
    return mensajesInicioPreguntas


def mensajesFinalesPregunta(requestM):
    mensajesFinalesPreguntas = []
    for i in requestM.json():
        if(i["classMessage"] == "GenericoFinal" and i["isQorA"]
           == "Pregunta"):
            mensajesFinalesPreguntas.append(i)
    return mensajesFinalesPreguntas


def mensajespreguntas(idpaciente, requestM, requestG, reputacionPaciente):
    Preguntas = []
    for j in requestG.json():
        if(j["pat"] == idpaciente and j["state"] == "2"):
            MInicio = mensajesInicioPregunta(requestM)
            MFinales = mensajesFinalesPregunta(requestM)
            MInicioKindorAcertive = []
            MFinalesKindorAcertive = []
            cont1 = 0
            cont2 = 0
            cont3 = 0
            cont4 = 0
            if(reputacionPaciente >= 0.40):
                for i in MInicio:
                    if(i["typeMessage"] == "kind"):
                        MInicioKindorAcertive.append(MInicio[cont1])
                        cont1 = cont1 + 1
                for i in MFinales:
                    if(i["typeMessage"] == "kind"):
                        MFinalesKindorAcertive.append(MFinales[cont2])
                        cont2 = cont2 + 1
            else:
                for i in MInicio:
                    if(i["typeMessage"] == "assertive"):
                        MInicioKindorAcertive.append(MInicio[cont3])
                        cont3 = cont3 + 1
                for i in MFinales:
                    if(i["typeMessage"] == "assertive"):
                        MFinalesKindorAcertive.append(MFinales[cont4])
                        cont4 = cont4 + 1
            if(len(MInicioKindorAcertive) != 0 and len(MFinales) != 0):
                Preguntas.append({"pregunta": MInicioKindorAcertive[random.randint(
                                  0, len(MInicioKindorAcertive)-1)]
                                  ["description"]+" " + j["description"]+" " +
                                  MFinalesKindorAcertive[random.randint(0,
                                                                        len(MFinalesKindorAcertive)
                                                                        - 1)]
                                  ["description"],
                                  "idmeta": j["_id"]})
    return Preguntas


def mensajesRespuestaPositiva(requestM):
    mensajesRespuestasPositivas = []
    for i in requestM.json():
        if(i["classMessage"] == "GenericoInicio" and i["isQorA"]
           == "RespuestaPositiva"):
            mensajesRespuestasPositivas.append(i)
    return mensajesRespuestasPositivas


def mensajesRespuestaNegativa(requestM):
    mensajesRespuestasNegativas = []
    for i in requestM.json():
        if(i["classMessage"] == "GenericoInicio" and i["isQorA"]
                == "RespuestaNegativa"):
            mensajesRespuestasNegativas.append(i)
    return mensajesRespuestasNegativas


def mensajesBienvenida(requestM, reputacionDelModelo):
    mensajesBienvenidas = []
    if(reputacionDelModelo >= 0.40):
        for i in requestM.json():
            if(i["classMessage"] == "GenericoInicio" and i["isQorA"] == "Saludos" and
               i["typeMessage"] == "kind"):
                mensajesBienvenidas.append(i)
    else:
        for i in requestM.json():
            if(i["classMessage"] == "GenericoInicio" and i["isQorA"] == "Saludos" and
               i["typeMessage"] == "assertive"):
                mensajesBienvenidas.append(i)
    saludos = mensajesBienvenidas[random.randint(0, len(mensajesBienvenidas) - 1)]
    return saludos


def mensajesDespedida(requestM, reputacionDelModelo):
    mensajesDespedidas = []
    if(reputacionDelModelo >= 0.40):
        for i in requestM.json():
            if(i["classMessage"] == "GenericoInicio" and i["isQorA"] == "Despedidas" and
               i["typeMessage"] == "kind"):
                mensajesDespedidas.append(i)
    else:
        for i in requestM.json():
            if(i["classMessage"] == "GenericoInicio" and i["isQorA"] == "Despedidas" and
               i["typeMessage"] == "assertive"):
                mensajesDespedidas.append(i)
    despedida = mensajesDespedidas[random.randint(0, len(mensajesDespedidas) - 1)]
    return despedida


def mensajesRespuesta(idpaciente, requestM, requestG, reputacionDelModelo):
    RPositivas = []
    RNegativas = []
    for J in requestG.json():
        if(idpaciente == J["pat"] and J["state"] == "2"):
            mensajesrespuestapositiva = mensajesRespuestaPositiva(requestM)
            mensajesrespuestanegativa = mensajesRespuestaNegativa(requestM)
            MRPKindorAssertive = []
            MRNKindorAssertive = []
            if(reputacionDelModelo >= 0.40):
                for i in mensajesrespuestapositiva:
                    if(i["typeMessage"] == "kind"):
                        MRPKindorAssertive.append(i)

                for i in mensajesrespuestanegativa:
                    if(i["typeMessage"] == "kind"):
                        MRNKindorAssertive.append(i)

            else:
                for i in mensajesrespuestapositiva:
                    if(i["typeMessage"] == "assertive"):
                        MRPKindorAssertive.append(i)

                for i in mensajesrespuestanegativa:
                    if(i["typeMessage"] == "assertive"):
                        MRNKindorAssertive.append(i)
            if(len(MRPKindorAssertive) != 0):
                RPositivas.append({"RespuestaPositiva":
                                   MRPKindorAssertive[random.randint(0,
                                                                     len(MRPKindorAssertive)
                                                                     - 1)]["description"],
                                   "idmeta": J["_id"]})
            if(len(MRNKindorAssertive) != 0):
                RNegativas.append({"RespuestaNegativa":
                                   MRNKindorAssertive[random.randint(0,
                                                                     len(MRNKindorAssertive)
                                                                     - 1)]["description"],
                                   "idmeta": J["_id"]})

    return RPositivas, RNegativas


@hug.get('/getmessages/{id}')
def messages(id: str):
    requestM = requests.get("https://api-rest-botic.herokuapp.com/api/messages")
    responseG = requests.get("https://api-rest-botic.herokuapp.com/api/goals")
    if(len(responseG.json()) != 0):
        reputacionP = modelo_bayesiano.getreputation(id)
    else:
        reputacionP = 0.40
    MPreguntas = mensajespreguntas(id, requestM, responseG, reputacionP)
    MRespuestasP, MRespuestasN = mensajesRespuesta(id, requestM, responseG, reputacionP)
    saludos = mensajesBienvenida(requestM, reputacionP)
    despedida = mensajesDespedida(requestM, reputacionP)
    return MPreguntas, MRespuestasN, MRespuestasP, saludos, despedida


print(messages("5dd05132d15d7100175f0a02"))
