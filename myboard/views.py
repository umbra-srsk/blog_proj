from django.shortcuts import render, redirect, get_object_or_404
from .models import MyBoard, MyMember, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse
from . import calc_latlng
import requests
import json
from django.contrib.auth.models import User
from django.views.generic import ListView


def index(request):
    myboard_all = MyBoard.objects.all().order_by('-id')
    #print(myboard_all)

    paginator = Paginator(myboard_all, 5)
    page_num = request.GET.get('page', '1')
    
    #페이지에 맞는 모델
    page_obj = paginator.get_page(page_num)
 
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

        if MyMember.objects.filter(myname=myname).exists():
            return render(request, 'register.html', {'error': '이미 존재하는 이름 입니다'})

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
        

        try:
            mymember = MyMember.objects.get(myname=myname)
        except MyMember.DoesNotExist:
            return render(request, 'login.html', {'error': '잘못된 이름 또는 비밀번호 입니다'})
        

        if check_password(mypassword, mymember.mypassword):
             request.session['myname'] = mymember.myname
             return redirect('/')
        
        else:
            #return redirect('login')
            return render(request, 'login', {'error': '잘못된 이름 또는 비밀번호 입니다'})

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
        data = json.loads(request.body)
        lat = data.get('lat')
        lng = data.get('lng')

    
    api_latlng = None

    if lat is not None and lng is not None:
        api_latlng = calc_latlng.mapToGrid(lat, lng)


    now = datetime.now()
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst'
    params = {
        'ServiceKey' : 'vDPsHfRauBIF+jBMpO/ec6aUByTVO02YSht+oAdhZoLORXaMfX8XXWTG0PNuIV6NG8EHDi+4yfaKhFeG1vJmKw==',
        'pageNo' : '1',
        'numOfRows' : '12',
        'dataType' : 'JSON',
        'base_date' : str(now.year)+'0'+str(now.month)+str(now.day),
        'base_time' : '0' + str(now.hour - 1)+'00',
        'nx' : api_latlng[0],
        'ny' : api_latlng[1]
    }

    print(params)
    '''
    'nx' : api_latlng[0],
    'ny' : api_latlng[1]
    '''


    response = requests.get(url, params=params)

    items = response.json().get('response').get('body').get('items')

    weather_data = dict()

    for item in items['item']:
        # 기온
        if item['category'] == 'T1H':
            weather_data['tmp'] = item['obsrValue']
        # 습도
        if item['category'] == 'REH':
            weather_data['hum'] = item['obsrValue']
        # 강수량
        if item['category'] == 'RN1':
            weather_data['rain'] = item['obsrValue']

    print(weather_data)

    return JsonResponse(weather_data)

'''
def add_reply(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        author = request.session.get('myname')
        content = request.POST.get('content')

        print(post_id), print(author), print(content)

        if post_id and author and content:
            myboard = get_object_or_404(MyBoard, id=post_id)
            print(myboard)

            if not author:
                return JsonResponse({'success': False, 'message': '로그인이 필요합니다.'})

            reply = Reply.objects.create(myboard=myboard, author=author, content=content)

            return JsonResponse({'success': True, 'author': author, 'content': content})
    
    return JsonResponse({'success': False, 'message': '잘못된 요청입니다.'})

'''


def add_reply(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        author = request.session.get('myname')
        content = request.POST.get('content')

        if post_id and author and content:
            myboard = get_object_or_404(MyBoard, id=post_id)

            if not author:
                return JsonResponse({'success': False, 'message': '로그인이 필요합니다.'})

            reply = Reply.objects.create(myboard=myboard, author=author, content=content)

            return JsonResponse({
                'success': True,
                'id': reply.id,  # Send the Reply.id in the response
                'author': author,
                'content': content
            })

    return JsonResponse({'success': False, 'message': '잘못된 요청입니다.'})


def get_replies(request, id):
    myboard_one = get_object_or_404(MyBoard, id=id)
    replies = Reply.objects.filter(myboard=myboard_one)
    reply_list = []
    for reply in replies:
        reply_data = {
            'id': reply.id,
            'author': reply.author,
            'content': reply.content
        }
        reply_list.append(reply_data)
    return JsonResponse({'success': True, 'replies': reply_list})

def delete_reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    reply.delete()
    return JsonResponse({'success': True})

    
def search(request):
    query = request.GET.get('q')

    if query:
        posts = MyBoard.objects.filter(mytitle__icontains=query)
    else:
        posts = MyBoard.objects.all()

    return render(request, 'search.html', {'posts': posts})

class PostListView(ListView):
    model = MyBoard
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 5 # 페이지당 게시글 수 설정

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            queryset = MyBoard.objects.filter(title__icontains = query)
        else:
            queryset = MyBoard.objects.all()
        return queryset
    
def result(request):
    query = request.GET.get('query')

    if query:
        posts = MyBoard.objects.filter(Q(mytitle__icontains=query) | Q(mycontent__icontains=query))

    else:
        posts = MyBoard.objects.all()

    return render(request, 'result.html', {'posts':posts})
    