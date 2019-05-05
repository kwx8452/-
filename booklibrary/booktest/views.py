from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from .models import Book,BorrowMessage,StudentUser,HotPic,Message
from django.core.mail import send_mail,send_mass_mail
from django.conf import settings

import random
import io
from PIL import Image,ImageDraw,ImageFont
# 邮箱验证有效期
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.views.decorators.cache import cache_page

# @cache_page(60*5)
def index(request):
    # 得到序列化工具
    # serulil = Serializer(settings.SECRET_KEY,50)
    # result = serulil.dumps({'userid':101}).decode("utf-8")
    #
    # # 得到反序列化工具
    # dserutil = Serializer(settings.SECRET_KEY, 50)
    # try:
    #     obj = dserutil.loads(result)



    message = Message.objects.all()
    hotpics = HotPic.objects.all().order_by('index')
    return render(request,'booktest/index.html',{'hotpics':hotpics,'message':message})
    # return render(request,'/booktest/index')


def reader(request):
    user = StudentUser.objects.get(username=request.session['username'])
    return render(request, 'booktest/reader.html', {'user': user})

def rlogin(request):

    if request.method == 'GET':
        return render(request,'booktest/reader_login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        verifycode = request.POST['verifycode']
        student = StudentUser.objects.filter(username=username).filter()
        if student:
            if student.username == username and student.password == password:
                if student.is_active == True:
                # user = StudentUser.objects.get(username=username)
                    request.session['username'] = username
                    return redirect(to=reverse('booktest:reader'))
                if verifycode == request.session.get('verifycode'):
                    return render(request,'booktest/reader.html')
                else:
                    return HttpResponse("验证码错误")


            else:
                error = '链接已失效'
                return render(request, 'booktest/reader_login.html', {'error': error})
        else:
            error = '账号或密码错误'
            return render(request, 'booktest/reader_login.html', {'error': error})




def mlogin(request):
    return render(request,'booktest/reader_login.html')

#
# def register(request):
#     return render(request,'booktest/register.html')


def register(request):
    if request.method == 'GET':
        return render(request,'booktest/register.html')
    else:
        try:

            username = request.POST['username']
            password = request.POST['password']
            colleg = request.POST['college']
            numbe = request.POST['number']
            email = request.POST['email']


            StudentUser.objects.create_user(username,password=password,studentnum=numbe,college=colleg,email=email,is_active=False)
            id = StudentUser.objects.get(username=username).id
            seruili = Serializer(settings.SECRET_KEY,50)
            userid = seruili.dumps({'userid':id}).decode('utf-8')
            send_mail("激活账户",f"<a href='http://127.0.0.1:8000/booktest/active/{userid}'>点击链接激活账号</a>",settings.DEFAULT_FROM_EMAIL,[email])

            # return render(request,'booktest/reader_login.html')
        except Exception as e:

            return render(request,'booktest/reader_login.html',{'error':e})

        return redirect(reverse('booktest:rlogin'))


def logout(request):
    return render(request,'booktest/index.html')


def query(request,id):
    user = StudentUser.objects.get(id=id)
    if request.method == 'GET':
        return render(request, 'booktest/reader_query.html', {"user":user})
    elif request.method == 'POST':
        choice = request.POST['item']
        content = request.POST['query']
        if content == '':
            return render(request, 'booktest/reader_query.html',{'user':user, 'error': '不能为空'})
        # return render(request,'booktest/reader_query.html')
        if choice == 'name':
            books = Book.objects.filter(bname__contains=content)
        else:
            books = Book.objects.filter(author__contains=content)
        if len(books) == 0:
            return render(request, 'booktest/reader_query.html', {'user': user, 'error': '没有找到此书'})
        return render(request, 'booktest/reader_query.html', {'user':user, 'books':books})


def info(request):
    return render(request,'booktest/reader_info.html')


def histroy(request):
    # borrow = BorrowMessage.objects.get(book=book)
    return render(request,'booktest/reader_histroy.html')


def book(request, bookid):
    book = Book.objects.get(pk=bookid)
    user = StudentUser.objects.get(username=request.session['username'])
    # bookhistory = BorrowMessage.objects.get(pk=bookid)
    return render(request,'booktest/reader_book.html', {'book': book, 'user': user})


def upload(request):
    if request.method == 'GET':
        return render(request, 'booktest/reader_upload.html')
    elif request.method == 'POST':
        name = request.POST['name']
        index = request.POST['index']
        pic = request.FILES['pic']
        load = HotPic(index=index,pic=pic,name=name)
        load.save()
        return redirect(reverse('booktest:index'))


def edit(request):
    if request.method == 'GET':
        return render(request,'booktest/edit.html')
    elif request.method =='POST':
        title = request.POST['title']
        message = request.POST['message']
        meg = Message(title=title,message=message)
        meg.save()
        return redirect(reverse('booktest:index'))


def meilto(request):
    try:
        send_mail("Djonge邮件1",'Django发送的邮件',settings.DEFAULT_FROM_EMAIL,['3317957914@qq.com'])
        print('发送成功')
    except:
        return HttpResponse('发送失败')
    return HttpResponse("发送成功")


def active(request,id):
    serulil = Serializer(settings.SECRET_KEY,50)
    try:
        obj = serulil.loads(id)
        user = StudentUser.objects.get(pk=obj['userid'])
        user.is_active = True
        user.save()
        return redirect(reverse('booktest:register'))
    except:

        return HttpResponse("链接已失效")

def ajax(request):
   return render(request, 'booktest/ajax.html')


def ajaxajax(request):
    if request.method == 'GET':
        return HttpResponse("get请求成功")
    elif request.method == 'POST':
        return HttpResponse("post请求成功")


def ajaxlogin(request):
    if request.method == 'GET':
        return render(request,'booktest/ajaxlogin.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        verifycode = request.POST['verifycode']
        user = StudentUser.objects.filter(username=username).first()
        if user:
            if user.username == username and user.password == password:
                if verifycode == request.session.get('verifycode'):
                    return HttpResponse('登录成功')
                else:
                    return HttpResponse("验证码错误")
            else:

                return HttpResponse("登录失败")
        else:
            return HttpResponse('用户名不存在')


def checkuser(request):
    if request.method =='POST':
        username = request.POST['username']
        user = StudentUser.objects.filter(username=username).first()
        if user is None:
            return HttpResponse('success')
        else:
            return HttpResponse("failcd")

def verifycode(request):
    bgcolor = (random.randrange(20, 100),
               random.randrange(20, 100),
               random.randrange(20, 100))
    width = 100
    heigth = 25
    # 创建画面对象
    im = Image.new('RGB', (width, heigth), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, heigth))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象
    font = ImageFont.truetype('static/fonts/ALGER.TTF', 23)
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)



    # 释放画笔
    del draw

    #
    request.session['verifycode'] = rand_str
    f = io.BytesIO()
    im.save(f, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(f.getvalue(), 'image/png')