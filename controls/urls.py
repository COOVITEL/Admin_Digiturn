from django.urls import path, include
from . import views
from . import graficts


urlpatterns = [
    path("", views.login, name="login"),
    path("user-logout", views.user_logout, name="user-logout"),
    path("administrables", views.Admin, name="admin"),
    path("dates_digiturns", views.DatesDigiTurn, name="dates"),
    path("download_dates", views.downloadDates, name="download"),
    path("update_date_digiturn/<int:id>", views.updateTurn, name="updateTurn"),
    path("estadisticas", views.estadisticas, name="estadisticas"),
    path("plot/", graficts.plot, name="plot"),
    path("typesTurns", graficts.typesTurns, name="types"),
    path("quality", graficts.qualitifyTurns, name="qualitify"),
]