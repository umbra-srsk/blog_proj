from django.shortcuts import render, redirect
from .models import MyBoard, MyMember
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse
import math


def index(request):
    myboard_all = MyBoard.objects.all().order_by('-id')
    #print(myboard_all)

    paginator = Paginator(myboard_all, 5)
    page_num = request.GET.get('page', '1')
    
    #페이지에 맞는 모델
    page_obj = paginator.get_page(page_num)
    print(type(page_obj))

    #총 모델 수
    print(page_obj.count)
    #총 페이지 수
    print(page_obj.paginator.num_pages)
    #총 페이지 range 객체
    print(page_obj.paginator.page_range)
    #다음 페이지 유무
    print(page_obj.has_next())
    #이전 페이지 유무
    print(page_obj.has_previous())

    try:
        #다음 페이지 숫자(없으면 에러)
        print(page_obj.next_page_number())
        #이전 페이지 숫자
        print(page_obj.previous_page_number())

    except:
        pass
    #
    print(page_obj.start_index())
    #
    print(page_obj.end_index())


    return render(request, 'index.html', {'list': page_obj})

def insert_proc(request):
    if request.method == 'GET':
        return render(request, 'insert.html')
    else:
        myname = request.POST['myname']
        mytitle = request.POST['mytitle']
        mycontent = request.POST['mycontent']

        result = MyBoard.objects.create(myname=myname, mytitle=mytitle, mycontent=mycontent, mydate=timezone.now())
        print(result)

        if result:
            return redirect('index')
        else:
            return redirect('insert')

"""
def insert_form(request):
    return render(request, 'insert.html')

def insert_res(request):
    myname = request.POST['myname']
    mytitle = request.POST['mytitle']
    mycontent = request.POST['mycontent']


    result = MyBoard.objects.create(myname=myname, mytitle=mytitle, mycontent=mycontent, mydate=timezone.now())
    print(result)

    if result:
        return redirect('index')
    else:
        return redirect('insert')
"""

def detail(request, id):
    myboard_one = MyBoard.objects.get(id=id)
    print(myboard_one)
    return render(request, 'detail.html', {'dto': myboard_one})

def update_proc(request, id):
    if request.method == 'GET':
        myboard_one = MyBoard.objects.get(id=id)
        print(myboard_one)
        return render(request, 'update.html', {'dto': myboard_one})
    else:
        mytitle = request.POST['mytitle']
        mycontent = request.POST['mycontent']
        #id = request.POST['id']

        myboard = MyBoard.objects.filter(id=id)
        print(myboard)
        result_title = myboard.update(mytitle=mytitle)
        result_content = myboard.update(mycontent=mycontent)
        print(f'title update : {result_title} / content update : {result_content}')

        if result_title + result_content == 2:
            return redirect(f'/detail/{id}')
        else:
            return redirect(f'/update/{id}')


"""
def update_form(request, id):
    myboard_one = MyBoard.objects.get(id=id)
    print(myboard_one)
    return render(request, 'update.html', {'dto': myboard_one})

def update_res(request):
    mytitle = request.POST['mytitle']
    mycontent = request.POST['mycontent']
    id = request.POST['id']

    myboard = MyBoard.objects.filter(id=id)
    print(myboard)
    result_title = myboard.update(mytitle=mytitle)
    result_content= myboard.update(mycontent=mycontent)
    print(f'title update : {result_title} / content update : {result_content}')

    if result_title + result_content == 2:
        return redirect(f'/detail/{id}')
    else :
        return redirect(f'/updateform/{id}')
"""

def delete_proc(request, id):
    result_delete = MyBoard.objects.filter(id=id).delete()
    #print(result_delete)
    '''
        myboard = MyBoard.objects.get(id=id)
        myboard.mytitle = mytitle
        myboard.mycontent = mycontent
        myboard.save()
    '''

    if result_delete[0]:
        return redirect('index')
    else:
        return redirect(f'/detail/{id}')



def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        myname = request.POST['myname']
        mypassword = request.POST['mypassword']
        myemail = request.POST['myemail']

        #mymember = MyMember(myname=myname, mypassword=mypassword, myemail=myemail)
        mymember = MyMember(myname=myname, mypassword=make_password(mypassword), myemail=myemail)
        mymember.save()

        return redirect('/')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        myname = request.POST['myname']

        mypassword = request.POST['mypassword']
        

        mymember = MyMember.objects.get(myname=myname)

        if check_password(mypassword, mymember.mypassword):
             request.session['myname'] = mymember.myname
             return redirect('/')
        
        else:
            return redirect('login')

'''
        if mypassword == mymember.mypassword:
            request.session['myname'] = mymember.myname
            print(myname)
            print(mypassword)
            return redirect('/')

        else:
            return redirect('login')
'''

def logout(request):
    del request.session['myname']
    return redirect('/')



def weather(request):
    if request.method == 'POST':
        lat = request.POST.get("lat")
        lng = request.POST.get("lng")


    now = datetime.now()
    url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0"
    params = {
        'ServiceKey' : 'vDPsHfRauBIF+jBMpO/ec6aUByTVO02YSht+oAdhZoLORXaMfX8XXWTG0PNuIV6NG8EHDi+4yfaKhFeG1vJmKw==',
        'base_date' : '20230711' ,
        'base_time' : '0600' ,
        'nx' : lat,
        'ny' : lng
    }







def search(request):
    pass    
