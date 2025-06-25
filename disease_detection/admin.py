from django.contrib import admin
from .models import DiseaseIncident

from django.contrib import admin
from .models import users_data

admin.site.register(users_data)


admin.site.register(DiseaseIncident)