from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class StudentUser(User):
    college = models.CharField(max_length=20)
    studentnum = models.IntegerField()



class Book(models.Model):
    isbn = models.IntegerField()
    bname = models.CharField(max_length=20)
    author = models.CharField(max_length=20)
    publish_date = models.DateField()
    publisher = models.CharField(max_length=20)

    def __str__(self):
        return self.bname



class BorrowMessage(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    person = models.ForeignKey('StudentUser', on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()
    status = models.BooleanField()

    def __str__(self):
        return self.book


class HotPic(models.Model):
    name = models.CharField(max_length=20)
    pic = models.ImageField(upload_to='hotpic')
    index = models.IntegerField(unique=True)

    def __str__(self):
        return self.name


from tinymce.models import HTMLField
class Message(models.Model):
    title = models.CharField(max_length=20)
    message = HTMLField()
    def __str__(self):
        return self.title