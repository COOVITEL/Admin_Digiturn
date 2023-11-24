from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.shortcuts import HttpResponse
import matplotlib.pyplot as plt
import requests
import io

URL = "http://192.168.1.16:8005/turns/api/v1/turns/"

def turns_counts(turns, key, value):
    return len([date for date in turns if date.get(key) == value])

def plot(request):
    try:
        response = requests.get(URL)
        turns = response.json()
    except requests.exceptions.RequestException as e:
        return HttpResponse("Error al obtener datos de la URL", status=500)
    
    bar = turns_counts(turns, "city", "Barranquilla")
    bog = turns_counts(turns, "city", "Bogotá")
    buc = turns_counts(turns, "city", "Bucaramanga")
    cal = turns_counts(turns, "city", "Cali")
    cuc = turns_counts(turns, "city", "Cúcuta")
    iba = turns_counts(turns, "city", "Ibagué")
    man = turns_counts(turns, "city", "Manizales")
    med = turns_counts(turns, "city", "Medellin")
    tun = turns_counts(turns, "city", "Tunja")    
    total = len(turns)
    
    fig, axes = plt.subplots()
    plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.3)

    offices = ['B/quilla','Bogotá','B/manga','Cali','Cúcuta','Ibagué','Manizales','Medellin','Tunja', 'Total']

    counts = [bar, bog, buc, cal, cuc, iba, man, med, tun, total]
    
    bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:pink']

    axes.bar(offices, counts, color=bar_colors, width=0.5)
    
    #for i, j in zip(offices, counts):
    #    plt.text(i, j, str(j), ha='center', va='bottom')
    
    axes.set_ylabel("Numero de turnos", fontsize=18)
    axes.set_title("Turnos Sucursales", fontsize=20)
    axes.set_xticklabels(offices, rotation=35)  
    
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    
    fig.clear()
    
    response['Content-Length'] = str(len(response.content))
    
    return response

def typesTurns(request):
    """"""
    try:
        response = requests.get(URL)
        turns = response.json()
    except requests.exceptions.RequestException as e:
        return HttpResponse("Error al obtener datos de la URL", status=500)
    
    caja = turns_counts(turns, "type2", "Caja")
    cre = turns_counts(turns, "type2", "Crédito")
    afi = turns_counts(turns, "type2", "Afiliación")
    aho = turns_counts(turns, "type2", "Ahorro")
    seg = turns_counts(turns, "type2", "Seguro")
    aux = turns_counts(turns, "type2", "Auxilio")
    est = turns_counts(turns, "type2", "Estado")
    otr = turns_counts(turns, "type2", "Otros")

    fig, axes = plt.subplots()
    plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.3)

    types = ['Caja', 'Crédito', 'Afiliación', 'Ahorro', 'Seguro', 'Auxilio', 'Estado Cuenta', 'Otros']
    counts = [caja, cre, afi, aho, seg, aux, est, otr]
    bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:pink']
    
    axes.bar(types, counts, color=bar_colors, width=0.5)
    
    #for x, y in zip(types, counts):
    #    plt.text(x, y, str(y), ha='center', va='bottom')

    axes.set_ylabel("Numero de turnos", fontsize=18)
    axes.set_title("Tipos de turnos", fontsize=20)
    axes.set_xticklabels(types, rotation=35)

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)

    response = HttpResponse(buf.getvalue(), content_type='image/png')

    fig.clear()
    response['Content-Length'] = str(len(response.content))
    return response

def qualitifyTurns(request):
    """"""
    try:
        response = requests.get(URL)
        turns = response.json()
    except requests.exceptions.RequestException as e:
        return HttpResponse("Error al obtener datos de la URL", status=500)


    qualitify = len([data for data in turns if data.get("score_time") != "empty"])
    emply = len([data for data in turns if data.get("score_time") == "empty"])
    sms = len([data for data in turns if data.get("sms_send") == "send"])
    qualitify_digi = len([data for data in turns if data.get("score_tiem") != "empty" and data.get("sms_send") == "pending" and data.get("state") != "by_call"])
    qualitify_sms = len([data for data in turns if data.get("score_time") != "empty" and data.get("sms_send") == "send"])
    qualitify_by_call = len([data for data in turns if data.get("socre_time") != "empty" and data.get("state") == "by_call"])
    by_call_failed = len([data for data in turns if data.get("state") == "qualitify"])
    total = len([date for date in turns])

    fig, axes = plt.subplots()
    plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.3)

    scores = ['Calificados',
              'Sin calificar',
              'Sms enviado',
              'Calificado Digiturno',
              'Calificado SMS',
              'Calificado Call',
              'Call fallido',
              'Total']
    
    counts = [qualitify, emply, sms, qualitify_digi, qualitify_sms, qualitify_by_call, by_call_failed, total]

    bar_colors = ['tab:red', 'tab:blue', 'tab:green', 'tab:orange', 'tab:pink']
    
    axes.bar(scores, counts, color=bar_colors, width=0.5)
    
    for a, b in zip(scores, counts):
        plt.text(a, b, str(b), ha='center', va='bottom')

    axes.set_ylabel("Numero de turnos", fontsize=18)
    axes.set_title("Estado calificaciones", fontsize=20)
    axes.set_xticklabels(scores, rotation=35)

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)

    response = HttpResponse(buf.getvalue(), content_type='image/png')

    fig.clear()
    response['Content-Length'] = str(len(response.content))
    return response