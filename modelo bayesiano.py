import requests
import hug


@hug.get('/getmessages')
def getmessages(id: int):
    responseP = requests.get("https://api-rest-botic.herokuapp.com/api/patients")
    responseG = requests.get("https://api-rest-botic.herokuapp.com/api/goals")
    resonseM = requests.get("https://api-rest-botic.herokuapp.com/api/messages")
    if (responseP.status_code == 200):
        for i in responseP.json():
            if (id == i["_id"]):
                return


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
