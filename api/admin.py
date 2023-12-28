from django.contrib import admin
from .models import CustomUser, DateModel, TimeEntryModel, Admin, Transaction, TSN, UserGame,Account,Earn_Point

admin.site.register(CustomUser)
admin.site.register(DateModel)
admin.site.register(TimeEntryModel)
admin.site.register(Admin)
admin.site.register(Transaction)
admin.site.register(TSN)
admin.site.register(UserGame)
admin.site.register(Account)
admin.site.register(Earn_Point)
# admin.site.register(Win_Percent)



