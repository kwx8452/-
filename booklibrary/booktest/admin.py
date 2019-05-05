from django.contrib import admin
from .models import Book,BorrowMessage,StudentUser,HotPic,Message
# Register your models here.
admin.site.register(BorrowMessage)
admin.site.register(Book)
admin.site.register(StudentUser)
admin.site.register(HotPic)
admin.site.register(Message)