from django.urls import path
from .views import diseaseNodisease


urlpatterns = [
    path('prediction/', diseaseNodisease),
]