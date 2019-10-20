import requests
import hug
import datetime
import json


@hug.get('/getmessages')
def getmessages(id: hug.type.number):
    responseP = requests.get("https://api-rest-botic.herokuapp.com/api/patients")
    responseG = requests.get("https://api-rest-botic.herokuapp.com/api/goals")
    resonseM = requests.get("https://api-rest-botic.herokuapp.com/api/messages")
    if (responseG.status_code == 200):


def EstadoDeMetas(id, responseG):
    if (responseG.status_code == 200):
        for i in responseG:
            if(id == i["_id"] and i["status"] == "1"):
                historialmetascumplidas = historialmetascumplidas + 1
            elif(id == i["_id"] and i["status"] == "0"):
                historialmetasincumplidas = historialmetasincumplidas + 1

    return historialmetascumplidas, historialmetasincumplidas, ultimameta,


def ultimaMeta(MetaFecha, ResponseG):
    ultimaFecha = MetaFecha
    for i in ResponseG:
        if(i["fechacumplida"] > ultimaFecha):
            ultimaFecha = i["fechacumplida"]
    return ultimafecha


def reputationBayesianModel(r, s,  a, w):
    return (r+w*a)/(r+s+w)


def RulesModel(hisorialmetascumplidas, historialmetasincumplidas, ultimaMeta,
               numeroDeMensajesMetaAnterior, numerodemensajespromedio,  r,  s):
    if(hisorialmetascumplidas >= historialmetasincumplidas and ultimaMeta is
       True and numeroDeMensajesMetaAnterior <= numerodemensajespromedio):
        r = r+1
    elif(hisorialmetascumplidas >= historialmetasincumplidas and ultimaMeta
         is True and numeroDeMensajesMetaAnterior > numerodemensajespromedio):
        r = r+1
    elif(hisorialmetascumplidas >= historialmetasincumplidas and ultimaMeta is
         False and numeroDeMensajesMetaAnterior <= numerodemensajespromedio):
        r = r+1
    elif(hisorialmetascumplidas >= historialmetasincumplidas and ultimaMeta is
         False and numeroDeMensajesMetaAnterior > numerodemensajespromedio):
        s = s+1
    elif(hisorialmetascumplidas < historialmetasincumplidas and ultimaMeta is
         True and numeroDeMensajesMetaAnterior <= numerodemensajespromedio):
        r = r+1
    elif(hisorialmetascumplidas < historialmetasincumplidas and ultimaMeta is
         True and numeroDeMensajesMetaAnterior > numerodemensajespromedio):
        s = s+1
    elif(hisorialmetascumplidas < historialmetasincumplidas and ultimaMeta is
         False and numeroDeMensajesMetaAnterior <= numerodemensajespromedio):
        s = s+1
    elif(hisorialmetascumplidas < historialmetasincumplidas and ultimaMeta is
         False and numeroDeMensajesMetaAnterior > numerodemensajespromedio):
        s = s+1

    return r, s


def actualizarRandS(r, s, id):
    req = None
    responsebody{'_id': id, 'r': r, 's': s}
    try
    req = requests.put("https://api-rest-botic.herokuapp.com/api/bayesianModel",
                       params=[json.dumps(responsebody)])
    if req.status_code != 200:
        print(req.text)
        raise Exception('Recieved non 200 response while sending response to CFN.')
        return
    except requests.exceptions.RequestException as e:
        if (req is not None):
            print(req.text)
        print(e)
        raise
