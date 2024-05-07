from django.shortcuts import render
from TestModel.models import Student
from TestModel.models import GroupChat
from TestModel.models import User
from HelloWorld import search
from django.db.models import Avg,Max,Min,Count,Sum

# Create your views here.
def index(request):
    num=request.session.get('num')
    value = {
        'name': request.session.get('name'),
        'power': request.session.get('power'),
        'num': request.session.get('num')
    }
    alldata = {}
    num = request.session.get('num')
    power = request.session.get('power')
    stu_info = list(Student.objects.filter(num=num).values())  # 获得该名同学的信息
    group_id = stu_info[0]['group_id']
    member_info = list(Student.objects.filter(group_id=group_id).values())
    # 选取后十条数据
    group_talk = list(GroupChat.objects.filter(group_id=group_id).order_by('-id').values())
    group_peo = list(GroupChat.objects.filter(group_id=group_id).values('send_num').annotate(count=Count('id')))
    for item in group_talk:
        num = item['send_num']
        item['name'] = get_name(num)
        if item['send_type'] == '2':
            file_path = item['send_content']
            import os
            if os.sep in file_path:
                file_name = file_path.split('\\')[-1]
            else:
                file_name = file_path.split('/')[-1]
            item['file_name'] = file_name
            item['file_type'] = file_name.split('.')[1];
            fsize = os.path.getsize(file_path)
            fsize = round(fsize / float(1024))  # 转换文件大小为KB
            item['file_size'] = fsize;
    search.time_format(group_talk)
    search.find_talk(group_peo, member_info)
    search.is_user(group_talk, request.session.get('num'))
    notice_list = search.get_notice(num)
    alldata['member_list'] = member_info  # 组员信息
    alldata['stu_info'] = stu_info  # 用户信息
    alldata['room_name'] = group_id  # 房间信息
    alldata['group_talk'] = group_talk  # 聊天记录
    return render(request, 'group_chat.html', alldata)
    #return render(request,'chat/index.html',{})
def get_info(request,group_id):
    alldata={}
    user_info=list(User.objects.filter(num=request.session.get('num')).values("num","power","name"))
    user_info[0]['group_id']=group_id
    member_info = list(Student.objects.filter(group_id=group_id).values())
    # 选取后十条数据
    group_talk = list(GroupChat.objects.filter(group_id=group_id).order_by('-id').values())
    group_peo = list(GroupChat.objects.filter(group_id=group_id).values('send_num').annotate(count=Count('id')))
    for item in group_talk:
        num = item['send_num']
        item['name'] = get_name(num)
        if item['send_type'] == '2':
            file_path = item['send_content']
            import os
            if os.sep in file_path:
                file_name = file_path.split('\\')[-1]
            else:
                file_name = file_path.split('/')[-1]
            item['file_name'] = file_name
            item['file_type'] = file_name.split('.')[1];
            fsize = os.path.getsize(file_path)
            fsize = round(fsize / float(1024))  # 转换文件大小为KB
            item['file_size'] = fsize;
    search.time_format(group_talk)
    search.find_talk(group_peo, member_info)
    search.is_user(group_talk, request.session.get('num'))
    alldata['member_list'] = member_info  # 组员信息
    alldata['stu_info'] = user_info  # 用户信息
    alldata['room_name'] = group_id  # 房间信息
    alldata['group_talk'] = group_talk  # 聊天记录
    return alldata
def get_name(num):
    stu=Student.objects.filter(num=num)
    if stu:
        return list(Student.objects.filter(num=num).values())[0]['name']
    else:
        return list(User.objects.filter(num=num).values())[0]['name']
def room(request,room_name):
    value = {
        'name': request.session.get('name'),
        'power': request.session.get('power'),
        'num': request.session.get('num')
    }
    alldata = {}
    num = request.session.get('num')
    power = request.session.get('power')
    if power=='老师' or power=='管理员': #进入讨论区的为老师或管理员
             alldata=get_info(request,room_name)
             return render(request, 'group_chat.html', alldata)
    stu_info = list(Student.objects.filter(num=num).values())  # 获得该名同学的信息
    group_id = stu_info[0]['group_id']
    member_info = list(Student.objects.filter(group_id=group_id).values())
    #选取后十条数据
    group_talk=list(GroupChat.objects.filter(group_id=group_id).order_by('-id').values())
    group_peo=list(GroupChat.objects.filter(group_id=group_id).values('send_num').annotate(count = Count('id')))
    for item in group_talk:
        num=item['send_num']
        item['name']=get_name(num)
        if item['send_type'] == '2':
            file_path=item['send_content']
            import os
            if os.sep in file_path:
                file_name = file_path.split('\\')[-1]
            else:
                file_name = file_path.split('/')[-1]
            item['file_name']=file_name
            item['file_type']=file_name.split('.')[1];
            fsize = os.path.getsize(file_path)
            fsize = round(fsize / float(1024))  # 转换文件大小为KB
            item['file_size'] = fsize;
    search.time_format(group_talk)
    search.find_talk(group_peo, member_info)
    search.is_user(group_talk,request.session.get('num'))
    notice_list = search.get_notice(num)
    alldata['member_list'] = member_info  # 组员信息
    alldata['stu_info'] = stu_info  # 用户信息
    alldata['room_name'] = room_name  # 房间信息
    alldata['group_talk'] = group_talk  # 聊天记录
    return render(request,'group_chat.html',alldata)