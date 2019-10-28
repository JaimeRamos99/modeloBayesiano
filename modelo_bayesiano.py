import requests


def ultimaMeta(MetaFecha, ResponseG):
    ultimaFecha = MetaFecha
    for i in ResponseG.json():
        if("complianceDate" in i):
            Date = i["complianceDate"]
            if(Date >= ultimaFecha):
                ultimaMeta = i
    return ultimaMeta


def VariablesReglas(responseG):
    historialmetascumplidas = 0
    historialmetasincumplidas = 0
    numerodemensajespromedio = 0
    if (responseG.status_code == 200):
        for i in responseG.json():
            if(i["state"] == "1"):
                historialmetascumplidas = historialmetascumplidas + 1
            elif(i["state"] == "0"):
                historialmetasincumplidas = historialmetasincumplidas + 1
            if(i["state"] == "1" or i["state"] == "0"):
                if("complianceDate" in i):
                    if(i["complianceDate"] is not None):
                        ultimameta = ultimaMeta(i["complianceDate"], responseG)
                if("nMessages" in i):
                    if(i["nMessages"] is not None):
                        numerodemensajespromedio = numerodemensajespromedio + \
                            int(float(i["nMessages"]))
        numerodemensajespromedio = numerodemensajespromedio / \
            (historialmetascumplidas + historialmetasincumplidas)
        if(ultimameta["state"] == "1"):
            list = historialmetascumplidas, historialmetascumplidas, True, \
                int(ultimameta["nMessages"]), numerodemensajespromedio
        else:
            list = historialmetascumplidas, historialmetascumplidas, False, \
                int(ultimameta["nMessages"]), numerodemensajespromedio

    return list


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
    responsebody = {'patient': id, 'r': r, 's': s}

    try:
        req = requests.put("https://api-rest-botic.herokuapp.com/api/bayesianModel",
                           json=responsebody)
        if req.status_code != 200:
            print(req.text)
            raise Exception('Recieved non 200 response while sending response to CFN.')
        return
    except requests.exceptions.RequestException as e:
        if (req is not None):
            print(req.text)
        print(e)
        raise


def getreputation(idpaciente):
    responseG = requests.get("https://api-rest-botic.herokuapp.com/api/goals")
    responseModel = requests.get("https://api-rest-botic.herokuapp.com/api/bayesianModel")
    a = 0.7
    w = 2
    if (responseG.status_code == 200 and responseModel.status_code == 200):
        listavariables = VariablesReglas(responseG)
        for i in responseModel.json():
            if(idpaciente == i["patient"]):
                r = int(i["r"])
                s = int(i["s"])

        r, s = RulesModel(listavariables[0], listavariables[1], listavariables[2],
                          listavariables[3], listavariables[4], r, s)
        reputacionDelModelo = reputationBayesianModel(r, s, a, w)
        actualizarRandS(r, s, idpaciente)
    else:
        print("status server != 200")
    return reputacionDelModelo


responseG = requests.get("https://api-rest-botic.herokuapp.com/api/patients")
responseModel = requests.get("https://api-rest-botic.herokuapp.com/api/bayesianModel")
print(getreputation("5d997dd8af8eb50017d94c8e"))
