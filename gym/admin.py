from django.contrib import admin
from .models import Gym, Class, Plans, Trainer
# Register your models here.
admin.site.register(Gym)
admin.site.register(Class)
admin.site.register(Plans)
admin.site.register(Trainer)