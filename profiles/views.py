# from typing import Annotated
from django.shortcuts import get_object_or_404,render,HttpResponse, redirect
from accounts.models import User
from buy.models import Buy
from django.conf import settings
from accounts.forms import Smsform ,Smscheckform
from profiles.forms import UserReviewform, UserReportform, PostReportform
from .models import Review
from django.db.models import Avg
from django.contrib.auth.decorators import login_required

application_id = settings.SENDBIRD_APPLICATION_ID
sendbird_api_token = settings.SENDBIRD_API_TOKEN

def changeChatNick(request, new_nick):
     #sendbird 정보 가져오기
    user_id = request.user.email #유저 이메일 지정

    url = f"https://api-{application_id}.sendbird.com/v3/users/{user_id}"
    api_headers = {"Api-Token": sendbird_api_token}
    
    data = {
        'nickname' : new_nick,
    }
    
    res = requests.put(url, data= json.dumps(data), headers=api_headers)
    
    info = res.text
    parse = json.loads(info)
    #print(parse)

@login_required(login_url='/accounts/login/')
def profileHome(request,user_name):
    user = get_object_or_404(User, username=user_name)
    p_post =  Buy.objects.filter(ID=user).order_by('-writeDate')
    reviews = Review.objects.filter(ID=user).aggregate(avg_rate=Avg('rating'))
    likes = user.like_posts.all()
    joins = user.join_posts.all()
    #  sms 폼출력
    return render(request, 'profile/home.html',{'user':user , 'p_post':p_post, 'likes':likes,'joins':joins,'reviews':reviews})

def profileEdit(request,user_name):
    user = get_object_or_404(User, username=user_name)
    if request.method == "POST":
        new_nick = request.POST['content']
        user.username = new_nick
        changeChatNick(request, new_nick)
        user.save()
        return redirect('../'+user.username)
    return render(request, 'profile/edit_profile.html')

#  sms 인증
# Python
import json, requests, time, random

# Django
from django.views import View
from django.http import JsonResponse
from .utils import make_signature
from django.contrib import messages

def sms(request, user_name): # 폼 출력 
    smsform  = Smsform()
    checksmsform = Smscheckform()
    return render(request,'profile/sms.html', {'smsform':smsform , 'checksmsform':checksmsform})

    # return render(request, 'profile/sms.html', {'username': user_name})

def send_sms(phone_number, auth_number):
    timestamp = str(int(time.time() * 1000)) # sign  
    headers = {
        'Content-Type': "application/json; charset=UTF-8", # 네이버 참고서 차용
        'x-ncp-apigw-timestamp': timestamp, # 네이버 API 서버와 5분이상 시간차이 발생시 오류
        'x-ncp-iam-access-key': 'SdCSP6m7s7H4bba0QO3E',
        'x-ncp-apigw-signature-v2': make_signature(timestamp) # utils.py 이용
    }
    body = {
        "type": "SMS", 
        "contentType": "COMM",
        "from": "01092247763", # 사전에 등록해놓은 발신용 번호 입력, 타 번호 입력시 오류
        "content": f"[바이투게더]인증번호:{auth_number}", # 메세지를 이쁘게 꾸며보자
        "messages": [{"to": f"{phone_number}"}] # 네이버 양식에 따른 messages.to 입력
    }
    URL ='https://sens.apigw.ntruss.com/sms/v2/services/ncp:sms:kr:292298761053:buytogether/messages' 
    body = json.dumps(body)
    requests.post(URL, headers=headers, data=body)
        # 발송 URI 부분에는 아래 URL을 넣어주면 된다.
        # 다만, 너무 길고 동시에 보안이슈가 있기에 별도로 분기해놓은 settings 파일에 넣어서 불러오는 것을 추천한다.
    
def sendsms(request, username):
    if request.method=='POST':
        form = Smsform(request.POST)
        data = request.POST['phone_number']
        # data = request.POST.get["phone_number"]
        input_mobile_num = data
        auth_num = random.randint(10000, 100000) # 랜덤숫자 생성, 5자리로 계획하였다.
        if form.is_valid():
            try:##인증ㅇ번호 발송
                auth_mobile = User.objects.get(username=username)
                auth_mobile.auth_number = auth_num
                auth_mobile.phone_number = input_mobile_num
                auth_mobile.save()
                send_sms(phone_number=data, auth_number=auth_num)
                # return JsonResponse({'message': '인증번호 발송완료'}, status=200)
                messages.success(request, f"인증번호가 발송되었습니다. 인증번호를 입력해주세요.")
                return redirect('../../profile/'+username+'/sms')
            except User.DoesNotExist: # 인증요청번호 미 존재 시 DB 입력 로직 작성
                User.objects.update_or_create(
                    phone_number=input_mobile_num,
                    auth_number=auth_num,
                ).save()
                send_sms(phone_number=input_mobile_num, auth_number=auth_num)
                # return JsonResponse({'message': '인증번호 발송 및 DB 입력완료'}, status=200)
                # return HttpResponse('인증번호 발송완료 및 입력완료')
        messages.error(request, f"휴대폰번호오류")
        return redirect('../../profile/'+username+'/sms')
    return redirect('../../profile/'+username+'/sms')


