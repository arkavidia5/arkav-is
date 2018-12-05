from django.apps import apps
from django.contrib import admin

# Register your models here.


app = apps.get_app_config('quiz')

for model_name, model in app.models.items():
    admin.site.register(model)