from django.db import models
from accounts.models import User
from buy.models import Buy

class ReportUser(models.Model):
    content =models.TextField()
    ID = models.ForeignKey(User,  on_delete=models.CASCADE,blank=False,
                                 null=False,
                                 default="")# 글쓴이 

class ReportPost(models.Model):
    content = models.TextField()
    buyID = models.ForeignKey(Buy, on_delete=models.CASCADE, blank= True,null=False)#거래글


# 신고,, > 게시글 신고는 게시글 에서 작성자 아이디 받아와서 유저 신고로
# 유저 신고는

class Review(models.Model):
    content = models.TextField()# 리뷰 내용 
    writer = models.ForeignKey(User,  on_delete=models.CASCADE,blank=False,
                                 null=False,
                                 default="", related_name='writer') # 리뷰를 작성한 사람 
    ID = models.ForeignKey(User,  on_delete=models.CASCADE,blank=False,
                                 null=False,
                                 default="",related_name='ID') #리뷰당하는 사람
    rating = models.FloatField() # 별점 s