def checksms(request,username):# 인증번호 확인
    
    if request.method == 'POST':
        form = Smscheckform(request.POST)
        if form.is_valid():
            data = request.POST.get("auth_number")
            # phone_number = request.POST.get("phone_number")
            try:
                verification = User.objects.get(username=username)

                if verification.auth_number == data:
                    verification.sms = True
                    verification.save()
                    # return JsonResponse({'message': '인증 완료되었습니다.'}, status=200)
                    messages.success(request, f"인증 완료")
                    return redirect('../../profile/'+username+'/sms')

                else:
                    # return JsonResponse({'message': '인증 실패입니다.'}, status=400)
                    messages.error(request, f"인증 실패")
                    verification.phone_number=""
                    verification.sms=False
                    verification.save()
                    return redirect('../../profile/'+username+'/sms')

            except User.DoesNotExist:
                    messages.error(request, f"인증 실패")
                    verification.sms=False
                    verification.phone_number=""
                    verification.save()
                    return redirect('../../profile/'+username+'/sms')
    

@login_required(login_url='/accounts/login/')
def reportUser(request, username):
    if request.method == 'POST':
        form = UserReportform(request.POST)
        user = User.objects.get(username=username)
        
        if form.is_valid():
            finished_form =form.save(commit=False)
            finished_form.ID=get_object_or_404(User,id=user.id)
            finished_form.save()
        return redirect('../'+user.username)
    else:
        form  = UserReportform()
    # return render(request,'profile/review.html', {'form':form})
    return render(request, 'profile/report.html', {'form':form})

@login_required(login_url='/accounts/login/')
def reportPost(request, post_id):
    if request.method == 'POST':
        form = PostReportform(request.POST)
        post = Buy.objects.get(id=post_id)
        
        if form.is_valid():
            finished_form =form.save(commit=False)
            finished_form.buyID=get_object_or_404(Buy,id=post_id)
            finished_form.save()
        return redirect('../'+str(post.id))
    else:
        form  = PostReportform()
    # return render(request,'profile/review.html', {'form':form})
    return render(request, 'profile/reportpost.html', {'form':form, 'id':post_id})

@login_required(login_url='/accounts/login/')
def userProfile(request, username):
    profileuser = get_object_or_404(User, username=username) # 사용자 닉네임
    reviews = Review.objects.filter(ID=profileuser).aggregate(avg_rate=Avg('rating'))
    posts =  Buy.objects.filter(ID=profileuser).order_by('-writeDate') # 사용자가 쓴 글 불러옴
    # point__avg=  User.objects.values('username').annotate(point__avg=Avg('porint'))
    return render(request, 'profile/userprofile.html', {'profileuser': profileuser , 'posts' : posts,'reviews':reviews})

from django.db.models import Q 
@login_required(login_url='/accounts/login/')
def review(request,username): #username 상대방 수정도 넣으면 좋을 듯 유저 한명당 리뷰 하나만 가능
    profileuser = get_object_or_404(User, username=username)
    writer_id = request.user.id
    writer = User.objects.get(id=writer_id)
    
    try:
        review = get_object_or_404(Review,Q(ID=profileuser)& Q(writer=writer))
        return editReview(request,profileuser.username)
    except:
        return createReview(request,profileuser.username)
     

@login_required(login_url='/accounts/login/')
def createReview(request,username):
    form = UserReviewform(request.POST)
    profileuser = User.objects.get(username=username)
    if request.method == 'POST':
        writer_id = request.user.id
        writer = User.objects.get(id=writer_id)

        if form.is_valid():
            finished_form =form.save(commit=False)
            finished_form.writer=get_object_or_404(User,id=writer_id)
            finished_form.ID=get_object_or_404(User,id=profileuser.id)
            finished_form.save()
        return redirect('../userprofile/'+profileuser.username)
    else:
        form  = UserReviewform()
    return render(request,'profile/review.html', {'form':form,'profileuser':profileuser})


def editReview(request,username):
    profileuser = User.objects.get(username=username)
    writer_id = request.user.id
    writer = User.objects.get(id=writer_id)
    # review = Review.objects.all().filter(Q(ID=user)& Q(writer=writer))
    review = get_object_or_404(Review,Q(ID=profileuser)& Q(writer=writer))
    # 글을 수정사항을 입력하고 제출을 눌렀을 때
    if request.method == "POST":
        form = UserReviewform(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # {'name': '수정된 이름', 'image': <InMemoryUploadedFile: Birman_43.jpg 	(image/jpeg)>, 'gender': 'female', 'body': '수정된 내용'}
            review.content = form.cleaned_data['content']
            review.rating = form.cleaned_data['rating']
            review.save()
            return redirect('../userprofile/'+profileuser.username)
        
    # 수정사항을 입력하기 위해 페이지에 처음 접속했을 때
    else:
        form = UserReviewform(instance =review )
        context={
            'form':form,
            'writing':True,
            'now':'edit',
            'profileuser':profileuser,
        }
    return render(request,'profile/review.html', context)