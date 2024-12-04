"""
URL configuration for energetic_dashboard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from .views import energy_data_list, add_energy_data

urlpatterns = [
    path('', views.index, name='index'),
    path('show_data/', views.show_data, name='show_data'),

    # API
    path('api/energy-data/', energy_data_list, name='energy_data_list'),  # GET
    path('api/energy-data/<int:id>/', views.get_energy_data, name='get_energy_data'), # GET BY ID
    path('api/energy-data/add/', add_energy_data, name='add_energy_data'),  # POST
    path('api/energy-data/update/<int:id>/', views.update_energy_data, name='update_energy_data'), # PUT
    path('api/energy-data/delete/<int:id>/', views.delete_energy_data, name='delete_energy_data'), # DELETE
]
