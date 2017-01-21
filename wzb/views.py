#coding=utf-8
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, render


from django.db.models.signals import post_save

from django.contrib.auth.models import User



from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core import serializers

def hello(request):

    # Create an HttpResponse object...
    # response = HttpResponse("Your favorite color is now %s" %             request.GET["favorite_color"])

    # ... and set a cookie on the response
    # response.set_cookie("favorite_color",'kk')
    d = request.COOKIES
    response = HttpResponse('right %s' % d)

    response.set_cookie("favorite_color", 'test')
    k = request.COOKIES
    request.session["fav_color"] = "blue"
    name = request.user.username
    # except:
    #     name = 'no'
    # print request.session["fav_color"]

    return response


def index(request):

    #Notification.objects.unread()
    # user = User.objects.get(pk=request.user.id)
    # k=user.notifications.unread()
    # p=CodeTable.objects.all()
    return render(request, 'index.html',locals())


from django.db.models.signals import post_save
from notifications.signals import notify
from stockCode.models import CodeTable


#自定义一个获取消息的函数
def fetchNotification(request):
    user = User.objects.get(pk=request.user.id)
    k=user.notifications.unread()
    t=serializers.serialize("json", k)

    return HttpResponse(t)


def test(request):

    return HttpResponse(t)
