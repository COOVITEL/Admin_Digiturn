from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, CreateUserForm, Scores
from django.contrib.auth.models import auth
from django.contrib import messages
import pandas as pd
from datetime import datetime
import requests
import os



def login(request):
    """"""
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("admin")

    form2 = CreateUserForm()
    if request.method == 'POST':
        form2 = CreateUserForm(request.POST)
        if form2.is_valid():
            form2.save()
            return redirect("login")

    context = {'loginform': form,
               'registerform': form2}
    
    return render(request, 'authentication/login.html', context)

def user_logout(request):
    auth.logout(request)
    return redirect('login')

# Render the options controls
@login_required(login_url="login")
def Admin(request):
    return render(request, 'options.html')

@login_required(login_url="login")
def downloadDates(request):
    response = requests.get("http://192.168.1.16:8005/turns/api/v1/turns/")
    dates = response.json()

    df = pd.DataFrame(dates)
    """
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='openpyxl')
    df.to_excel(writer, index=False)
    writer.close()
    xlsx_data = output.getvalue()

    response = HttpResponse(xlsx_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=datos.xlsx'
    return response
    """
    df.to_excel('static/images/datos.xlsx', index=False)

    file_path = os.path.join('datos.xlsx')
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    else:
        return redirect("admin")
    

@login_required(login_url="login")
def DatesDigiTurn(request):
    response = requests.get("http://192.168.1.16:8005/turns/api/v1/turns/")
    list_dates = response.json()

    list_dates = [item for item in list_dates if item.get("score_time") == "empty" and len(str(item.get("phone"))) == 10 and item.get("state") != "qualifying"]

    city = request.GET.get("city")
    date = request.GET.get("fecha")
    now = datetime.now()
    day = now.day
    
    if city is not None:
        list_dates = [item for item in list_dates if item.get("city") == city]
    if date == "1":
        list_dates = [item for item in list_dates if str(item.get("date")[-2:]) == str(day)]
    if date == "3":
        list_dates = [item for item in list_dates if int(item.get("date")[-2:]) >= int(day - 3)]
    if date == "7":
        list_dates = [item for item in list_dates if int(item.get("date")[-2:]) >= int(day - 7)]
    
    context = {
        "dates": list_dates,
        "date": day
    }        

    return render(request, "dates.html", context=context)

@login_required(login_url="login")
def updateTurn(request, id):
    """"""
    form = Scores()
    response = requests.get(f"http://192.168.1.16:8005/turns/api/v1/turns/{id}/")
    turn = response.json()
    copy = turn
    if request.method == "GET":
        render(request, "updatescore.html", {"turn": turn, "scores": form})
        copy["state"] = "qualifying"
        requests.put(f"http://192.168.1.16:8005/turns/api/v1/turns/{id}/", data=copy)
    
    if request.method == "POST":
        form = Scores(request.POST)
        if form.is_valid():
            if copy["state"] == "by_call":
                return redirect("dates")
            copy["score_time"] = request.POST.get('time')
            copy["score_service"] = request.POST.get('attention')
            copy["score_att"] = request.POST.get('service')
            copy["score_recommen"] = request.POST.get('recomment')
            copy["state"] = "by_call"
            requests.put(f"http://192.168.1.16:8005/turns/api/v1/turns/{id}/", data=copy)
            messages.success(request, "Las calificaciones se actualizaron de forma correcta!")
            return redirect("dates")

    return render(request, "updatescore.html", {"turn": turn, "scores": form})

def estadisticas(request):
    return render(request, "estadisticas.html")
     