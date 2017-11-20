from django.contrib import admin
from .models import Hospuser
from .models import Subject
from .models import Cancertype
from .models import Sample	

# Register your models here.

admin.site.register(Hospuser)
admin.site.register(Subject)
admin.site.register(Cancertype)
admin.site.register(Sample)


