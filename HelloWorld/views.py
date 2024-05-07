from django.core import serializers
from django.shortcuts import render,redirect
from django.utils import timezone
from django.core import serializers
from django.conf import settings
from django.db.models import Avg,Max,Min,Count,Sum  #   引入函数
from django.db import transaction
from django.http import HttpResponse, JsonResponse,StreamingHttpResponse,FileResponse
from TestModel.models import User
from TestModel.models import Student
from TestModel.models import task
from TestModel.models import doc
from TestModel.models import feed_back
from TestModel.models import feedbackfile
from TestModel.models import notice
from TestModel.models import learn_obj
from TestModel.models import init_info
from TestModel.models import Evaluate
from TestModel.models import eva_recollect
from TestModel.models import GroupChat
from TestModel.models import UserGroup
from django.db.models import Max
from . import search
import json
import xlrd
import datetime
def index(request):#登录页
    return render(request,'index.html')
def techinit(request):#进入教师初始化页面
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    return render(request,'tech-init.html',context=value)
def techinitinfo(request):#初始化系统信息
    return render(request,'tech-init-info.html')
def stuinitinfo(request):#手动添加学生信息
    data={}
    group_list=list(UserGroup.objects.all().values("group_id","topic"))
    for item in group_list:
        item['count']=Student.objects.filter(group_id=item["group_id"]).count()
    data['group_list']=group_list
    return render(request,'stu-init-info.html',data)
def user_info(request):#手动添加学生信息
    data={}
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    num=request.session.get('num')
    power=request.session.get('power')
    group_list=list(UserGroup.objects.all().values("group_id","topic"))
    for item in group_list:
        item['count']=Student.objects.filter(group_id=item["group_id"]).count()

    user_info=list(User.objects.filter(num=num).values())
    if power == '学生':
        user_info[0]['grade']=Student.objects.filter(num=num).first().grade
        user_info[0]['group_id'] = Student.objects.filter(num=num).first().group_id
        user_info[0]['group_topic'] = UserGroup.objects.filter(group_id=user_info[0]['group_id']).first().topic
        user_info[0]['group_role'] = Student.objects.filter(num=num).first().group_role
    data['group_list']=group_list
    data['user'] = user_info
    return render(request,'user_info.html',data)
def edit_password(request):#修改密码
    data={}
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    num=request.session.get('num')
    power=request.session.get('power')
    user_info=list(User.objects.filter(num=num).values())
    data['user'] = user_info
    return render(request,'edit_password.html',data)
def groupinitinfo(request):#手动添加小组信息
    maxid = UserGroup.objects.all().aggregate(Max('group_id'))
    print(maxid)
    if maxid['group_id__max'] == None:
        maxid['group_id__max'] = 1
    else:
        maxid['group_id__max'] = maxid['group_id__max'] + 1
    value = {'maxid': maxid['group_id__max']
             }
    return render(request,'group-init-info.html',context=value)
def addinitinfo(request):#初始化系统信息上传
  back_dic = {'resultCode': None, 'msg': None}
  if request.method=='POST':
    obj_topic=request.POST.get('obj_topic')
    obj_content=request.POST.get('obj_content')
    obj_author=request.session.get('name')
    stufile=request.FILES.get('stufile',None)
    stufile_name=stufile.name #获取文件名字
    print(stufile_name)
    groupfile = request.FILES.get('groupfile',None)
    groupfile_name = groupfile.name #获取文件名字
    print(groupfile_name)
    stu_group_index=0
    stu_topic_index=0
    # 解析excel文件
    try:
        with transaction.atomic():
            msg=''
            stu_info = xlrd.open_workbook(filename=None, file_contents=stufile.read())
            stu_sheet = stu_info.sheet_by_index(0)
            stu_t = stu_sheet.row_values(0)
            for row in range(0, len(stu_t)):
                if stu_t[row] == '学号':
                    stu_num_index = row
                if stu_t[row] == '姓名':
                    stu_name_index = row
                if stu_t[row] == '班级':
                    stu_grade_index = row
                if stu_t[row] == '组号':
                    stu_group_index = row
                if stu_t[row] == '选题':
                    stu_topic_index = row
            if stu_group_index or stu_topic_index :
                for row in range(1, stu_sheet.nrows):
                    stu_num = str(str(stu_sheet.row_values(row)[stu_num_index]).split('.')[0])  # 学号
                    stu=Student.objects.filter(num=stu_num)
                    if stu:
                        msg=msg+"\n已存在学号为"+stu_num+"的学生"
                    else:
                        stu_name = str(stu_sheet.row_values(row)[stu_name_index])  # 姓名
                        stu_bj = str(stu_sheet.row_values(row)[stu_grade_index])  # 班级
                        if stu_group_index:
                           group_id=str(stu_sheet.row_values(row)[stu_group_index])
                           newstu = Student(num=stu_num, name=stu_name, grade=stu_bj, score=0, group_id=group_id,
                                            group_role='尚未指定')
                           newuser = User(num=stu_num, pwd=stu_num, power='学生', name=stu_name)
                           newstu.save()
                           newuser.save()
                        else:
                           group_topic = str(stu_sheet.row_values(row)[stu_topic_index])
                           group_id=UserGroup.objects.filter(topic=group_topic).first()
                           if group_id:
                                group_id = UserGroup.objects.filter(topic=group_topic).first().group_id
                                newstu = Student(num=stu_num, name=stu_name, grade=stu_bj, score=0, group_id=group_id,
                                                 group_role='尚未指定')
                                newstu.save()
                           else:
                               maxid = UserGroup.objects.all().aggregate(Max('group_id'))
                               print(maxid)
                               if maxid['group_id__max'] == None:
                                   maxid['group_id__max'] = 1
                               else:
                                   maxid['group_id__max'] = maxid['group_id__max'] + 1
                               new_group=UserGroup(group_id=maxid['group_id__max'],topic=group_topic,group_score=0)
                               newstu = Student(num=stu_num, name=stu_name, grade=stu_bj, score=0, group_id=maxid['group_id__max'],
                                                 group_role='尚未指定')
                               new_group.save()
                               newstu.save()
                           newuser = User(num=stu_num, pwd=stu_num, power='学生', name=stu_name)
                           newuser.save()
            else:
                for row in range(1, stu_sheet.nrows):
                    stu_num = str(str(stu_sheet.row_values(row)[stu_num_index]).split('.')[0])  # 学号
                    stu = Student.objects.filter(num=stu_num)
                    if stu:
                        msg=msg+"\n已存在学号为"+stu_num+"的学生"
                    else:
                        stu_name = str(stu_sheet.row_values(row)[stu_name_index])  # 姓名
                        stu_bj = str(stu_sheet.row_values(row)[stu_grade_index])  # 班级
                        print(stu_num + stu_name + stu_bj)  # 取出每行数据 可以写入数据库
                        newstu = Student(num=stu_num, name=stu_name, grade=stu_bj, score=0, group_id=0, group_role='尚未指定')
                        newuser = User(num=stu_num, pwd=stu_num, power='学生', name=stu_name)
                        newstu.save()
                        newuser.save()
            group_info = xlrd.open_workbook(filename=None, file_contents=groupfile.read())
            group_sheet = group_info.sheet_by_index(0)
            group_t = group_sheet.row_values(0)
            for row in range(0, len(group_t)):
                if group_t[row] == '小组编号':
                    group_num_index = row
                if group_t[row] == '学习主题':
                    group_con_index = row
            for row in range(1, group_sheet.nrows):
                group_num = str(str(group_sheet.row_values(row)[group_num_index]).split('.')[0])  # 小组编号
                group_con = str(group_sheet.row_values(row)[group_con_index])  # 学习主题
                is_same=search.id_is_same(group_num,group_con)
                if is_same:
                    msg=msg+'\n已存在'+group_con+'该学习主题,无法加入数据库'
                else:
                    print(group_num + group_con)  # 取出每行数据 可以写入数据库
                    newgroup = UserGroup(group_id=group_num, topic=group_con, group_score=0)
                    newgroup.save()
            # 拼接绝对路径 上传文件至目录
            import os
            file_path = os.path.join(settings.BASE_DIR, 'statics', 'init_info', stufile_name)
            file_path1 = os.path.join(settings.BASE_DIR, 'statics', 'init_info', groupfile_name)
            with open(file_path, 'wb')as f:
                for chunk in stufile.chunks():
                    f.write(chunk)
            with open(file_path1, 'wb')as f:
                for chunk in stufile.chunks():
                    f.write(chunk)
            # 新增初始文件信息
            import datetime
            dt = datetime.datetime.now()
            now = dt.strftime('%Y-%m-%d %H:%M:%S %p')
            stufile_type = str(str(stufile_name).split('.')[1])  # 获取文件的拓展名
            print(stufile_type)
            groupfile_type = str(str(groupfile_name).split('.')[1])  # 获取文件的拓展名
            newstufile = init_info(file_name=stufile_name, file_path=file_path, file_time=now, file_type=stufile_type)
            newgroupfile = init_info(file_name=groupfile_name, file_path=file_path1, file_time=now,
                                     file_type=groupfile_type)
            newstufile.save()
            newgroupfile.save()
            # 教师教学信息添加
            dt = datetime.datetime.now()
            now = dt.strftime('%Y-%m-%d %H:%M:%S %p')
            newlearnobj = learn_obj(obj_topic=obj_topic, obj_content=obj_content, obj_time=now, obj_author=obj_author,
                                    obj_type=1)
            newlearnobj.save()
            back_dic['resultCode'] = 200
            back_dic['msg'] = '已提交初始信息，学生信息与小组信息均已保存'+msg
            return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e)+"上传文件类型有误，只支持xls和xlsx格式的Excel文档"
        return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
  else:
    back_dic['resultCode'] = -1
    back_dic['msg'] = '出现错误'
    return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def add_stuinits(request):#学生信息上传
  back_dic = {'resultCode': None, 'msg': None}
  print(request.session.get('num'))
  if request.method =='POST':
    stu_num=request.POST.get('stu_num')
    stu_name=request.POST.get('stu_name')
    stu_grade = request.POST.get('stu_grade')
    group_id = request.POST.get('group_id')
    num=Student.objects.filter(num=stu_num)
    if num:
        back_dic['resultCode'] = -1
        back_dic['msg'] = '存在'+stu_num+'该学号学生'
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    try:
        with transaction.atomic():
            newstu = Student(num=stu_num, name=stu_name, grade=stu_grade, score=0, group_id=group_id, group_role='尚未指定')
            newuser = User(num=stu_num, pwd=stu_num, power='学生', name=stu_name)
            newstu.save()
            newuser.save()
            back_dic['resultCode'] = 200
            back_dic['msg'] = '已提交初始信息，新学生信息已保存'
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e) + "添加错误"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
  else:
    back_dic['resultCode'] = -1
    back_dic['msg'] = '出现错误'
    return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def edit_userinfo(request):#设置用户信息
  back_dic = {'resultCode': None, 'msg': None}
  if request.method =='POST':
    stu_num=request.POST.get('stu_num')
    stu_name=request.POST.get('stu_name')
    stu_grade = request.POST.get('stu_grade')
    stu_phone = request.POST.get('stu_phone')
    stu_email = request.POST.get('stu_email')
    num=Student.objects.filter(num=stu_num)
    if not num:
        back_dic['resultCode'] = -1
        back_dic['msg'] = '不存在'+stu_num+'该学号学生'
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    try:
        with transaction.atomic():
            Student.objects.filter(num=stu_num).update(
                 name=stu_name,
                grade=stu_grade
            )
            User.objects.filter(num=stu_num).update(
                    name=stu_name,
                    phone=stu_phone,
                    email=stu_email
                )
            back_dic['resultCode'] = 200
            back_dic['msg'] = '已修改用户信息'
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e) + "修改错误"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
  else:
    back_dic['resultCode'] = -1
    back_dic['msg'] = '出现错误'
    return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def pwd_edit(request):#修改密码
  back_dic = {'resultCode': None, 'msg': None}
  if request.method =='POST':
    stu_num=request.POST.get('stu_num')
    stu_name=request.POST.get('stu_name')
    pwd = request.POST.get('password')
    try:
        with transaction.atomic():
            User.objects.filter(num=stu_num).update(
                   pwd=pwd
                )
            back_dic['resultCode'] = 200
            back_dic['msg'] = '密码修改成功'
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e) + "修改错误"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
  else:
    back_dic['resultCode'] = -1
    back_dic['msg'] = '出现错误'
    return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def add_groupsinitinfo(request):#小组信息上传
  back_dic = {'resultCode': None, 'msg': None}
  if request.method=='POST':
    group_num=request.POST.get('group_num')
    group_topic=request.POST.get('group_topic')
    print(group_topic)
    try:
        with transaction.atomic():
                newgroup = UserGroup(group_id=group_num, topic=group_topic, group_score=0)
                newgroup.save()
                back_dic['resultCode'] = 200
                back_dic['msg'] = '已提交初始信息，小组信息已保存'
                return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e)+"添加错误"
        return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
  else:
    back_dic['resultCode'] = -1
    back_dic['msg'] = '出现错误'
    return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def displaystu(request):#初始化系统信息上传
  back_dic = {'resultCode': None, 'msg': None,'rows':None,'cols':None,'stu_list':None}
  if request.method=='POST':
    stufile=request.FILES.get('stufile',None)
    stufile_name=stufile.name #获取文件名字
    stu_list=[]
    col_list = []
    print(stufile_name)
    # 解析excel文件
    try:
        with transaction.atomic():
            stu_info = xlrd.open_workbook(filename=None, file_contents=stufile.read())
            stu_sheet = stu_info.sheet_by_index(0)
            stu_t = stu_sheet.row_values(0) #取出表头元素

            stu_col=stu_sheet.ncols #记录列数
            stu_row=stu_sheet.nrows #记录行数

            for row in range(0, stu_sheet.nrows):
                data=[]
                for col in range(0, stu_sheet.ncols):
                    data.append(str(stu_sheet.row_values(row)[col]))
                stu_list.extend(data)
                #stu_num = str(str(stu_sheet.row_values(row)[0]).split('.')[0])  # 学号
                #stu_name = str(stu_sheet.row_values(row)[1])  # 姓名
                #stu_bj = str(stu_sheet.row_values(row)[2])  # 班级
                #stu_list.extend([stu_num,stu_name,stu_bj])
            back_dic['resultCode'] = 200
            back_dic['msg'] = '学生数据加载完毕'
            back_dic['rows']=stu_row
            back_dic['cols'] = stu_col
            back_dic['stu_list']=stu_list
            return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e)+"上传文件类型有误，只支持xls和xlsx格式的Excel文档"
        return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
  else:
    back_dic['resultCode'] = -1
    back_dic['msg'] = '出现错误'
    return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def displaydata(request):#初始化系统信息上传
  back_dic = {'resultCode': None, 'msg': None,'rows':None,'cols':None,'stu_list':None}
  if request.method=='POST':
    learnfile=request.FILES.get('learnfile',None)
    learnfile_name=learnfile.name #获取文件名字
    learn_list=[]
    col_list = []
    flag=0
    print(learnfile_name)
    # 解析excel文件
    try:
        with transaction.atomic():
            learn_info = xlrd.open_workbook(filename=None, file_contents=learnfile.read())
            learn_sheet = learn_info.sheet_by_index(0)
            learn_t = learn_sheet.row_values(0) #取出表头元素
            learn_col=learn_sheet.ncols #记录列数
            learn_row=learn_sheet.nrows #记录行数
            for row in range(0, learn_sheet.nrows):
                for col in range(0, learn_sheet.ncols):
                   col_list.append(str(learn_sheet.row_values(row)[col]))
                learn_list.extend(col_list)
                col_list = []
            back_dic['resultCode'] = 200
            back_dic['msg'] = '文件数据加载完毕'
            back_dic['rows']=learn_row
            back_dic['cols'] = learn_col
            back_dic['learn_list']=learn_list
            return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e)+"上传文件类型有误，只支持xls和xlsx格式的Excel文档"
        return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
  else:
    back_dic['resultCode'] = -1
    back_dic['msg'] = '出现错误'
    return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def dp_talkdata(request):#管理聊天记录
  back_dic = {'resultCode': None, 'msg': None,'rows':None,'cols':None,'stu_list':None}
  if request.method=='POST':
    group_id=request.POST.get('group_id')
    title = "第" + group_id + "组聊天记录"
    file_name = title + '.xls'
    import os
    file_path = os.path.join(settings.BASE_DIR, 'statics', 'group_talk', file_name)
    if os.path.exists(file_path):
        learnfile_name=file_name
        learn_list=[]
        col_list = []
        flag=0
        print(learnfile_name)
        # 解析excel文件
        try:
            with transaction.atomic():
                learn_info = xlrd.open_workbook(file_path)
                learn_sheet = learn_info.sheet_by_index(0)
                learn_t = learn_sheet.row_values(0) #取出表头元素
                learn_col=learn_sheet.ncols #记录列数
                learn_row=learn_sheet.nrows #记录行数
                for row in range(0, learn_sheet.nrows):
                    for col in range(0, learn_sheet.ncols):
                       col_list.append(str(learn_sheet.row_values(row)[col]))
                    learn_list.extend(col_list)
                    col_list = []
                back_dic['resultCode'] = 200
                back_dic['msg'] = '文件数据加载完毕'
                back_dic['rows']=learn_row
                back_dic['cols'] = learn_col
                back_dic['learn_list']=learn_list
                return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
        except Exception as e:
            print(e)
            back_dic['resultCode'] = -1
            back_dic['msg'] = str(e)+"上传文件类型有误，只支持xls和xlsx格式的Excel文档"
            return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
    else:
        back_dic['resultCode'] = -1
        back_dic['msg'] = '不存在聊天记录文件,请先导出聊天记录后，管理聊天记录'
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
  else:
    back_dic['resultCode'] = -1
    back_dic['msg'] = '出现错误'
    return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def dataview(request):#数据可视化
  back_dic = {'resultCode': None, 'msg': None,'rows':None,'cols':None }
  if request.method=='POST':
    learnfile=request.FILES.get('learnfile',None)
    learnfile_name=learnfile.name #获取文件名字
    x_data=request.POST.get('xdata')
    y_data = request.POST.get('ydata')
    x_list = []
    y_list = []
    null_list = []
    flag=0;
    print(learnfile_name)
    # 解析excel文件
    try:
        with transaction.atomic():
            learn_info = xlrd.open_workbook(filename=None, file_contents=learnfile.read())
            learn_sheet = learn_info.sheet_by_index(0)
            learn_t = learn_sheet.row_values(0) #取出表头元素
            learn_col=learn_sheet.ncols #记录列数
            learn_row=learn_sheet.nrows #记录行数
            for row in range(1, learn_sheet.nrows):
                s=str(learn_sheet.row_values(row)[int(x_data)])
                if s.strip() == '':
                    null_list.append(row);
                    print(str(row)+'s is null')
                elif s.strip() == '-':
                    null_list.append(row);
                    print(str(row)+'s is -')
                else:
                    x_list.append(str(learn_sheet.row_values(row)[int(x_data)]))
            for row in range(1, learn_sheet.nrows):
                if len(null_list):
                    if row == null_list[flag]:
                        print(str(row) + ' is null')

                        if flag < len(null_list) - 1:
                            flag = flag + 1
                    else:
                        y_list.append(str(learn_sheet.row_values(row)[int(y_data)]))
                else:
                    s = str(learn_sheet.row_values(row)[int(y_data)])
                    if s.strip() != '-' and s.strip() != '':
                        print(s)
                        y_list.append(str(learn_sheet.row_values(row)[int(y_data)]))
                    else :
                        x_list.remove(str(learn_sheet.row_values(row)[int(x_data)]))

            back_dic['resultCode'] = 200
            back_dic['msg'] = '文件数据加载完毕'
            back_dic['rows']=learn_row
            back_dic['cols'] = learn_col
            back_dic['x_name'] =str(learn_sheet.row_values(0)[int(x_data)])
            back_dic['y_name'] =str(learn_sheet.row_values(0)[int(y_data)])
            back_dic['x_list']= x_list
            back_dic['y_list'] = y_list
            return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e)+"上传文件类型有误，只支持xls和xlsx格式的Excel文档"
        return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
  else:
    back_dic['resultCode'] = -1
    back_dic['msg'] = '出现错误'
    return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def displaygroup(request):  # 初始化系统信息上传
      back_dic = {'resultCode': None, 'msg': None, 'rows': None, 'cols': None, 'group_list': None}
      if request.method == 'POST':
          groupfile = request.FILES.get('groupfile', None)
          groupfile_name = groupfile.name  # 获取文件名字
          group_list = []
          # 解析excel文件
          try:
              with transaction.atomic():
                  group_info = xlrd.open_workbook(filename=None, file_contents=groupfile.read())
                  group_sheet = group_info.sheet_by_index(0)
                  group_t = group_sheet.row_values(0)  # 取出表头元素
                  group_col = group_sheet.ncols  # 记录列数
                  group_row = group_sheet.nrows  # 记录行数
                  for row in range(0, group_sheet.nrows):
                      group_num = str(str(group_sheet.row_values(row)[0]).split('.')[0])  # 小组编号
                      group_name = str(group_sheet.row_values(row)[1])  # 学习主题
                      group_list.extend([group_num, group_name])
                  back_dic['resultCode'] = 200
                  back_dic['msg'] = '小组数据加载完毕'
                  back_dic['rows'] = group_row
                  back_dic['cols'] = group_col
                  back_dic['group_list'] = group_list
                  return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
          except Exception as e:
              print(e)
              back_dic['resultCode'] = -1
              back_dic['msg'] = str(e) + "上传文件类型有误，只支持xls和xlsx格式的Excel文档"
              return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
      else:
          back_dic['resultCode'] = -1
          back_dic['msg'] = '出现错误'
          return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def indextech(request):#进入教师主页
    # 教师管理界面
    flag = 0
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    alldata = {}
    num = request.session.get('num')  # 获取教工号
    notice_list = search.get_notice(num)
    if num == None:  # 需要登录
        return render(request, 'index.html', context=value)
    #找出已发布任务的小组
    task_info=list(task.objects.values("group_id").annotate(count_task=Count("task_id")));
    # 找出已完成任务的小组
    task_fininfo =list(task.objects.filter(is_finish=1).values("group_id").annotate(count_task=Count("task_id"))) ;
    #print(task_info)
    flag=1
    if len(task_info)>len(task_fininfo):
          for i in task_info:
              newgroup=list(UserGroup.objects.filter(group_id=i['group_id']).values("group_id","topic"))
              group_topic=newgroup[0]['topic']
              for j in task_fininfo:
                if i['group_id'] == j['group_id']:
                       j['task_total']=i['count_task']
                       j['task_topic'] = group_topic
                       task_percent=str(round(int(j['count_task'])/int(j['task_total'])*100,2))
                       j['percent'] =task_percent+'%'
                       flag=0
              if flag == 1:
                task_fininfo.append({'group_id': i['group_id'], 'count_task': 0,'task_total':i['count_task']
                                        ,'task_topic':group_topic
                                        ,'percent': '0%'
                                     })
              else :
                  flag=1
    alldata['task_fininfo']=task_fininfo
    alldata['notice_list'] = notice_list
    return render(request, 'index_tech.html', alldata)
def enter_talking(request):#教师界面-进入小组讨论区
    # 教师管理界面
    flag = 0
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    alldata = {}
    num = request.session.get('num')  # 获取教工号
    if num == None:  # 需要登录
        return render(request, 'index.html', context=value)
    group_list=list(UserGroup.objects.all().values("group_id","topic"))
    alldata['group_list']=group_list
    notice_list=search.get_notice(num)
    alldata['notice_list'] = notice_list
    return render(request,'enter_grouptalk.html',alldata)
def talk_manage(request):#bms-小组讨论管理
    # 教师管理界面
    flag = 0
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    alldata = {}
    num = request.session.get('num')  # 获取教工号
    if num == None:  # 需要登录
        return render(request, 'index.html', context=value)
    group_list=list(UserGroup.objects.all().values("group_id","topic"))
    alldata['group_list']=group_list
    return render(request,'talk_manage.html',alldata)
def mark_assess(request):#教师界面-成绩评分
    # 教师管理界面
    flag = 0
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    alldata = {}
    num = request.session.get('num')  # 获取教工号
    if num == None:  # 需要登录
        return render(request, 'index.html', context=value)
    group_list=list(UserGroup.objects.all().values("group_id","topic"))
    for item in group_list:
        stu_list=list(Student.objects.filter(group_id=item['group_id']).values("num","name","group_role","score"))
        if stu_list:
            item['stu_list']=stu_list
        else :
            item['stu_list'] = [{'name':'无'}]
    group_multiple = search.get_multiple(num)  # 获得小组多元综合评价
    search.get_multiplescore(group_multiple,group_list)#变成百分制
    alldata['group_list']=group_list
    notice_list=search.get_notice(num)
    alldata['notice_list'] = notice_list
    return render(request,'mark_assess.html',alldata)
def submitfinalscore(request):
    back_dic = {'resultCode': None, 'msg': None}
    if request.method == 'POST':
        group_id=request.POST.get('group_id')
        group_score=float(request.POST.get('group_score'))
        UserGroup.objects.filter(group_id=group_id).update(
            group_score=group_score
        )
        back_dic['resultCode'] = 200
        back_dic['msg'] = '已提交小组综合成绩'
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    else:
        back_dic['resultCode'] = -1
        back_dic['msg'] = '出现错误'
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def upload_stuscore(request):
    back_dic = {'resultCode': None, 'msg': None}
    data=[]
    if request.method == 'POST':
        stu_file=request.FILES.get('stu_file',None)
        # 写入服务器中
        try:
            with transaction.atomic():
                score_info = xlrd.open_workbook(filename=None, file_contents=stu_file.read())
                score_sheet = score_info.sheet_by_index(0)
                score_t = score_sheet.row_values(0)
                for title in range(0, len(score_t)):
                    if score_t[title] == '学号':
                        num_index = title
                    elif score_t[title] == '成绩' or score_t[title] == '得分':
                        score_index = title
                for row in range(1, score_sheet.nrows):
                    stu_num = str(score_sheet.row_values(row)[num_index]).split('.')[0]
                    group_id=Student.objects.filter(num=stu_num).first().group_id
                    group_score=UserGroup.objects.filter(group_id=group_id).first().group_score
                    stu_score=float(score_sheet.row_values(row)[score_index])
                    data.append({'num':stu_num,'group_id':group_id,'group_score':group_score,'score':stu_score})
                back_dic['resultCode'] = 200
                back_dic['msg'] = '发送成功'
                back_dic['data'] = data
                return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
        except Exception as e:
            print(e)
            back_dic['resultCode'] = -1
            back_dic['msg'] = str(e) + "上传有误,请按照正确格式上传excel文件"
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    else:
        back_dic['resultCode'] = -1
        back_dic['msg'] = '出现错误'
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def uploadselfscore(request):#上传个人成绩
    back_dic = {'resultCode': None, 'msg': None}
    if request.method == 'POST':
        submit_data=json.loads(request.POST.get('submit_data'))
        # 写入数据库中
        try:
            with transaction.atomic():
                for item in submit_data:
                    num=item['num']
                    Student.objects.filter(num=num).update(
                        score=float(item['score'])
                    )
                back_dic['resultCode'] = 200
                back_dic['msg'] = '提交成功！'
                return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
        except Exception as e:
            print(e)
            back_dic['resultCode'] = -1
            back_dic['msg'] = str(e) + "上传有误,请按照正确格式上传excel文件"
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    else:
        back_dic['resultCode'] = -1
        back_dic['msg'] = '出现错误'
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def feedbackemail(request):#教师主页-反馈邮箱
    # 教师管理-反馈邮箱
    flag = 0
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    alldata = {}
    num = request.session.get('num')  # 获取教工号
    if num == None:  # 需要登录
        return render(request, 'index.html', context=value)
    import os
    feedback_list=list(feed_back.objects.exclude(feedback_type=4).values())
    for item in feedback_list:
        file_count=item['feedback_file']
        num=item['num']
        name=list(Student.objects.filter(num=num).values('name'))[0]['name']
        group_role = list(Student.objects.filter(num=num).values('group_role'))[0]['group_role']
        item['name']=name
        item['group_role']=group_role
        fb_id=item['feedback_id']
        file_list=list(feedbackfile.objects.filter(feedback_id=fb_id).values('file_path'))
        for files in file_list:
            files_path=files['file_path']
            if os.sep in files_path:
                file_name = files_path.split('\\')[-1]
            else:
                file_name = files_path.split('/')[-1]
            file_path = os.path.join(settings.BASE_DIR, 'statics', 'feedbackfile', file_name)
            print(file_path)
            fsize = os.path.getsize(file_path)
            fsize = round(fsize / float(1024)) #转换文件大小为KB
            files['file_name']=file_name
            files['file_path'] = file_path
            files['fsize'] = fsize
        item['file_list']=file_list
    alldata['feedback_list']=feedback_list
    notice_list=search.get_notice(num)
    alldata['notice_list'] = notice_list
    return render(request, 'tech_feedbackemail.html', alldata)
def data_analysis(request):#教师主页-评论分析
    flag = 0
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    alldata = {}
    num = request.session.get('num')  # 获取教工号
    if num == None:  # 需要登录
        return render(request, 'index.html', context=value)
    title_list=search.get_title('组内评价')
    avg_list=[]
    eva_list = list(eva_recollect.objects.filter(eva_type='组内评价') \
                    .values("pj_id") \
                    .annotate(count=Count('pj_id')) \
                    .values("pj_id", "valuer_num", "eva_type","group_id"))
    group_list=list(UserGroup.objects.all().values())
    for item in group_list:
        flag=0
        count=0
        member_weight = search.group_weight(item)  # 计算各组的权重
        for eva in eva_list:
            stu_list=list(eva_recollect.objects.filter(pj_id=eva['pj_id'],group_id=item['group_id']).values("pj_id","valuer_num","eva_id","eva_content","group_id"))
            if stu_list:
                if flag == 0:
                    for score in stu_list:
                        question = Evaluate.objects.filter(evaluate_id=score['eva_id']).first().evaluate_item
                        item[str(question)] = search.sum_weight(int(score['eva_content']),score['valuer_num'],member_weight)
                    count=count+1
                else:
                    for score in stu_list:
                        question = Evaluate.objects.filter(evaluate_id=score['eva_id']).first().evaluate_item
                        item[str(question)]=round(item[str(question)]+search.sum_weight(int(score['eva_content']),score['valuer_num'],member_weight),2)
                    count = count + 1
                flag=1
        #计算平均
        search.averagescore(item,count,title_list,avg_list)
    groups_list=search.diffgroupavg()#计算组间互评的加权平均
    group_evadata=search.get_titledata()
    titles_list = search.get_title('组间互评')
    group_multiple=search.get_multiple(num)#获得小组多元综合评价
    multi_title_list=search.get_title('多元评价')
    notice_list=search.get_notice(num)
    alldata['group_evadata'] = group_evadata
    alldata['groups_list'] = groups_list
    alldata['titles_list'] = titles_list
    alldata['multi_title_list'] = multi_title_list
    alldata['group_multiple'] = group_multiple
    alldata['title_list']=title_list
    alldata['group_list']=group_list
    alldata['avg_list'] = avg_list
    alldata['notice_list'] = notice_list
    return render(request, 'tech_dataanalysis.html', alldata)
def detail_groupinfo(request):
    flag = 0
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    alldata = {}
    num = request.session.get('num')  # 获取教工号
    if num == None:  # 需要登录
        return render(request, 'index.html', context=value)
    group_id=request.GET.get('group_id')
    group_list=list(UserGroup.objects.filter(group_id=group_id).values())
    for item in group_list:
        stu_list=list(Student.objects.filter(group_id=item['group_id']).values())
        item['stu_list']=stu_list
    group_data=search.get_groupeva(group_id,'组内评价')
    title_list = search.get_titles('组内评价')
    member_weight = search.group_weight({'group_id':group_id})  # 计算权重
    time_data=search.get_grouplearn()#获得小组平均学习时长
    task_finished=search.get_grouptask(group_id)#获得小组成员任务完成情况
    member_time_data=search.get_membertimedata(group_id)#获取小组成员个人评价信息
    member_rank_list=search.get_memberrank(group_id)#获取小组成员个人排名
    #小组发帖词云
    tag_data=search.get_wordcloud(group_id)#获取小组词频权重
    alldata['title_list'] = title_list
    alldata['group_data'] = group_data
    alldata['group_list'] = group_list
    alldata['time_data'] = time_data
    alldata['member_weight'] = member_weight
    alldata['task_finished'] = task_finished #小组任务完成情况
    alldata['member_time_data'] = member_time_data  #小组成员学习时长对比
    alldata['member_rank_list'] = member_rank_list  # 小组成员个人评价排名
    alldata['chat_data'] = tag_data  # 小组词频权重
    alldata['group_id'] = int(group_id)
    notice_list=search.get_notice(num)
    alldata['notice_list'] = notice_list
    return render(request,'dataanalysis_detail.html', alldata)
def detail_memberinfo(request):
    flag = 0
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    alldata = {}
    num = request.session.get('num')  # 获取学号
    if num == None:  # 需要登录
        return render(request, 'index.html', context=value)
    num=request.GET.get('num')
    stu_info=list(Student.objects.filter(num=num).values("num","name","group_id","group_role"))
    group_list = list(UserGroup.objects.filter(group_id=stu_info[0]['group_id']).values())
    for item in group_list:
        member_list = list(Student.objects.filter(group_id=item['group_id']).values())
    self_eva=search.get_selfeva(num)
    inter_eva = search.get_intereva(num)
    inter_title_list=search.get_titles('成员互评')
    title_list=search.get_titles('个人评价')
    chat_data=search.get_memberwordcloud(num)
    alldata['stu_info'] = stu_info #用户信息
    alldata['member_list'] = member_list
    alldata['group_list'] = group_list
    alldata['self_eva'] = self_eva
    alldata['inter_eva'] = inter_eva
    alldata['inter_title_list'] = inter_title_list
    alldata['title_list'] = title_list
    alldata['chat_data'] = chat_data
    alldata['group_id'] = int(stu_info[0]['group_id'])
    notice_list=search.get_notice(request.session.get('num'))
    alldata['notice_list'] = notice_list
    return render(request,'dataanalysis_member_detail.html', alldata)
def stu_pj_manage(request):#学生主页-评论管理
    flag = 0
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    alldata = {}
    num = request.session.get('num')  # 获取教工号
    if num == None:  # 需要登录
        return render(request, 'index.html', context=value)
    if request.method=='GET':
        stu_num=request.GET.get('stu_num')
        eva_list = list(eva_recollect.objects.filter(valuer_num=stu_num)\
                        .values("pj_id")\
                        .annotate(count=Count('id'))\
                        .values("pj_id","valuer_num", "count", "group_id","eva_type"))
        for item in eva_list:
            item['eva_time']=eva_recollect.objects.filter(pj_id=item['pj_id']).first().eva_time.strftime('%Y-%m-%d %H:%M:%S %p')
            item['beeva_num'] = eva_recollect.objects.filter(pj_id=item['pj_id']).first().beeva_num
            if item['eva_type']=='成员互评':
                item['beeva_num']=Student.objects.filter(num=item['beeva_num']).first().name
            elif item['eva_type']=='组间互评':
                item['beeva_num'] = '第'+item['beeva_num']+'组'+'('+UserGroup.objects.filter(group_id=item['beeva_num']).first().topic+')'
        alldata['eva_list']=eva_list
        notice_list=search.get_notice(num)
        alldata['notice_list'] = notice_list
        return render(request, 'stu_pj_manage.html', alldata)
    else:
      return render(request, 'index.html', alldata)
def tech_eva_manage(request):#教师主页-评论管理
    flag = 0
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    alldata = {}
    num = request.session.get('num')  # 获取教工号
    if num == None:  # 需要登录
        return render(request, 'index.html', context=value)
    if request.method=='GET':
        eva_type=request.GET.get('eva')
        if eva_type == 'stu':
            #学生自评
            eva_list=list(eva_recollect.objects.filter(eva_type='个人评价')\
                .values("valuer_num")\
                .annotate(count=Count('id'))\
                .values("valuer_num","count","group_id"))
            for item in eva_list:
                item['valuer_name'] = Student.objects.filter(num=item['valuer_num']).first().name
                item['valuer_class'] = Student.objects.filter(num=item['valuer_num']).first().grade
                item['eva_type']='个人评价'
                item['eva_time']=eva_recollect.objects.filter(eva_type='个人评价',valuer_num=item['valuer_num']).first().eva_time.strftime('%Y-%m-%d %H:%M:%S %p')
                item['beeva_num']=Student.objects.filter(num=item['valuer_num']).first().name
                item['beeva_name'] = eva_recollect.objects.filter(eva_type='个人评价', valuer_num=item[
                    'valuer_num']).first().beeva_num
                item['act_name']=UserGroup.objects.filter(group_id=item['group_id']).first().topic

        elif eva_type == 'group':
            #小组自评
            eva_list = list(eva_recollect.objects.filter(eva_type='组内评价') \
                            .values("valuer_num") \
                            .annotate(count=Count('id')) \
                            .values("valuer_num", "count", "group_id"))
            for item in eva_list:
                item['valuer_name'] = Student.objects.filter(num=item['valuer_num']).first().name
                item['valuer_class'] = Student.objects.filter(num=item['valuer_num']).first().grade
                item['eva_type'] = '组内评价'
                item['eva_time'] = eva_recollect.objects.filter(eva_type='组内评价', valuer_num=item[
                    'valuer_num']).first().eva_time.strftime('%Y-%m-%d %H:%M:%S %p')
                item['beeva_num'] = "第"+str(Student.objects.filter(num=item['valuer_num']).first().group_id)+"组"
                item['beeva_name'] = eva_recollect.objects.filter(eva_type='组内评价', valuer_num=item[
                        'valuer_num']).first().beeva_num
                item['act_name'] = UserGroup.objects.filter(group_id=item['group_id']).first().topic


        elif eva_type == 'groups':
            #小组互评
            data=[]
            eva_list = list(eva_recollect.objects.filter(eva_type='组间互评')\
                            .values("valuer_num")\
                            .annotate(count=Count('id'))\
                            .values("valuer_num", "count", "group_id"))
            for item in eva_list:
                eva_group_list=list(eva_recollect.objects.filter(valuer_num=item['valuer_num'],eva_type='组间互评')\
                            .values("beeva_num")\
                            .annotate(count=Count('id'))\
                            .values("valuer_num","beeva_num", "count", "group_id"))
                for elist in eva_group_list:
                    elist['valuer_name'] = Student.objects.filter(num=elist['valuer_num']).first().name
                    elist['valuer_class'] = Student.objects.filter(num=elist['valuer_num']).first().grade
                    elist['eva_type'] = '组间互评'
                    elist['eva_time'] = eva_recollect.objects.filter(eva_type='组间互评',valuer_num=elist[
                      'valuer_num'] ,beeva_num=elist['beeva_num']).first().eva_time.strftime('%Y-%m-%d %H:%M:%S %p')
                    elist['beeva_name'] =eva_recollect.objects.filter(eva_type='组间互评', beeva_num=elist[
                        'beeva_num'],valuer_num=elist['valuer_num']).first().beeva_num
                    elist['beeva_num'] = '第' + str(eva_recollect.objects.filter(eva_type='组间互评',beeva_num=elist[
                        'beeva_num'], valuer_num=elist['valuer_num']).first().beeva_num) + '组'
                    elist['act_name'] = UserGroup.objects.filter(group_id=elist['group_id']).first().topic
                    data.append(elist)
            eva_list=data

        elif eva_type == 'member':
            #成员互评
            data = []
            eva_list = list(eva_recollect.objects.filter(eva_type='成员互评') \
                            .values("valuer_num") \
                            .annotate(count=Count('id')) \
                            .values("valuer_num", "count", "group_id"))
            for item in eva_list:
                eva_group_list = list(eva_recollect.objects.filter(valuer_num=item['valuer_num'], eva_type='成员互评') \
                                      .values("beeva_num") \
                                      .annotate(count=Count('id')) \
                                      .values("valuer_num", "beeva_num", "count", "group_id"))
                for elist in eva_group_list:
                    elist['valuer_name'] = Student.objects.filter(num=elist['valuer_num']).first().name
                    elist['valuer_class'] = Student.objects.filter(num=elist['valuer_num']).first().grade
                    elist['eva_type'] = '成员互评'
                    elist['eva_time'] = eva_recollect.objects.filter(eva_type='成员互评', beeva_num=elist[
                        'beeva_num'],valuer_num=elist[
                        'valuer_num']).first().eva_time.strftime('%Y-%m-%d %H:%M:%S %p')
                    elist['beeva_name'] = eva_recollect.objects.filter(eva_type='成员互评',beeva_num=elist[
                        'beeva_num'], valuer_num=elist[
                        'valuer_num']).first().beeva_num
                    elist['beeva_num'] = Student.objects.filter(num=elist['beeva_name']).first().name
                    elist['act_name'] = UserGroup.objects.filter(group_id=elist['group_id']).first().topic
                    data.append(elist)
            eva_list = data

        elif eva_type == 'teacher':
            #教师评价
            data = []
            eva_list = list(eva_recollect.objects.filter(eva_type='教师评价') \
                            .values("valuer_num") \
                            .annotate(count=Count('id')) \
                            .values("valuer_num", "count", "group_id"))
            for item in eva_list:
                eva_group_list = list(eva_recollect.objects.filter(valuer_num=item['valuer_num'], eva_type='教师评价') \
                                      .values("beeva_num") \
                                      .annotate(count=Count('id')) \
                                      .values("valuer_num", "beeva_num", "count", "group_id"))
                for elist in eva_group_list:
                    elist['valuer_name'] = User.objects.filter(num=elist['valuer_num']).first().name
                    elist['valuer_class'] = '无'
                    elist['eva_type'] = '教师评价'
                    elist['pj_id'] = eva_recollect.objects.filter(eva_type='教师评价', beeva_num=elist[
                        'beeva_num'], valuer_num=elist['valuer_num']).first().pj_id
                    elist['eva_time'] = eva_recollect.objects.filter(eva_type='教师评价', beeva_num=elist[
                        'beeva_num'],valuer_num=elist[
                        'valuer_num']).first().eva_time.strftime('%Y-%m-%d %H:%M:%S %p')
                    elist['beeva_name'] = eva_recollect.objects.filter(eva_type='教师评价', beeva_num=elist[
                        'beeva_num'], valuer_num=elist['valuer_num']).first().beeva_num
                    elist['beeva_num'] = '第' + str(eva_recollect.objects.filter(eva_type='教师评价', beeva_num=elist[
                        'beeva_num'], valuer_num=elist['valuer_num']).first().beeva_num) + '组'
                    elist['act_name'] = UserGroup.objects.filter(group_id=elist['beeva_name']).first().topic
                    data.append(elist)
            eva_list = data

        alldata['eva_list']=eva_list
        notice_list=search.get_notice(num)
        alldata['notice_list'] = notice_list
        return render(request, 'tech_evamanage.html', alldata)
    else:
      return render(request, 'index.html', alldata)
def display_eva(request):#教师主页-评论信息展示
    back_dic = {'resultCode': None, 'msg': None}
    if request.method == 'POST':
        eva_type = request.POST.get('eva_type')
        valuer_num = request.POST.get('valuer_num')
        beeva_num=request.POST.get('beeva_num')
        eva_list=list(eva_recollect.objects.filter(eva_type=eva_type,valuer_num=valuer_num,beeva_num=beeva_num).values())
        for item in eva_list:
            item['eva_time']=item['eva_time'].strftime('%Y-%m-%d %H:%M:%S %p')
            item['valuer_name'] = Student.objects.filter(num=item['valuer_num']).first().name
            item['eva_title'] = Evaluate.objects.filter(evaluate_id=item['eva_id']).first().evaluate_item
        back_dic['resultCode'] = 200
        back_dic['msg'] = '文件数据加载完毕'
        back_dic['eva_list'] = eva_list
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    else:
        back_dic['resultCode'] = -1
        back_dic['msg'] = '出现错误'
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def bms_eva(request):#后台-评论管理
    flag = 0
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    alldata = {}
    num = request.session.get('num')  # 获取教工号
    if num == None:  # 需要登录
        return render(request, 'index.html', context=value)
    if request.method=='GET':
        eva_type=request.GET.get('eva')
        if eva_type == 'stu':
            #学生自评
            eva_list=list(eva_recollect.objects.filter(eva_type='个人评价')\
                .values("valuer_num")\
                .annotate(count=Count('id'))\
                .values("valuer_num","count","group_id"))
            #print(eva_list)
            for item in eva_list:
                item['pj_id'] = eva_recollect.objects.filter(eva_type='个人评价',valuer_num=item['valuer_num']).first().pj_id
                item['valuer_name'] = Student.objects.filter(num=item['valuer_num']).first().name
                item['valuer_class'] = Student.objects.filter(num=item['valuer_num']).first().grade
                item['eva_type']='个人评价'
                item['eva_time']=eva_recollect.objects.filter(eva_type='个人评价',valuer_num=item['valuer_num']).first().eva_time.strftime('%Y-%m-%d %H:%M:%S %p')
                item['beeva_num']=Student.objects.filter(num=item['valuer_num']).first().name
                item['beeva_name'] = eva_recollect.objects.filter(eva_type='个人评价', valuer_num=item[
                    'valuer_num']).first().beeva_num
                item['act_name']=UserGroup.objects.filter(group_id=item['group_id']).first().topic
            print(eva_list)
        elif eva_type == 'group':
            #小组自评
            eva_list = list(eva_recollect.objects.filter(eva_type='组内评价') \
                            .values("valuer_num") \
                            .annotate(count=Count('id')) \
                            .values("valuer_num", "count", "group_id"))
            for item in eva_list:
                item['pj_id'] = eva_recollect.objects.filter(eva_type='组内评价',valuer_num=item['valuer_num']).first().pj_id
                item['valuer_name'] = Student.objects.filter(num=item['valuer_num']).first().name
                item['valuer_class'] = Student.objects.filter(num=item['valuer_num']).first().grade
                item['eva_type'] = '组内评价'
                item['eva_time'] = eva_recollect.objects.filter(eva_type='组内评价', valuer_num=item[
                    'valuer_num']).first().eva_time.strftime('%Y-%m-%d %H:%M:%S %p')
                item['beeva_num'] = "第"+str(Student.objects.filter(num=item['valuer_num']).first().group_id)+"组"
                item['beeva_name'] = eva_recollect.objects.filter(eva_type='组内评价', valuer_num=item[
                        'valuer_num']).first().beeva_num
                item['act_name'] = UserGroup.objects.filter(group_id=item['group_id']).first().topic
            print(eva_list)

        elif eva_type == 'groups':
            #小组互评
            data=[]
            eva_list = list(eva_recollect.objects.filter(eva_type='组间互评')\
                            .values("valuer_num")\
                            .annotate(count=Count('id'))\
                            .values("valuer_num", "count", "group_id"))
            for item in eva_list:
                eva_group_list=list(eva_recollect.objects.filter(valuer_num=item['valuer_num'],eva_type='组间互评')\
                            .values("beeva_num")\
                            .annotate(count=Count('id'))\
                            .values("valuer_num","beeva_num", "count", "group_id"))
                for elist in eva_group_list:
                    elist['pj_id'] = eva_recollect.objects.filter(eva_type='组间互评', beeva_num=elist[
                        'beeva_num'],valuer_num=elist['valuer_num']).first().pj_id
                    elist['valuer_name'] = Student.objects.filter(num=elist['valuer_num']).first().name
                    elist['valuer_class'] = Student.objects.filter(num=elist['valuer_num']).first().grade
                    elist['eva_type'] = '组间互评'
                    elist['eva_time'] = eva_recollect.objects.filter(eva_type='组间互评',valuer_num=elist[
                      'valuer_num'] ,beeva_num=elist['beeva_num']).first().eva_time.strftime('%Y-%m-%d %H:%M:%S %p')
                    elist['beeva_name'] =eva_recollect.objects.filter(eva_type='组间互评', beeva_num=elist[
                        'beeva_num'],valuer_num=elist['valuer_num']).first().beeva_num
                    elist['beeva_num'] = '第' + str(eva_recollect.objects.filter(eva_type='组间互评',beeva_num=elist[
                        'beeva_num'], valuer_num=elist['valuer_num']).first().beeva_num) + '组'
                    elist['act_name'] = UserGroup.objects.filter(group_id=elist['group_id']).first().topic
                    data.append(elist)
            eva_list=data
            print(eva_list)
        elif eva_type == 'member':
            #成员互评
            data = []
            eva_list = list(eva_recollect.objects.filter(eva_type='成员互评') \
                            .values("valuer_num") \
                            .annotate(count=Count('id')) \
                            .values("valuer_num", "count", "group_id"))
            for item in eva_list:
                eva_group_list = list(eva_recollect.objects.filter(valuer_num=item['valuer_num'], eva_type='成员互评') \
                                      .values("beeva_num") \
                                      .annotate(count=Count('id')) \
                                      .values("valuer_num", "beeva_num", "count", "group_id"))
                for elist in eva_group_list:
                    elist['valuer_name'] = Student.objects.filter(num=elist['valuer_num']).first().name
                    elist['valuer_class'] = Student.objects.filter(num=elist['valuer_num']).first().grade
                    elist['eva_type'] = '成员互评'
                    elist['pj_id'] = eva_recollect.objects.filter(eva_type='成员互评', beeva_num=elist[
                        'beeva_num'], valuer_num=elist['valuer_num']).first().pj_id
                    elist['eva_time'] = eva_recollect.objects.filter(eva_type='成员互评', beeva_num=elist[
                        'beeva_num'],valuer_num=elist[
                        'valuer_num']).first().eva_time.strftime('%Y-%m-%d %H:%M:%S %p')
                    elist['beeva_name'] = eva_recollect.objects.filter(eva_type='成员互评',beeva_num=elist[
                        'beeva_num'], valuer_num=elist[
                        'valuer_num']).first().beeva_num
                    elist['beeva_num'] = Student.objects.filter(num=elist['beeva_name']).first().name
                    elist['act_name'] = UserGroup.objects.filter(group_id=elist['group_id']).first().topic
                    data.append(elist)
            eva_list = data
            print(eva_list)
        elif eva_type == 'teacher':
            #成员互评
            data = []
            eva_list = list(eva_recollect.objects.filter(eva_type='教师评价') \
                            .values("valuer_num") \
                            .annotate(count=Count('id')) \
                            .values("valuer_num", "count", "group_id"))
            for item in eva_list:
                eva_group_list = list(eva_recollect.objects.filter(valuer_num=item['valuer_num'], eva_type='教师评价') \
                                      .values("beeva_num") \
                                      .annotate(count=Count('id')) \
                                      .values("valuer_num", "beeva_num", "count", "group_id"))
                for elist in eva_group_list:
                    elist['valuer_name'] = User.objects.filter(num=elist['valuer_num']).first().name
                    elist['valuer_class'] = '无'
                    elist['eva_type'] = '教师评价'
                    elist['pj_id'] = eva_recollect.objects.filter(eva_type='教师评价', beeva_num=elist[
                        'beeva_num'], valuer_num=elist['valuer_num']).first().pj_id
                    elist['eva_time'] = eva_recollect.objects.filter(eva_type='教师评价', beeva_num=elist[
                        'beeva_num'],valuer_num=elist[
                        'valuer_num']).first().eva_time.strftime('%Y-%m-%d %H:%M:%S %p')
                    elist['beeva_name'] = eva_recollect.objects.filter(eva_type='教师评价', beeva_num=elist[
                        'beeva_num'], valuer_num=elist['valuer_num']).first().beeva_num
                    elist['beeva_num'] = '第' + str(eva_recollect.objects.filter(eva_type='教师评价', beeva_num=elist[
                        'beeva_num'], valuer_num=elist['valuer_num']).first().beeva_num) + '组'
                    elist['act_name'] = UserGroup.objects.filter(group_id=elist['beeva_name']).first().topic
                    data.append(elist)
            eva_list = data
            print(eva_list)
        alldata['eva_list']=eva_list
        return render(request, 'bms_evamanage.html', alldata)
    else:
      return render(request, 'index.html', alldata)
def display_eva(request):#教师主页-评论信息展示
    back_dic = {'resultCode': None, 'msg': None}
    if request.method == 'POST':
        eva_type = request.POST.get('eva_type')
        valuer_num = request.POST.get('valuer_num')
        beeva_num=request.POST.get('beeva_num')
        eva_list=list(eva_recollect.objects.filter(eva_type=eva_type,valuer_num=valuer_num,beeva_num=beeva_num).values())
        if eva_type == '教师评价':
            for item in eva_list:
                item['eva_time']=item['eva_time'].strftime('%Y-%m-%d %H:%M:%S %p')
                item['valuer_name'] = User.objects.filter(num=item['valuer_num']).first().name
                item['eva_title'] = Evaluate.objects.filter(evaluate_id=item['eva_id']).first().evaluate_item
        else :
            for item in eva_list:
                item['eva_time']=item['eva_time'].strftime('%Y-%m-%d %H:%M:%S %p')
                item['valuer_name'] = Student.objects.filter(num=item['valuer_num']).first().name
                item['eva_title'] = Evaluate.objects.filter(evaluate_id=item['eva_id']).first().evaluate_item
        back_dic['resultCode'] = 200
        back_dic['msg'] = '文件数据加载完毕'
        back_dic['eva_list'] = eva_list
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    else:
        back_dic['resultCode'] = -1
        back_dic['msg'] = '出现错误'
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def display_stu_eva(request):#学生管理-评价信息展示
    back_dic = {'resultCode': None, 'msg': None}
    if request.method == 'POST':
        pj_id = request.POST.get('pj_id')
        eva_list=list(eva_recollect.objects.filter(pj_id=pj_id).values())
        for item in eva_list:
            item['eva_time']=item['eva_time'].strftime('%Y-%m-%d %H:%M:%S %p')
            item['valuer_name'] = Student.objects.filter(num=item['valuer_num']).first().name
            item['eva_title'] = Evaluate.objects.filter(evaluate_id=item['eva_id']).first().evaluate_item
        back_dic['resultCode'] = 200
        back_dic['msg'] = '评价数据加载完毕'
        back_dic['eva_list'] = eva_list
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    else:
        back_dic['resultCode'] = -1
        back_dic['msg'] = '出现错误'
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def delete_stu_eva(request):#学生管理-评价信息删除
    back_dic = {'resultCode': None, 'msg': None}
    if request.method == 'POST':
        pj_id = request.POST.get('pj_id')
        try:
            with transaction.atomic():
                eva_recollect.objects.filter(pj_id=pj_id).delete()
                back_dic['resultCode'] = 200
                back_dic['msg'] = '评价数据已删除'
                return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
        except Exception as e:
            print(e)
            back_dic['resultCode'] = -1
            back_dic['msg'] = '删除错误，错误信息:'+ str(e)
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    else:
        back_dic['resultCode'] = -1
        back_dic['msg'] = '出现错误'
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def showmaildetail(request):
    back_dic = {'resultCode': None, 'msg': None}
    feedback_id=request.POST.get('id')
    try:
        with transaction.atomic():
            feedback_list = list(feed_back.objects.filter(feedback_id=feedback_id).values())
            file_count = feedback_list[0]['feedback_file']
            num = feedback_list[0]['num']
            name = list(Student.objects.filter(num=num).values('name'))[0]['name']
            group_role = list(Student.objects.filter(num=num).values('group_role'))[0]['group_role']
            feedback_list[0]['name'] = name
            feedback_list[0]['group_role'] = group_role
            feedback_list[0]['feedback_time'] = feedback_list[0]['feedback_time'].strftime('%Y-%m-%d %H:%M:%S %p')
            fb_id = feedback_list[0]['feedback_id']
            file_list = list(feedbackfile.objects.filter(feedback_id=fb_id).values('id','file_path'))
            import os
            for files in file_list:
                files_path = files['file_path']
                if os.sep in files_path:
                    file_name = files_path.split('\\')[-1]
                else:
                    file_name = files_path.split('/')[-1]
                file_path = os.path.join(settings.BASE_DIR, 'statics', 'feedbackfile', file_name)
                fsize = os.path.getsize(file_path)
                fsize = round(fsize / float(1024))  # 转换文件大小为KB
                files['file_name'] = file_name
                files['file_path'] = file_path
                files['fsize'] = fsize
            feedback_list[0]['file_list'] = file_list
            back_dic['feedback_list'] = feedback_list
            back_dic['resultCode'] = 200
            back_dic['msg'] = '加载完毕'
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e) + "错误"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def feedback_delete(request):
    back_dic = {'resultCode': None, 'msg': None}
    feedback_id = request.POST.get('id')
    try:
        with transaction.atomic():
            feedback_list = list(feed_back.objects.filter(feedback_id=feedback_id).values())
            file_count = feedback_list[0]['feedback_file']
            fb_id = feedback_list[0]['feedback_id']
            file_list = list(feedbackfile.objects.filter(feedback_id=fb_id).values())
            import os
            for files in file_list:
                files_path = files['file_path']
                if os.sep in files_path:
                    file_name = files_path.split('\\')[-1]
                else:
                    file_name = files_path.split('/')[-1]
                if os.path.exists(files_path):
                    os.remove(files_path)
                else:
                    print(' no such file ')  #则返回文件不存在
            #删除数据库记录
            feedback_list = feed_back.objects.filter(feedback_id=feedback_id).delete()
            file_list = feedbackfile.objects.filter(feedback_id=feedback_id).delete()
            back_dic['resultCode'] = 200
            back_dic['msg'] = '已删除'
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e) + "错误"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def calendar_check(request):#进入日历界面
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    if value['power']=='学生':
        value['role']=Student.objects.filter(num=value['num']).first().group_role
    return render(request,'calender.html',context=value)
def stumanage(request):#成员管理模块
    back_dic = {'resultCode': None, 'msg': None, 'rows': None, 'cols': None, 'stu_list': None}
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    num = request.session.get('num')  # 获取教工号
    if num == None:  # 需要登录
        return render(request, 'index.html', context=value)
    if value['power']=='老师':
        mydata = Student.objects.all()
        nonmydata=Student.objects.filter(group_id=0,group_role='尚未指定')
        group_count=search.member_manage()
        data = {}
        nondata=serializers.serialize("json", nonmydata)
        newdata = serializers.serialize("json", mydata)
        data['list'] = json.loads(newdata)
        data['nonlist'] = json.loads(nondata)
        data['group_count'] = group_count
        data['count'] = Student.objects.all().count()
        notice_list = search.get_notice(num)
        data['notice_list'] = notice_list
        return render(request,'stu_mange.html',data)
    elif value['power']=='学生':
        group_role=Student.objects.filter(num=num).first().group_role
        if group_role == '组长':
            group_id=Student.objects.filter(num=num).first().group_id
            mydata = Student.objects.filter(group_id=group_id)
            data = {}
            newdata = serializers.serialize("json", mydata)
            data['list'] = json.loads(newdata)
            data['count'] = Student.objects.all().count()
            notice_list=search.get_notice(num)
            data['notice_list'] = notice_list
            return render(request, 'leader_stumanage .html', data)
        else:
            return render(request, 'index.html', context=value)
def scoremanage(request):#教师主页-成绩管理模块
    back_dic = {'resultCode': None, 'msg': None, 'rows': None, 'cols': None, 'stu_list': None}
    alldata={}
    data=[]
    new_id=[]
    now_topic=[]
    score=[]
    flag=0
    data_id = Student.objects.exclude(group_id=0).values("group_id").order_by("group_id").distinct()
    data_id=list(data_id)
    for people in data_id:
      now_id=people['group_id']#组号
      new_id.append(now_id)
      if now_id!=0:
          new_topic=list(UserGroup.objects.filter(group_id=now_id).values("group_id","topic","group_score"))
          data_id[flag]['topic']=new_topic[0]['topic']
          data_id[flag]['score']=new_topic[0]['group_score']
          flag=flag+1
          #data.append(new_topic)
          #alldata['list'+str(now_id)+'bj']=now_id
    alldata['group_lists'] = data_id
    notice_list=search.get_notice(request.session.get('num'))
    alldata['notice_list'] = notice_list
    return render(request,'score-manage.html',alldata)
def memberscore(request):#教师主页-成绩管理-显示个人成绩
    back_dic = {'resultCode': None, 'msg': None, 'listgroup': None}
    id=request.POST.get('group_id')
    try:
            now_group=Student.objects.filter(group_id=id)#各组成员
            now_data=serializers.serialize("json", now_group)
            back_dic['resultCode']=200
            back_dic['msg'] = '成功'
            back_dic['listgroup'] = json.loads(now_data)
            return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e)+"修改出现错误"
        return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def stumanagechange(request):#教师主页-成员管理模块-修改学生数据
    back_dic = {'resultCode': None, 'msg': None, 'rows': None, 'cols': None, 'stu_list': None}
    print(request.POST.get('stu_po'))
    stu_num=request.POST.get('stu_num')
    stu_name=request.POST.get('stu_name')
    stu_grade = request.POST.get('stu_grade')
    stu_group = request.POST.get('stu_group')
    stu_po = request.POST.get('stu_po')
    try:
        with transaction.atomic():
                Student.objects.filter(num=stu_num).update(
                  num=stu_num,
                  name=stu_name,
                  grade=stu_grade,
                  group_id=stu_group,
                  group_role=stu_po
                )

                back_dic['resultCode'] = 200
                back_dic['msg'] = '已完成数据更新'
                return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e)+"修改出现错误"
        return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def addnewgroupmember(request):#教师主页-成员管理模块-添加成员
    back_dic = {'resultCode': None, 'msg': None, 'rows': None, 'cols': None, 'stu_list': None}
    print(request.POST.get('stu_num'))
    stu_num=request.POST.get('stu_num')
    group_id = request.POST.get('group_id')
    try:
        with transaction.atomic():
                Student.objects.filter(num=stu_num).update(
                  group_id=group_id,
                )
                back_dic['resultCode'] = 200
                back_dic['msg'] = '已完成数据更新'
                return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e)+"修改出现错误"
        return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def onloadgroupinfo(request):#教师主页-成员管理模块-加载成员信息
    back_dic = {'resultCode': None, 'msg': None}
    group_role = ['组长', '记录员', '报告员', '检察员', '组员']
    group_id = request.POST.get('group_id')
    try:
        with transaction.atomic():
                stu_list=Student.objects.filter(group_id=group_id).values("num","name","grade","group_role")
                stu_role=[]
                for stu in stu_list:
                    stu_role.append(stu['group_role'])
                subtraction_list = list(set(group_role).difference(set(stu_role)))#求差集
                stu_list = list(Student.objects.filter(group_id=group_id,group_role='尚未指定').values("num", "name", "grade", "group_role"))
                back_dic['resultCode'] = 200
                back_dic['msg'] = '已完成数据加载'
                back_dic['stu_list'] = stu_list
                back_dic['sub_list'] = subtraction_list
                return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e)+"修改出现错误"
        return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def submitchooserole(request):#教师主页-成员管理模块-担任角色
    back_dic = {'resultCode': None, 'msg': None}
    group_id = request.POST.get('group_id')
    stu_num=request.POST.get('stu_num')
    stu_role = request.POST.get('stu_role')
    try:
        with transaction.atomic():
                Student.objects.filter(num=stu_num).update(
                   group_role=stu_role
                )
                back_dic['resultCode'] = 200
                back_dic['msg'] = '已完成'
                return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e)+"修改出现错误"
        return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def groupdetail(request):#教师主页-显示各组详细信息
    alldata={}
    print(request.POST.get('group_id'))
    #对应各组的基本信息 每项任务的负责人 完成状态
    group_id=request.POST.get('group_id')
    try:
        with transaction.atomic():
                tasklist=list(task.objects.filter(group_id=group_id).values("num","group_role",
                "task_id","task_content","start_time","end_time","is_finish","is_overtime","task_type"))
                for tasks in tasklist:
                    member=list(Student.objects.filter(num=tasks['num']).values("name"))
                    tasks['name']=member[0]['name']
                alldata['resultCode'] = 200
                alldata['msg'] = '已完成数据更新'
                alldata['cols'] =  10
                alldata['data'] = tasklist
                return JsonResponse(alldata)
    except Exception as e:
        print(e)
        alldata['resultCode'] = -1
        alldata['msg'] = str(e)+"修改出现错误"
        return JsonResponse(alldata)
def scoremanagechange(request):#教师主页-成绩管理-修改成绩
    back_dic = {'resultCode': None, 'msg': None, 'rows': None, 'cols': None, 'stu_list': None}
    stu_num=request.POST.get('stu_num')
    stu_score = int(request.POST.get('stu_score'))
    if stu_score<0 or stu_score>100:
        back_dic['resultCode'] = 300
        back_dic['msg'] = "分数错误"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    try:
        with transaction.atomic():
                Student.objects.filter(num=stu_num).update(

                  score=stu_score
                )
                back_dic['resultCode'] = 200
                back_dic['msg'] = '已完成更新'
                return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e)+"修改出现错误"
        return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def login(request):
    back_dic={'user':None,'msg':None,'code':None,'power':None}
    num=request.POST.get('phone')
    pwd=request.POST.get('pwd')
    print(num);
    print(pwd);
    user = User.objects.filter(num=num, pwd=pwd).first()
    print(user)
    if user:
        #设置session
        request.session['name']=user.name
        request.session['num']=user.num
        request.session['power']=user.power
        request.session.set_expiry(60*30*10)#5个小时
        print('登陆者为'+request.session['name']+'权限为'+request.session['power']);
        print(pwd);
        back_dic['user'] = num
        back_dic['msg'] = '成功'
        back_dic['code'] = 200
        back_dic['power'] = user.power
    else:
        back_dic['user'] = num
        back_dic['msg'] = '用户名或密码错误'
        back_dic['code'] = 404
    import json
    return HttpResponse(json.dumps(back_dic))
def stutask(request):
 #根据学生不同的角色呈现不同的任务管理界面
    flag=0
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    alldata={}
    num=request.session.get('num')#获取学生用户的学号
    notice_list=search.get_notice(num)
    search.check_is_overtime()
    if num == None:
       return render(request, 'index.html', context=value)
    stu_info=list(Student.objects.filter(num=num).values())#获得该名同学的组号、角色以及姓名
    search.check_is_overtime()#查看是否超时
    group_id=stu_info[0]['group_id']
    group_role=stu_info[0]['group_role']
    name=stu_info[0]['name']
    alldata['stu_info']=stu_info#登录信息
    if group_role =='组长':
        #找出所有组员的信息
        member_info=list(Student.objects.filter(group_id=group_id).values("num","group_role","name"))
        alldata['member_list']=member_info#组员信息
        task_list=list(task.objects.filter(num=num).values("task_content","start_time","end_time","is_finish","is_overtime","task_type","sub_id"))
        alldata['task_list'] = task_list  #任务信息
        alldata['notice_list'] = notice_list
        return render(request, 'stu_index_leader.html', alldata)
    elif group_role =='记录员':
        #找出所有组员的信息
        member_info=list(Student.objects.filter(group_id=group_id).values("num","group_role","name"))
        alldata['member_list']=member_info#组员信息
        task_list=list(task.objects.filter(num=num).values("task_content","start_time","end_time","is_finish","is_overtime","task_type","sub_id"))
        alldata['task_list'] = task_list  #任务信息
        alldata['notice_list'] = notice_list
        return render(request, 'stu_index_recorder.html', alldata)
    elif group_role =='检察员':
        #找出所有组员的信息
        member_info=list(Student.objects.filter(group_id=group_id).values("num","group_role","name"))
        alldata['member_list']=member_info#组员信息
        task_list=list(task.objects.filter(num=num).values("task_content","start_time","end_time","is_finish","is_overtime","task_type","sub_id"))
        alldata['task_list'] = task_list  #任务信息
        alldata['notice_list']=notice_list
        return render(request, 'stu_index_checker.html', alldata)
    elif group_role =='报告员':
        #找出所有组员的信息
        member_info=list(Student.objects.filter(group_id=group_id).values("num","group_role","name"))
        alldata['member_list']=member_info#组员信息
        task_list=list(task.objects.filter(num=num).values("task_content","start_time","end_time","is_finish","is_overtime","task_type","sub_id"))
        alldata['task_list'] = task_list  #任务信息
        alldata['notice_list'] = notice_list
        return render(request, 'stu_index_reporter.html', alldata)
    elif group_role =='组员':
        #找出所有组员的信息
        member_info=list(Student.objects.filter(group_id=group_id).values("num","group_role","name"))
        alldata['member_list']=member_info#组员信息
        task_list=list(task.objects.filter(num=num).values("task_content","start_time","end_time","is_finish","is_overtime","task_type","sub_id"))
        alldata['task_list'] = task_list  #任务信息
        alldata['notice_list'] = notice_list
        return render(request, 'stu_index_member.html', alldata)
    return render(request, 'index.html', context=value)
def stu_eva(request):#学生自评
    alldata = {}
    value = {'name': request.session.get('name'),
             'num': request.session.get('num')
             }
    num = request.session.get('num')  # 获取学生用户的学号
    value['power']=list(Student.objects.filter(num=num).values())[0]['group_role']
    if num == None:
        return render(request, 'index.html')
    group_id=list(Student.objects.filter(num=num).values())[0]['group_id']
    group_info=list(UserGroup.objects.filter(group_id=group_id).values())
    notice_list = search.get_notice(num)
    time=datetime.datetime.now()
    datetime_str=time.strftime('%Y-%m-%d %H:%M:%S %p')
    eva_list=list(Evaluate.objects.filter(evaluate_type='个人评价').values())
    is_submit=search.check_is_submit(num,group_id,'个人评价',eva_list)
    print(is_submit)
    alldata['eva_list']=eva_list
    alldata['notice_list'] = notice_list
    alldata['group_info'] = group_info
    alldata['time'] = datetime_str
    alldata['time1'] = time
    alldata['is_submit'] = is_submit
    alldata['user'] = value
    alldata['stu_info'] = list(Student.objects.filter(num=num).values())
    return render(request, 'stu_learn_eva.html',alldata)
def group_eva(request):#小组评价
    alldata = {}
    value = {'name': request.session.get('name'),
             'num': request.session.get('num')
             }
    num = request.session.get('num')  # 获取学生用户的学号
    value['power'] = list(Student.objects.filter(num=num).values())[0]['group_role']
    if num == None:
        return render(request, 'index.html')
    group_id=list(Student.objects.filter(num=num).values())[0]['group_id']
    group_info=list(UserGroup.objects.filter(group_id=group_id).values())
    notice_list = search.get_notice(num)
    time=datetime.datetime.now()
    datetime_str=time.strftime('%Y-%m-%d %H:%M:%S %p')
    eva_list=list(Evaluate.objects.filter(evaluate_type='组内评价').values())
    is_submit=search.check_is_submit(num,group_id,'组内评价',eva_list)
    print(is_submit)
    alldata['eva_list']=eva_list
    alldata['notice_list'] = notice_list
    alldata['group_info'] = group_info
    alldata['time'] = datetime_str
    alldata['time1'] = time
    alldata['is_submit'] = is_submit
    alldata['user'] = value
    alldata['stu_info'] = list(Student.objects.filter(num=num).values())
    return render(request, 'stu_learn_eva.html',alldata)
def diff_eva(request):#组间评价
    alldata = {}
    value = {'name': request.session.get('name'),
             'num': request.session.get('num')
             }
    num = request.session.get('num')  # 获取学生用户的学号
    value['power'] = list(Student.objects.filter(num=num).values())[0]['group_role']
    if num == None:
        return render(request, 'index.html')
    group_id=list(Student.objects.filter(num=num).values())[0]['group_id']
    group_info=list(UserGroup.objects.filter(group_id=group_id).values())
    diffgroup_info = list(UserGroup.objects.exclude(group_id=group_id).values())
    search.is_evagroup(diffgroup_info,num,group_id,'组间互评')
    notice_list = search.get_notice(num)
    time=datetime.datetime.now()
    datetime_str=time.strftime('%Y-%m-%d %H:%M:%S %p')
    eva_list=list(Evaluate.objects.filter(evaluate_type='组间互评').values())
    alldata['eva_list']=eva_list
    alldata['notice_list'] = notice_list
    alldata['group_info'] = group_info
    alldata['diffgroup_info'] = diffgroup_info
    alldata['time'] = datetime_str
    alldata['time1'] = time
    alldata['user'] = value
    alldata['is_submit'] = False
    alldata['stu_info'] = list(Student.objects.filter(num=num).values())
    return render(request, 'stu_learn_eva.html',alldata)
def mem_eva(request):#成员互评
    alldata = {}
    value = {'name': request.session.get('name'),
             'num': request.session.get('num')
             }
    num = request.session.get('num')  # 获取学生用户的学号
    value['power'] = list(Student.objects.filter(num=num).values())[0]['group_role']
    if num == None:
        return render(request, 'index.html')
    group_id=list(Student.objects.filter(num=num).values())[0]['group_id']
    group_info=list(UserGroup.objects.filter(group_id=group_id).values())
    #同组的学生
    mem_list=list(Student.objects.filter(group_id=group_id).exclude(num=num).values())
    search.is_evamember(mem_list, num, group_id, '成员互评')
    notice_list = search.get_notice(num)
    time=datetime.datetime.now()
    datetime_str=time.strftime('%Y-%m-%d %H:%M:%S %p')
    eva_list=list(Evaluate.objects.filter(evaluate_type='成员互评').values())
    alldata['eva_list']=eva_list
    alldata['notice_list'] = notice_list
    alldata['group_info'] = group_info
    alldata['mem_list'] = mem_list
    alldata['time'] = datetime_str
    alldata['time1'] = time
    alldata['user'] = value
    alldata['is_submit'] = False
    alldata['stu_info'] = list(Student.objects.filter(num=num).values())
    return render(request, 'stu_learn_eva.html',alldata)
def teacher_eva(request):#教师评价
    alldata = {}
    num = request.session.get('num')  # 获取教师用户的教工号
    if num == None:
        return render(request, 'index.html')
    teacher_info=list(User.objects.filter(num=num).values())
    diffgroup_info = list(UserGroup.objects.all().values())
    search.is_evagroup(diffgroup_info, num, '0', '教师评价')
    notice_list = search.get_notice(num)
    time = datetime.datetime.now()
    datetime_str = time.strftime('%Y-%m-%d %H:%M:%S %p')
    eva_list = list(Evaluate.objects.filter(evaluate_type='教师评价').values())
    alldata['eva_list'] = eva_list
    alldata['notice_list'] = notice_list
    alldata['teacher_info'] = teacher_info
    alldata['diffgroup_info'] = diffgroup_info
    alldata['time'] = datetime_str
    alldata['time1'] = time
    alldata['is_submit'] = False
    return render(request, 'teacher_learn_eva.html',alldata)
def addstueva(request):#提交学生自评
    back_dic = {'resultCode': None, 'msg': None}
    submit_data=json.loads(request.POST.get('submit_data'))
    maxid = eva_recollect.objects.all().aggregate(Max('pj_id'))
    print(maxid)
    if maxid['pj_id__max'] == None:
        maxid['pj_id__max'] = 1
    else:
        maxid['pj_id__max'] = maxid['pj_id__max'] + 1
    try:
            for item in submit_data:
                neweva=eva_recollect(
                    eva_id=item['eva_id'],
                    eva_time=item['eva_time'],
                    act_name=item['act_name'],
                    beeva_num=item['beeva_num'],
                    eva_content=item['eva_content'],
                    eva_type=item['eva_type'],
                    form_type=item['form_type'],
                    group_id=item['group_id'],
                    valuer_num=item['valuer_num'],
                    pj_id=maxid['pj_id__max']
                )
                neweva.save()
            back_dic['resultCode'] = 200
            back_dic['msg'] = '成功'
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e)+"出现错误"
        return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def modifystueva(request):#提交评价修改
    back_dic = {'resultCode': None, 'msg': None}
    modify_data=json.loads(request.POST.get('modify_data'))
    try:
            for item in modify_data:
                neweva=eva_recollect.objects.filter(pj_id=item['pj_id'],eva_id=item['eva_id'])\
                    .update(
                    eva_content=item['eva_content'],
                    eva_time=datetime.datetime.now()

                )
            back_dic['resultCode'] = 200
            back_dic['msg'] = '修改成功'
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e)+"出现错误"
        return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def sendfeedback(request):
    #发送反馈邮件
    alldata={}
    num=request.session.get('num')
    notice_list = search.get_notice(num)
    alldata['notice_list'] = notice_list
    return render(request, 'stu_sendemail.html',alldata)
def group_chat(request):
    #进入讨论区
    value = {
             'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    alldata={}
    num=request.session.get('num')
    stu_info = list(Student.objects.filter(num=num).values())  # 获得该名同学的信息
    group_id = stu_info[0]['group_id']
    member_info = list(Student.objects.filter(group_id=group_id).values("num", "group_role", "name"))
    notice_list = search.get_notice(num)
    alldata['notice_list'] = notice_list
    alldata['member_list'] = member_info  # 组员信息
    alldata['stu_info'] = stu_info  # 组员信息
    return render(request, 'group_chat.html',alldata)
def replyfeedback(request):
    #学生受到反馈回复
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    alldata={}
    num=request.session.get('num')
    notice_list = search.get_notice(num)
    alldata['notice_list'] = notice_list
    num = request.session.get('num')  # 获取教工号
    if num == None:  # 需要登录
        return render(request, 'index.html', context=value)
    import os
    feedback_list = list(feed_back.objects.filter(feedback_type=4).values())
    for item in feedback_list:
        file_count = item['feedback_file']
        num = item['num']
        name = "老师回复"+list(Student.objects.filter(num=num).values('name'))[0]['name']
        group_role = list(Student.objects.filter(num=num).values('group_role'))[0]['group_role']
        item['name'] = name
        item['group_role'] = group_role
        fb_id = item['feedback_id']
        file_list = list(feedbackfile.objects.filter(feedback_id=fb_id).values('file_path'))
        for files in file_list:
            files_path = files['file_path']
            if os.sep in files_path:
                file_name = files_path.split('\\')[-1]
            else:
                file_name = files_path.split('/')[-1]
            file_path = os.path.join(settings.BASE_DIR, 'statics', 'feedbackfile', file_name)
            fsize = os.path.getsize(file_path)
            fsize = round(fsize / float(1024))  # 转换文件大小为KB
            files['file_name'] = file_name
            files['file_path'] = file_path
            files['fsize'] = fsize
        item['file_list'] = file_list
    alldata['feedback_list'] = feedback_list
    return render(request, 'stu_replyfeedback.html',alldata)
def addfeedbackmsg(request):
    back_dic = {'resultCode': None, 'msg': None}
    import datetime
    if request.method == 'POST':
        feedback_title = request.POST.get('feedback_title')
        feedback_content = request.POST.get('feedback_content')
        feedback_type = request.POST.get('feedback_type')
        num=request.session.get('num')
        group_id=list(Student.objects.filter(num=num).values('group_id'))[0]['group_id']
        feedback_time = datetime.datetime.now()  # 反馈时间时间
        file_flag=request.POST.get('file_flag')
        if file_flag == '有':
            file_list=request.FILES.getlist('feedback_file')
            file_count=request.POST.get('file_count')
                    #写入服务器中
            try:
                with transaction.atomic():
                    maxid = feed_back.objects.all().aggregate(Max('feedback_id'))
                    if maxid['feedback_id__max'] == None:
                        id = 1
                    else:
                        id = int(maxid['feedback_id__max']) + 1
                    newfeedback = feed_back(
                    group_id=group_id,
                    feedback_time=feedback_time,
                    feedback_type=feedback_type,
                    feedback_content=feedback_content,
                    feedback_title=feedback_title,
                    num=num,
                    feedback_file=file_count,
                    feedback_id=id
                    )
                    newfeedback.save()
                    for sfile in file_list:
                        f_name = sfile.name
                        import os
                        file_path = os.path.join(settings.BASE_DIR, 'statics', 'feedbackfile', f_name)
                        newfbfile=feedbackfile(
                            feedback_id=id,
                            file_path=file_path
                        )
                        newfbfile.save()
                        with open(file_path, 'wb')as f:
                            for chunk in sfile.chunks():
                                f.write(chunk)
                    back_dic['resultCode'] = 200
                    back_dic['msg'] = '发送成功'
                    return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
            except Exception as e:
                   print(e)
                   back_dic['resultCode'] = -1
                   back_dic['msg'] = str(e) + "上传有误"
                   return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
        elif file_flag == '无':
                file_info = request.POST.get('file_count')
                maxid = feed_back.objects.all().aggregate(Max('feedback_id'))
                if maxid['feedback_id__max']== None:
                    id=1
                else:
                    id = int(maxid['feedback_id__max']) + 1
                newfeedback = feed_back(
                    group_id=group_id,
                    feedback_time=feedback_time,
                    feedback_type=feedback_type,
                    feedback_content=feedback_content,
                    feedback_title=feedback_title,
                    num=num,
                    feedback_file=file_info,
                    feedback_id = id
                )
                newfeedback.save()
                back_dic['resultCode'] = 200
                back_dic['msg'] = '发送成功'
                return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    else:
        back_dic['resultCode'] = -1
        back_dic['msg'] = '出现错误'
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def addreplyfeedbackmsg(request):
    back_dic = {'resultCode': None, 'msg': None}
    import datetime
    if request.method == 'POST':
        feedback_title = request.POST.get('feedback_title')
        feedback_content = request.POST.get('feedback_content')
        feedback_type = request.POST.get('feedback_type')
        num=request.POST.get('num')
        group_id=list(Student.objects.filter(num=num).values('group_id'))[0]['group_id']
        feedback_time = datetime.datetime.now()  # 反馈时间时间
        file_flag=request.POST.get('file_flag')
        if file_flag == '有':
            file_list=request.FILES.getlist('feedback_file')
            file_count=request.POST.get('file_count')
                    #写入服务器中
            try:
                with transaction.atomic():
                    id = str(feed_back.objects.all().count() + 1)
                    newfeedback = feed_back(
                    group_id=group_id,
                    feedback_time=feedback_time,
                    feedback_type=feedback_type,
                    feedback_content=feedback_content,
                    feedback_title=feedback_title,
                    num=num,
                    feedback_file=file_count,
                    feedback_id=id
                    )
                    newfeedback.save()
                    for sfile in file_list:
                        f_name = sfile.name
                        import os
                        file_path = os.path.join(settings.BASE_DIR, 'statics', 'feedbackfile', f_name)
                        newfbfile=feedbackfile(
                            feedback_id=id,
                            file_path=file_path
                        )
                        newfbfile.save()
                        with open(file_path, 'wb')as f:
                            for chunk in sfile.chunks():
                                f.write(chunk)
                    back_dic['resultCode'] = 200
                    back_dic['msg'] = '发送成功'
                    return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
            except Exception as e:
                   print(e)
                   back_dic['resultCode'] = -1
                   back_dic['msg'] = str(e) + "上传有误"
                   return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
        elif file_flag == '无':
                file_info = request.POST.get('file_count')
                id = str(feed_back.objects.all().count() + 1)
                newfeedback = feed_back(
                    group_id=group_id,
                    feedback_time=feedback_time,
                    feedback_type=feedback_type,
                    feedback_content=feedback_content,
                    feedback_title=feedback_title,
                    num=num,
                    feedback_file=file_info,
                    feedback_id = id
                )
                newfeedback.save()
                back_dic['resultCode'] = 200
                back_dic['msg'] = '发送成功'
                return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    else:
        back_dic['resultCode'] = -1
        back_dic['msg'] = '出现错误'
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def grouptalkfile(request):
    back_dic = {'resultCode': None, 'msg': None}
    data=[]
    import datetime
    if request.method == 'POST':
            group_id=request.POST.get('group_id')
            num=request.POST.get('num')
            name = request.POST.get('name')
            type = request.POST.get('type')
            file_list=request.FILES.getlist('groupmsg_file')
            #写入服务器中
            try:
                with transaction.atomic():
                    #上传文件
                    for sfile in file_list:
                        f_name = sfile.name
                        import os
                        file_path = os.path.join(settings.BASE_DIR, 'statics', 'grouptalkfile',group_id)
                        if not os.path.exists(file_path):
                            os.mkdir(file_path)
                        file_path= os.path.join(settings.BASE_DIR, 'statics', 'grouptalkfile',group_id,f_name)
                        with open(file_path, 'wb')as f:
                            for chunk in sfile.chunks():
                                f.write(chunk)
                        fsize = os.path.getsize(file_path)
                        fsize = round(fsize / float(1024))  # 转换文件大小为KB
                        file_type = str(str(f_name).split('.')[1])  # 获取文件的拓展名
                        file={'file_name':f_name,'file_path':file_path,'fsize': fsize,'file_type':file_type}
                        data.append(file)
                    back_dic['file_info']=data
                    back_dic['resultCode'] = 200
                    back_dic['msg'] = '发送成功'
                    return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
            except Exception as e:
                   print(e)
                   back_dic['resultCode'] = -1
                   back_dic['msg'] = str(e) + "上传有误"
                   return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    else:
        back_dic['resultCode'] = -1
        back_dic['msg'] = '出现错误'
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def dlgroupfile(request):
    back_dic = {'resultCode': None, 'msg': None}
    if request.method == 'GET':
        file_id = request.GET.get('id')
        file_id=int(file_id)
        file_name = request.GET.get('file_name')
        file_path=GroupChat.objects.filter(id=file_id).values('send_content').first()['send_content']
        import os
        if not os.path.isfile(file_path):
            back_dic['resultCode'] = -1
            back_dic['msg'] = "找不到该文件"
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
        try:
            file = open(file_path, 'rb')
            import mimetypes
            content_type = mimetypes.guess_type(file_name)[0]  # 获取需要的content_type信息
            response = FileResponse(file)
            response['Content-Type'] = content_type
            filename = 'attachment;filename=' + file_name
            response['Content-Disposition'] = filename.encode('utf-8', 'ISO-8859-1')
            return response
        except:
            back_dic['resultCode'] = -1
            back_dic['msg'] = "找不到该文件"
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    else:
        back_dic['resultCode'] = -1
        back_dic['msg'] = '出现错误'
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def check_file(request):
 #根据学生不同的角色呈现不同的任务管理界面
    flag=0
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    alldata={}
    num=request.session.get('num')#获取学生用户的学号
    if num == None:
       return render(request, 'index.html', context=value)
    stu_info=list(Student.objects.filter(num=num).values("group_id","group_role","name"))#获得该名同学的组号、角色以及姓名
    group_id=stu_info[0]['group_id']
    group_role=stu_info[0]['group_role']
    name=stu_info[0]['name']
    if group_role =='组长':
        #找出所有待审核的文件
        doc_info=list(doc.objects.filter(group_id=group_id,is_check=False).values())
        alldata['doc_info']=doc_info
        return render(request, 'stu_check_file.html', alldata)
    elif group_role =='检察员':
        doc_info = list(doc.objects.filter(group_id=group_id, is_check=False).values())
        for item in doc_info:
            stu_num=item['num']
            stu_name=list(Student.objects.filter(num=stu_num).values('name'))[0]['name']
            item['publisher']=stu_name+'_'+stu_num
            if item['submit_type'] == '2':
                import os
                if os.sep in item['file_content']:
                    item['file_content'] = item['file_content'].split('\\')[-1]
                else:
                    item['file_content'] = item['file_content'].split('/')[-1]
            item['filepub_time']=item['filepub_time'].strftime('%Y-%m-%d %H:%M:%S %p')
        alldata['doc_info'] = doc_info
        return render(request, 'stu_check_file.html', alldata)
    return render(request, 'index.html', context=value)
def check_file_content(request):
    back_dic = {'resultCode': None, 'msg': None}
    id=request.POST.get('id')
    file=list(doc.objects.filter(id=id).values("file_content"))
    file_content=file[0]['file_content']
    back_dic['resultCode'] = 200
    back_dic['msg'] = '成功加载文件内容'
    back_dic['file_content'] = file_content
    return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def leader_taskmanage(request):
 #组长任务管理界面
    flag=0
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    alldata={}
    num=request.session.get('num')#获取用户的学号
    if num == None: #需要登录
       return render(request, 'index.html', context=value)
    search.check_is_overtime()
    num = request.session.get('num')
    notice_list = search.get_notice(num)
    alldata['notice_list'] = notice_list
    stu_info=list(Student.objects.filter(num=num).values("num","group_id","group_role","name"))#获得该名同学的组号、角色以及姓名
    group_id=stu_info[0]['group_id']
    group_role=stu_info[0]['group_role']
    name=stu_info[0]['name']
    if group_role =='组长':
        # 找出所有组员的信息
        member_info = list(Student.objects.filter(group_id=group_id).values("num", "group_role", "name"))
        alldata['member_list'] = member_info  # 组员信息
        #组员任务信息
        task_lists = list(task.objects.filter(group_id=group_id).values("num","task_id","task_content", "start_time", "end_time", "is_finish", "is_overtime",
                                                "task_type", "sub_id"))
        alldata['task_lists'] = task_lists  # 任务信息
        #任务编号
        task_ids=list(task.objects.filter(group_id=group_id).values("task_id"))
        alldata['task_ids']= task_ids
        for item in task_lists:
            member_num=item['num']
            start_time=item['start_time']
            end_time = item['end_time']

            member_name =list(Student.objects.filter(num=member_num).values("name"))[0]["name"]
            item['name'] = member_name
            item['start_time']=start_time.strftime( '%Y-%m-%d')
            item['end_time'] = end_time.strftime( '%Y-%m-%d')
        maxid = task.objects.all().aggregate(Max('task_id'))
        print(maxid)
        maxid['task_id__max'] = maxid['task_id__max'] + 1
        print(maxid)
        alldata['maxid']=maxid['task_id__max']
        print('id最大值' + str(maxid['task_id__max']))
        #print(alldata)
        return render(request, 'leader_taskmanage.html', alldata)
    return render(request, 'index.html', context=value)
def member_taskmanage(request):
 #除组长外-任务管理界面
    flag=0
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    alldata={}
    num=request.session.get('num')#获取用户的学号
    if num == None: #需要登录
       return render(request, 'index.html', context=value)
    stu_info=list(Student.objects.filter(num=num).values("num","group_id","group_role","name"))#获得该名同学的组号、角色以及姓名
    group_id=stu_info[0]['group_id']
    group_role=stu_info[0]['group_role']
    name=stu_info[0]['name']
    if group_role :
        task_lists = list(task.objects.filter(num=num).values("num","task_id","task_content", "start_time", "end_time", "is_finish", "is_overtime",
                                                "task_type", "sub_id"))
        alldata['task_lists'] = task_lists  # 任务信息
        for item in task_lists:
            task_id=item['task_id'];
            start_time=item['start_time']
            end_time = item['end_time']
            item['start_time']=start_time.strftime( '%Y-%m-%d')
            item['end_time'] = end_time.strftime( '%Y-%m-%d')
            #提交完待审核
            check=list(doc.objects.filter(task_id=task_id).values("task_id","is_check"))
            if check:
                item['status']="待审核"
                item['count'] = len(check)
            else :
                item['status'] = "未提交"
                item['count'] = 0
        return render(request, 'member_taskmanage.html', alldata)
    return render(request, 'index.html', context=value)
def submitdoc(request):#组员-提交任务
    back_dic = {'resultCode': None, 'msg': None, 'rows': None, 'cols': None, 'stu_list': None}
    task_id = request.POST.get('task_id')
    filepub_time = request.POST.get('filepub_time')
    submit_type= request.POST.get('submit_type')
    is_check = request.POST.get('is_check')
    task_remark = request.POST.get('task_remark')
    if submit_type == '1':
        #文本
        file_content=request.POST.get('file_content')
    else:
        #文件
        file_content = request.FILES.get('file_content', None)
    stu_info=list(task.objects.filter(task_id=task_id).values("num","group_id"))
    num=stu_info[0]['num']
    group_id=stu_info[0]['group_id']
    try:
        with transaction.atomic():
            if submit_type == '1':
                # 文本
                newtaskfile = doc(
                    group_id=group_id,
                    num=num,
                    task_id=task_id,
                    filepub_time=filepub_time,
                    file_content=file_content,
                    task_remark=task_remark,
                    is_check=False,
                    submit_type=submit_type,
                    file_type='无'
                )
                newtaskfile.save()
            else:
                # 文件
                file_name = file_content.name  # 获取文件名字
                file_type = str(str(file_name).split('.')[1])  # 获取文件的拓展名
                # 拼接绝对路径 上传文件至目录
                import os
                file_path = os.path.join(settings.BASE_DIR, 'statics', 'task_info', file_name)
                with open(file_path, 'wb')as f:
                    for chunk in file_content.chunks():
                        f.write(chunk)
                newtaskfile = doc(
                    group_id=group_id,
                    num=num,
                    task_id=task_id,
                    filepub_time=filepub_time,
                    file_content=file_path,
                    task_remark=task_remark,
                    is_check=False,
                    submit_type=submit_type,
                    file_type=file_type
                )
                newtaskfile.save()
            back_dic['resultCode'] = 200
            back_dic['msg'] = '已完成数据更新'
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e) + "修改出现错误"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def showsubmit(request):#组员-展示已提交文件
    back_dic = {'resultCode': None, 'msg': None}
    task_id = request.POST.get('task_id')
    try:
        with transaction.atomic():
            check_list=list(doc.objects.filter(task_id=task_id).values())
            for item in check_list:
                filepub_time = item['filepub_time']
                item['filepub_time'] = filepub_time.strftime('%Y-%m-%d %H:%M:%S')
            back_dic['resultCode'] = 200
            back_dic['msg'] = '已完成数据更新'
            back_dic['check_list'] = check_list
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e) + "修改出现错误"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def readfile(request):#组员-预览文件下载
    back_dic = {'resultCode': None, 'msg': None}
    file_id=request.GET.get('file_id')
    print(file_id)
    files=list(doc.objects.filter(id=file_id).values())
    print(files)
    num=files[0]['num']
    task_id=files[0]['task_id']
    stu=list(Student.objects.filter(num=num).values("num","name"))
    name=stu[0]['name']
    file_path = files[0]['file_content']
    file_type = files[0]['file_type']  # 获取文件类型
    import os
    if os.sep in file_path:
        file_name = file_path.split('\\')[-1]
    else:
        file_name = file_path.split('/')[-1]
    file_path=os.path.join(settings.BASE_DIR, 'statics', 'task_info', file_name)
    print(file_name)
    print(file_path)
    file=open(file_path,'rb')
    if file_type=='docx':
        import os
        if not os.path.isfile(file_path):
            back_dic['resultCode'] = -1
            back_dic['msg'] = "找不到该文件"
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
        try:
            response = FileResponse(file)
            response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
            filename='attachment;filename='+name+'_'+'任务'+task_id+'_'+file_name
            response['Content-Disposition'] = filename.encode('utf-8','ISO-8859-1')
            return response
        except:
            back_dic['resultCode'] = -1
            back_dic['msg'] = "找不到该文件"
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def export_talk(request):#导出聊天记录
    import xlwt
    back_dic = {'resultCode': None, 'msg': None}
    group_id=request.GET.get('group_id')
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
    title="第"+group_id+"组聊天记录"
    group_chats=list(GroupChat.objects.filter(group_id=group_id).values())
    print(len(group_chats))
    if len(group_chats) == 0:
        back_dic['resultCode'] = -1
        back_dic['msg'] = "no group chats please try again"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    else:
        mark=2
        wb = xlwt.Workbook(encoding='utf-8', style_compression=0)
        ws = wb.add_sheet('第' + group_id + '组')
        ws.write(0, 0, title, style0)
        ws.write(1, 0, "id", style0)
        ws.write(1, 1, "组号", style0)
        ws.write(1, 2, "学号", style0)
        ws.write(1, 3, "姓名", style0)
        ws.write(1, 4, "聊天内容", style0)
        ws.write(1, 5, "发送时间", style0)
        for item in group_chats:
            send_type=item['send_type']
            if int(send_type) == 2:
                file_path=item['send_content']
                import os
                if os.sep in file_path:
                    file_name = file_path.split('\\')[-1]
                else:
                    file_name = file_path.split('/')[-1]
                item['send_content']=file_name
                send_num=item['send_num']
                item['send_name']=User.objects.filter(num=send_num).first().name
                item['send_time']=str(item['send_time'])
                ws.write(mark, 0, item['id'])
                ws.write(mark, 1, item['group_id'])
                ws.write(mark, 2, item['send_num'])
                ws.write(mark, 3, item['send_name'])
                ws.write(mark, 4, item['send_content'])
                ws.write(mark, 5, item['send_time'])
                mark=mark+1
            else:
                send_num = item['send_num']
                item['send_name'] = User.objects.filter(num=send_num).first().name
                item['send_time'] = str(item['send_time'])
                ws.write(mark, 0, item['id'])
                ws.write(mark, 1, item['group_id'])
                ws.write(mark, 2, item['send_num'])
                ws.write(mark, 3, item['send_name'])
                ws.write(mark, 4, item['send_content'])
                ws.write(mark, 5, item['send_time'])
                mark = mark + 1
        # 拼接绝对路径 上传文件至目录
        file_name=title+'.xls'
        import os
        file_path = os.path.join(settings.BASE_DIR, 'statics', 'group_talk', file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        wb.save(file_path)
        file = open(file_path, 'rb')
        if not os.path.isfile(file_path):
                back_dic['resultCode'] = -1
                back_dic['msg'] = "找不到该文件"
                return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
        try:
                response = FileResponse(file)
                response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                filename='attachment;filename='+file_name
                response['Content-Disposition'] = filename.encode('utf-8','ISO-8859-1')
                return response
        except:
                back_dic['resultCode'] = -1
                back_dic['msg'] = "找不到该文件"
                return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def get_file(request):#导出小组成绩
    import xlwt
    back_dic = {'resultCode': None, 'msg': None}
    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
    groups=list(UserGroup.objects.all().values())
    if len(groups) == 0:
        back_dic['resultCode'] = -1
        back_dic['msg'] = "no groups please try again"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    else:
        mark = 0
        wb = xlwt.Workbook(encoding='utf-8', style_compression=0)
        ws = wb.add_sheet('小组成绩表')
        for item in groups :
            group_id=item['group_id']
            group_topic=item['topic']
            score = item['group_score']
            title="第"+str(group_id)+"组:"+str(group_topic)+"  小组成绩:"+str(score)
            ws.write(mark, 0, title, style0)
            mark=mark+1
            ws.write(mark, 0, "学号", style0)
            ws.write(mark, 1, "姓名", style0)
            ws.write(mark, 2, "班级", style0)
            ws.write(mark, 3, "角色", style0)
            ws.write(mark, 4, "分数", style0)
            mark = mark + 1
            stu_list=list(Student.objects.filter(group_id=group_id).values())
            for stu in stu_list:
                ws.write(mark, 0, stu['num'])
                ws.write(mark, 1, stu['name'])
                ws.write(mark, 2, stu['grade'])
                ws.write(mark, 3, stu['group_role'])
                ws.write(mark, 4, stu['score'])
                mark=mark+1
        # 拼接绝对路径 上传文件至目录
        file_name='小组成绩'+'.xls'
        import os
        file_path = os.path.join(settings.BASE_DIR, 'statics', 'group_score')
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_path = os.path.join(settings.BASE_DIR, 'statics', 'group_score', file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        wb.save(file_path)
        file = open(file_path, 'rb')
        if not os.path.isfile(file_path):
                back_dic['resultCode'] = -1
                back_dic['msg'] = "找不到该文件"
                return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
        try:
                response = FileResponse(file)
                response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                filename='attachment;filename='+file_name
                response['Content-Disposition'] = filename.encode('utf-8','ISO-8859-1')
                return response
        except:
                back_dic['resultCode'] = -1
                back_dic['msg'] = "找不到该文件"
                return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def readfiles(request):#教师-邮箱-文件下载
    back_dic = {'resultCode': None, 'msg': None}
    file_id=request.GET.get('file_id')
    files=list(feedbackfile.objects.filter(id=file_id).values())
    file_path = files[0]['file_path']
    import os
    if os.sep in file_path:
        file_name = file_path.split('\\')[-1]
    else:
        file_name = file_path.split('/')[-1]
    file_path=os.path.join(settings.BASE_DIR, 'statics', 'feedbackfile', file_name)
    file=open(file_path,'rb')
    import os
    if not os.path.isfile(file_path):
        back_dic['resultCode'] = -1
        back_dic['msg'] = "找不到该文件"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    try:
        response = FileResponse(file)
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        filename='attachment;filename='+file_name
        response['Content-Disposition'] = filename.encode('utf-8','ISO-8859-1')
        return response
    except:
        back_dic['resultCode'] = -1
        back_dic['msg'] = "找不到该文件"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def bms_readfile(request):#bms
    back_dic = {'resultCode': None, 'msg': None}
    file_path=request.GET.get('file_path')
    import os
    if os.sep in file_path:
        file_name = file_path.split('\\')[-1]
    else:
        file_name = file_path.split('/')[-1]
    file_path = os.path.join(settings.BASE_DIR, 'statics', 'feedbackfile', file_name)
    file = open(file_path, 'rb')
    import os
    if not os.path.isfile(file_path):
        back_dic['resultCode'] = -1
        back_dic['msg'] = "找不到该文件"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    try:
        response = FileResponse(file)
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        filename = 'attachment;filename=' + file_name
        response['Content-Disposition'] = filename.encode('utf-8', 'ISO-8859-1')
        return response
    except:
        back_dic['resultCode'] = -1
        back_dic['msg'] = "找不到该文件"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def reviewpass(request):#组员-预览已提交文件
    back_dic = {'resultCode': None, 'msg': None}
    file_id=request.POST.get('id')
    files=list(doc.objects.filter(id=file_id).values())
    submit_time=files[0]['filepub_time']
    str_submit_time=submit_time.strftime('%Y-%m-%d %H:%M:%S')
    task_id=files[0]['task_id']
    task_info=list(task.objects.filter(task_id=task_id).values())
    end_time = task_info[0]['end_time']
    dt2 = datetime.datetime.strptime(str(end_time), '%Y-%m-%d')#deadline
    dt1=datetime.datetime.strptime(str_submit_time,'%Y-%m-%d %H:%M:%S')#上交时间
    days = (dt2 - dt1).days#延迟天数
    if (dt2-dt1).days < 0:
        #超时提交
        task.objects.filter(task_id=task_id).update(
            is_finish=True,
            is_overtime=True,
            overtime_days=days,
        )
        doc.objects.filter(id=file_id).update(
            is_check=True
        )
    else :
        task.objects.filter(task_id=task_id).update(
            is_finish=True,
            is_overtime=False,
        )
        doc.objects.filter(id=file_id).update(
            is_check=True
        )
    back_dic['resultCode'] = 200
    back_dic['days'] = days
    back_dic['msg'] = "任务状态更新完成"
    return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def leader_taskchange(request):#组长-任务修改
    back_dic = {'resultCode': None, 'msg': None, 'rows': None, 'cols': None, 'stu_list': None}
    stu_num = request.POST.get('stu_num')
    task_id = request.POST.get('task_id')
    task_type= request.POST.get('task_type')
    task_content = request.POST.get('task_content')
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    sub_id = request.POST.get('sub_id')
    try:
        with transaction.atomic():
            task.objects.filter(num=stu_num,task_id=task_id).update(
                task_type=task_type,
                task_content=task_content,
                start_time =start_time ,
                end_time=end_time,
                sub_id=sub_id
            )

            back_dic['resultCode'] = 200
            back_dic['msg'] = '已完成数据更新'
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e) + "修改出现错误"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def bms_addtask(request):#后台-任务添加
    back_dic = {'resultCode': None, 'msg': None, 'rows': None, 'cols': None, 'stu_list': None}
    stu_num = request.POST.get('data[Name]')
    group_role = request.POST.get('data[role]')
    task_id = request.POST.get('data[task_id]')
    task_type= request.POST.get('data[type]')
    task_content = request.POST.get('data[L_content]')
    start_time = request.POST.get('data[start_time]')
    end_time = request.POST.get('data[end_time]')
    sub_id = request.POST.get('data[sub_id]')
    stu_info = list(Student.objects.filter(num=stu_num).values("num", "group_id", "group_role", "name"))  # 获得该名同学的组号、角色以及姓名
    group_id = stu_info[0]['group_id']
    try:
        with transaction.atomic():
            newtask = task(group_id=group_id,
                            num=stu_num, group_role=group_role, task_id=task_id, task_content=task_content,
                            start_time=start_time,end_time=end_time,is_finish=0,is_overtime=0,task_type=task_type,
                            sub_id=sub_id
                            )
            newtask.save()
            back_dic['resultCode'] = 200
            back_dic['msg'] = '已完成任务添加'
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e) + "修改出现错误"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def bms_edittask(request):#后台-任务添加
    back_dic = {'resultCode': None, 'msg': None, 'rows': None, 'cols': None, 'stu_list': None}
    id = request.POST.get('data[id]')
    group_id = request.POST.get('data[groupid]')
    stu_num = request.POST.get('data[Name]')
    group_role = request.POST.get('data[role]')
    task_id = request.POST.get('data[task_id]')
    task_type= request.POST.get('data[type]')
    task_content = request.POST.get('data[L_content]')
    start_time = request.POST.get('data[start_time]')
    end_time = request.POST.get('data[end_time]')
    sub_id = request.POST.get('data[sub_id]')
    try:
        with transaction.atomic():
            exittask = task.objects.filter(id=id).update(
                            group_id=group_id,
                            num=stu_num,
                            group_role=group_role,
                             task_id=task_id,
                            task_content=task_content,
                            start_time=start_time,
                            end_time=end_time,
                            task_type=task_type,
                            sub_id=sub_id
                            )
            back_dic['resultCode'] = 200
            back_dic['msg'] = '已完成任务修改'
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e) + "修改出现错误"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def bms_editlearn(request):#后台-任务添加
    back_dic = {'resultCode': None, 'msg': None, 'rows': None, 'cols': None, 'stu_list': None}
    id = request.POST.get('data[L_id]')
    obj_topic = request.POST.get('data[obj_topic]')
    obj_content = request.POST.get('data[obj_content]')
    obj_author = request.POST.get('data[obj_author]')
    obj_time = request.POST.get('data[obj_time]')
    obj_type= request.POST.get('data[obj_type]')
    try:
        with transaction.atomic():
            exitlearn = learn_obj.objects.filter(id=id).update(
                             obj_topic=obj_topic,
                             obj_content=obj_content,
                             obj_author=obj_author,
                             obj_time=obj_time,
                             obj_type=obj_type,
                            )
            back_dic['resultCode'] = 200
            back_dic['msg'] = '已完成学习主题修改'
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e) + "修改出现错误"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def bms_editnotice(request):#后台-编辑通知
    back_dic = {'resultCode': None, 'msg': None}
    id = request.POST.get('data[id]')
    send_num = request.POST.get('data[sendnum]')
    receive_num= request.POST.get('data[receivenum]')
    notice_title= request.POST.get('data[notice_title]')
    notice_content = request.POST.get('data[notice_content]')
    notice_type= request.POST.get('data[notice_type]')
    print(id)
    try:
        with transaction.atomic():
            exitnotice = notice.objects.filter(id=id).update(
                            send_num=send_num,
                            receive_num=receive_num,
                            notice_title=notice_title,
                            notice_content=notice_content,
                            notice_type=notice_type
                            )
            back_dic['resultCode'] = 200
            back_dic['msg'] = '已完成消息修改'
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e) + "修改出现错误"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def leader_taskadd(request):#组长-任务添加
    back_dic = {'resultCode': None, 'msg': None, 'rows': None, 'cols': None, 'stu_list': None}
    stu_num = request.POST.get('data[]')
    group_role = request.POST.get('group_role')
    task_id = request.POST.get('task_id')
    task_type= request.POST.get('task_type')
    task_content = request.POST.get('task_content')
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    sub_id = request.POST.get('sub_id')
    stu_info = list(Student.objects.filter(num=stu_num).values("num", "group_id", "group_role", "name"))  # 获得该名同学的组号、角色以及姓名
    group_id = stu_info[0]['group_id']
    try:
        with transaction.atomic():
            newtask = task(group_id=group_id,
                            num=stu_num, group_role=group_role, task_id=task_id, task_content=task_content,
                            start_time=start_time,end_time=end_time,is_finish=0,is_overtime=0,task_type=task_type,
                            sub_id=sub_id
                            )
            newtask.save()
            back_dic['resultCode'] = 200
            back_dic['msg'] = '已完成任务添加'
            return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e) + "修改出现错误"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def getstuinfo(request):#组长界面-获得成员信息
    back_dic = {'resultCode': None, 'msg': None}
    num = request.POST.get('stu_num')
    try:
        member = list(Student.objects.filter(num=num).values("num","name","group_role"))  # 找出该名同学
        back_dic['resultCode'] = 200
        back_dic['msg'] = '成功'
        back_dic['name'] = member[0]['name']
        back_dic['group_role'] = member[0]['group_role']
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e) + "修改出现错误"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")

def memberinfo(request):#组长界面-显示成员基本信息
    back_dic = {'resultCode': None, 'msg': None}
    num = request.POST.get('num')
    try:
        now_mem = Student.objects.filter(num=num)  # 找出该名同学
        user_info =list(User.objects.filter(num=num).values("phone","email"))
        now_data = serializers.serialize("json", now_mem)
        now_task= task.objects.filter(num=num)
        now_data1 = serializers.serialize("json", now_task)
        back_dic['resultCode'] = 200
        back_dic['msg'] = '成功'
        back_dic['meminfo'] = json.loads(now_data)
        back_dic['user_info'] = user_info
        back_dic['taskinfo'] = json.loads(now_data1)
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e) + "修改出现错误"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def send_notice(request):#组长-发送提醒通知
    back_dic = {'resultCode': None, 'msg': None}
    send_num=request.session.get('num')#发送者
    receive_num = request.POST.get('receive_num')#接收者
    send_stu=list(Student.objects.filter(num=send_num).values('num','name'))
    send_name=send_stu[0]['name']
    receive_stu=list(Student.objects.filter(num=receive_num).values('num','name'))
    receive_name=receive_stu[0]['name']
    task_id = request.POST.get('task_id')#任务id
    Tasks=list(task.objects.filter(task_id=task_id).values())
    task_content=Tasks[0]['task_content']
    end_time=Tasks[0]['end_time']
    is_overtime=Tasks[0]['is_overtime']
    notice_time = datetime.datetime.now() #通知时间
    notice_type =  '1'   #通知类型为提醒上传
    notice_title='请尽快上传'
    if is_overtime:
        #已超时
        overtime_days=Tasks[0]['overtime_days']
        notice_content = "请" + receive_name + "同学尽快提交任务" + task_id + ": " + task_content+"。  已超时"+str(abs(overtime_days))+"天"
    else:
        endtime = datetime.datetime.strptime(str(end_time), '%Y-%m-%d')
        now_time = notice_time.strftime('%Y-%m-%d')
        now_time = datetime.datetime.strptime(str(now_time), '%Y-%m-%d')
        ddl_days=(endtime - now_time).days
        notice_content="请"+receive_name+"同学尽快提交任务"+task_id+": "+task_content+"。离截止时间还有"+str(ddl_days)+"天"
    try:
        #上传消息通知
        new_notice=notice(
            send_num=send_num,
            receive_num=receive_num,
            notice_title=notice_title,
            notice_content=notice_content,
            notice_type=notice_type,
            notice_time=notice_time
        )
        new_notice.save()
        back_dic['resultCode'] = 200
        back_dic['msg'] = '设置提醒成功'
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    except Exception as e:
        print(e)
        back_dic['resultCode'] = -1
        back_dic['msg'] = str(e) + "修改出现错误"
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
def stuchat(request):
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    return render(request, 'chat.html', context=value)
def stucalls(request):
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    return render(request, 'calls.html', context=value)
def stucontacts(request):
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    return render(request, 'contacts.html', context=value)
def stuhelp(request):

    return render(request, 'help.html')
def reg(request):
    back_dic={'user':None,'msg':None,'code':None}
    num=request.POST.get('phone')
    pwd=request.POST.get('pwd')
    print(num);
    print(pwd);
    user = User.objects.filter(num=num).first()
    print(user)
    if user:
        back_dic['user'] = num
        back_dic['msg'] = '用户已存在'
        back_dic['code'] = 400
    else:
        newuser=User(num=num,pwd=pwd,power='学生')
        newuser.save()
        back_dic['user'] = num
        back_dic['msg'] = '注册成功'
        back_dic['code'] = 200
    import json
    return HttpResponse(json.dumps(back_dic))

def bms(request):
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    return render(request, 'homepage.html', context=value)
def welcome(request):
    return render(request, 'welcome.html')
def pjbz(request):
    return render(request, 'pjku.html')
def student_edit(request):
    return render(request, 'student-edit.html')
def user_edit(request):
    return render(request, 'user-edit.html')
def task_edit(request):
    return render(request, 'task-edit.html')
def learn_edit(request):
    return render(request, 'learn-edit.html')
def notice_edit(request):
    return render(request, 'notice-edit.html')
def group_edit(request):
    return render(request, 'group-edit.html')
def re(request):
    maxid=Student.objects.all().aggregate(Max('id'))
    print(maxid)
    maxid['id__max']=maxid['id__max']+1
    print(maxid)
    value={
        'max':maxid['id__max']
    }
    print('id最大值'+str(maxid['id__max']))
    return render(request, 'student-new.html',context=value)
def learn_new(request):
   maxid=learn_obj.objects.all().aggregate(Max('id'))
   if maxid:
            maxid['id__max']=maxid['id__max']+1

            value={
                'max':maxid['id__max']
            }
   else:
           maxid['id__max'] =  1
           value = {
               'max': maxid['id__max']
           }
   return render(request, 'learn_new.html',context=value)
def newuser(request):
    maxid=User.objects.all().aggregate(Max('id'))
    if maxid :
        maxid['id__max']=maxid['id__max']+1

        value={
            'max':maxid['id__max']
        }
    else :
        maxid['id__max'] = 1

        value = {
            'max': maxid['id__max']
        }
    return render(request, 'user-new.html',context=value)
def newtask(request):
    maxid=task.objects.all().aggregate(Max('id'))
    task_maxid=task.objects.all().aggregate(Max('task_id'))
    maxid['id__max']=maxid['id__max']+1
    task_maxid['task_id__max'] = task_maxid['task_id__max'] + 1
    print(maxid)
    value={
        'max':maxid['id__max'],
        'max_task': task_maxid['task_id__max']
    }
    print('id最大值'+str(maxid['id__max']))
    return render(request, 'task-new.html',context=value)
def newgroup(request):
    maxid=UserGroup.objects.all().aggregate(Max('id'))
    print(maxid)
    maxid['id__max']=maxid['id__max']+1
    print(maxid)
    value={
        'max':maxid['id__max']
    }
    print('id最大值'+str(maxid['id__max']))
    return render(request, 'group-new.html',context=value)
def delete_stu(request):
    stuid=request.POST.get('stuid')
    print(stuid)
    #删除学生信息
    Stu = Student.objects.get(num=stuid)
    Stu.delete()
    #删除用户信息
    user = User.objects.get(num=stuid)
    user.delete()
    back_dic = {'resultCode': 200}
    return HttpResponse(json.dumps(back_dic))
def delete_user(request):
    stuid=request.POST.get('stuid')
    print(stuid)
    #删除用户信息
    user = User.objects.get(num=stuid)
    user.delete()
    # 删除学生信息
    Stu = Student.objects.get(num=stuid)
    Stu.delete()
    back_dic = {'resultCode': 200}
    return HttpResponse(json.dumps(back_dic))
def delete_task(request):
    id=request.POST.get('id')
    print(id)
    #删除任务
    Task = task.objects.get(id=id)
    Task.delete()
    back_dic = {'resultCode': 200}
    return HttpResponse(json.dumps(back_dic))
def delete_chat_id(request):
    chat_id=request.POST.get('chat_id')
    print(chat_id)
    import os
    send_type=GroupChat.objects.filter(id=chat_id).first().send_type
    if int(send_type) == 2 :
        file_path=GroupChat.objects.filter(id=chat_id).first().send_content
        if os.path.exists(file_path):
            os.remove(file_path)
    chat = GroupChat.objects.get(id=chat_id)
    chat.delete()
    back_dic = {'resultCode': 200,'msg':"删除成功"}
    return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def delete_alltalk(request):
    group_id=request.POST.get('group_id')
    group_chats=list(GroupChat.objects.filter(group_id=group_id).values())
    if len(group_chats) == 0:
        back_dic = {'resultCode': -1, 'msg': "该组暂无聊天记录"}
        return HttpResponse(json.dumps(back_dic), content_type="application/json,charset=utf-8")
    for item in group_chats:
        send_type=item['send_type']
        if int(send_type)==2:
            import os
            file_path=item['send_content']
            id=item['id']
            if os.path.exists(file_path):
                os.remove(file_path)
            chat = GroupChat.objects.get(id=id)
            chat.delete()
        else:
            id = item['id']
            chat = GroupChat.objects.get(id=id)
            chat.delete()
    title = "第" + group_id + "组聊天记录"
    file_name = title + '.xls'
    import os
    file_path = os.path.join(settings.BASE_DIR, 'statics', 'group_talk', file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
    back_dic = {'resultCode': 200,'msg':"删除成功"}
    return HttpResponse(json.dumps(back_dic),content_type="application/json,charset=utf-8")
def delete_notice(request):
    id=request.POST.get('id')
    print(id)
    #删除任务
    notices = notice.objects.get(id=id)
    notices.delete()
    back_dic = {'resultCode': 200}
    return HttpResponse(json.dumps(back_dic))
def delete_doc(request):
    import os
    id=request.POST.get('id')
    submit_type = request.POST.get('submit_type')
    print(id)
    #删除上交任务
    if submit_type == 2 :
        path= doc.objects.filter(id=id).first().file_content
        os.remove(path)
    document = doc.objects.get(id=id)
    document.delete()
    back_dic = {'resultCode': 200}
    return HttpResponse(json.dumps(back_dic))
def delete_feedback(request):
    import os
    id=request.POST.get('id')
    feedback_id = request.POST.get('feedback_id')
    feedback_file = int(request.POST.get('feedback_file'))
    #删除附件
    if feedback_file  > 0 :
        file_list=list(feedbackfile.objects.filter(feedback_id=feedback_id).values())
        for item in file_list:
            path = item['file_path']
            os.remove(path)
    feedbackfiles = feedbackfile.objects.filter(feedback_id=feedback_id)
    feedbackfiles.delete()
    feedback = feed_back.objects.get(id=id)
    feedback.delete()
    back_dic = {'resultCode': 200}
    return HttpResponse(json.dumps(back_dic))
def delete_feedbackfile(request):
    import os
    id=request.POST.get('id')
    feedback_id = request.POST.get('feedback_id')
    file_path = request.POST.get('file_path')
    #删除附件
    path = file_path
    os.remove(path)
    feedbackfiles = feedbackfile.objects.filter(id=id)
    feedbackfiles.delete()
    numbers=int(feed_back.objects.filter(feedback_id=feedback_id).first().feedback_file)-1
    feedback = feed_back.objects.filter(feedback_id=feedback_id).update(
        feedback_file=numbers
    )
    back_dic = {'resultCode': 200}
    return HttpResponse(json.dumps(back_dic))
def delete_initfile(request):
    import os
    id=request.POST.get('id')
    file_path = init_info.objects.filter(id=id).first().file_path
    #删除附件
    path = file_path
    os.remove(path)
    feedbackfiles = init_info.objects.filter(id=id)
    feedbackfiles.delete()
    back_dic = {'resultCode': 200}
    return HttpResponse(json.dumps(back_dic))
def delete_learn(request):
    id=request.POST.get('id')
    learn = learn_obj.objects.filter(id=id)
    learn.delete()
    back_dic = {'resultCode': 200}
    return HttpResponse(json.dumps(back_dic))
def delete_group(request):
    groupid=request.POST.get('groupid')
    print(groupid)
    #删除小组信息
    group = UserGroup.objects.get(group_id=groupid)
    group.delete()
    back_dic = {'resultCode': 200}
    return HttpResponse(json.dumps(back_dic))
def changestuinfo(request):
    print(request.POST)
    id = request.POST.get('data[id]')
    Stuid = request.POST.get('data[stuid]')
    name = request.POST.get('data[name]')
    bj = request.POST.get('data[bj]')
    score = request.POST.get('data[score]')
    groupid = request.POST.get('data[group_id]')
    role = request.POST.get('data[group_role]')
    Student.objects.filter(num=Stuid).update(
        id=id,
        num=Stuid,
        name=name,
        grade=bj,
        score=score,
        group_id=groupid,
        group_role=role
    )
    back_dic = {'resultCode': 200}
    return HttpResponse(json.dumps(back_dic))
def changeuserinfo(request):
    print(request.POST)
    id = request.POST.get('data[id]')
    Stuid = request.POST.get('data[stuid]')
    name = request.POST.get('data[name]')
    power = request.POST.get('data[power]')
    pwd= request.POST.get('data[pwd]')
    User.objects.filter(num=Stuid).update(
        id=id,
        num=Stuid,
        pwd=pwd,
        power=power,
        name=name
    )
    back_dic = {'resultCode': 200}
    return HttpResponse(json.dumps(back_dic))
def changegroupinfo(request):
    print(request.POST)
    id = request.POST.get('data[id]')
    group_id = request.POST.get('data[groupid]')
    topic = request.POST.get('data[topic]')
    group_score = request.POST.get('data[score]')
    UserGroup.objects.filter(id=id).update(
        id=id,
        group_id=group_id,
        topic=topic,
        group_score=group_score,
    )
    back_dic = {'resultCode': 200}
    return HttpResponse(json.dumps(back_dic))
def newstuinfo(request):
    print(request.POST)
    id=request.POST.get('data[L_id]')
    Stuid = request.POST.get('data[Stuid]')
    name = request.POST.get('data[Name]')
    bj = request.POST.get('data[bj]')
    score = request.POST.get('data[score]')
    groupid = request.POST.get('data[groupid]')
    role = request.POST.get('data[role]')
    back_dic = {'num': None, 'name': None,'msg':None,
                'resultCode': None}
    stu = Student.objects.filter(num=Stuid).first()
    if stu:#已有该学生
        back_dic['num'] = Stuid
        back_dic['name'] = stu.name
        back_dic['msg'] = '添加错误，已有同学'+ back_dic['name']
        back_dic['resultCode'] = 500
        return HttpResponse(json.dumps(back_dic))
    else:#添加该名新同学
        newstu = Student(id=id,num=Stuid,name=name,grade=bj,score=score,group_id=groupid, group_role=role)
        newstu.save()
        #添加新用户
        newuser = User(num=Stuid, pwd=Stuid, power='学生',name=name)
        newuser.save()
        back_dic['resultCode'] = 200
        return HttpResponse(json.dumps(back_dic))
def newlearninfo(request):
    id=request.POST.get('data[L_id]')
    obj_topic = request.POST.get('data[obj_topic]')
    obj_content = request.POST.get('data[obj_content]')
    obj_type = request.POST.get('data[obj_type]')
    obj_author = request.session.get('name')  # 发送者
    obj_time = datetime.datetime.now()  # 时间
    back_dic = {'num': None, 'name': None,'msg':None,
                'resultCode': None}
    if not obj_author:
        back_dic['msg'] = '请先登录！'
        back_dic['resultCode'] = -1
        return HttpResponse(json.dumps(back_dic))
    else :
            newlearn = learn_obj(
                id=id,
                obj_content=obj_content,
                obj_time=obj_time,
                obj_author=obj_author,
                obj_type=obj_type,
                obj_topic=obj_topic
            )
            newlearn.save()
            back_dic['resultCode'] = 200
            return HttpResponse(json.dumps(back_dic))
def newuserinfo(request):
    print(request.POST)
    id=request.POST.get('data[id]')
    num = request.POST.get('data[num]')
    name = request.POST.get('data[Name]')
    pwd = request.POST.get('data[pwd]')
    power = request.POST.get('data[power]')
    back_dic = {'num': None, 'name': None,'msg':None,
                'resultCode': None}
    user = User.objects.filter(num=num).first()
    if user:#已有该用户
        back_dic['num'] = num
        back_dic['name'] = name
        back_dic['msg'] = '添加错误，已有用户'+ back_dic['name']
        back_dic['resultCode'] = 500
        return HttpResponse(json.dumps(back_dic))
    else:#添加该名新用户
        newuser = User(id=id,num=num,name=name,pwd=pwd,power=power)
        newuser.save()
        back_dic['resultCode'] = 200
        return HttpResponse(json.dumps(back_dic))
def newgroupinfo(request):
    print(request.POST)
    id=request.POST.get('data[id]')
    groupid = request.POST.get('data[groupid]')
    topic = request.POST.get('data[topic]')
    score = request.POST.get('data[score]')
    back_dic = {'msg':None,
                'resultCode': None}
    topic1 = UserGroup.objects.filter(topic=topic).first()
    if topic1:#已有该主题
        back_dic['msg'] = '添加错误，已有该学习主题: '+ topic
        back_dic['resultCode'] = 500
        return HttpResponse(json.dumps(back_dic))
    else:#添加该名新小组
        newgroup = UserGroup(id=id,group_id=groupid,topic=topic,group_score=score)
        newgroup.save()
        back_dic['resultCode'] = 200
        return HttpResponse(json.dumps(back_dic))
def sbi(request):
    id=request.POST.get('pk')
    stu = Student.objects.filter(id=id).first()
    back_dic = {'num': None, 'name': None, 'grade': None, 'score': None,'group_id': None,'group_role': None,'resultCode':None}
    if stu:
        back_dic['num']=stu.num
        back_dic['name']=stu.name
        back_dic['grade']=stu.grade
        back_dic['score']=stu.score
        back_dic['group_id']=stu.group_id
        back_dic['group_role']=stu.group_role
        back_dic['resultCode'] = 200
        return HttpResponse(json.dumps(back_dic))
    else :
        back_dic['resultCode'] = 500
        return HttpResponse(json.dumps(back_dic))
def sbc(request):
    id=request.POST.get('pk')
    user = User.objects.filter(id=id).first()
    back_dic = {'num': None, 'pwd': None, 'power': None, 'name': None}
    if user:
        back_dic['num']=user.num
        back_dic['name']=user.name
        back_dic['pwd']=user.pwd
        back_dic['power']=user.power
        back_dic['resultCode'] = 200
        return HttpResponse(json.dumps(back_dic))
    else :
        back_dic['resultCode'] = -1
        return HttpResponse(json.dumps(back_dic))
def query_task(request):
    id=request.POST.get('pk')
    Task = task.objects.filter(id=id).first()
    back_dic = {}
    print(str(Task.start_time))
    if Task:
        back_dic['group_id']=Task.group_id
        group_stu = Student.objects.filter(group_id=Task.group_id)
        task_list = task.objects.filter(group_id=Task.group_id)
        newdata = serializers.serialize("json", group_stu)
        taskdata = serializers.serialize("json", task_list)
        back_dic['list'] = json.loads(newdata)
        back_dic['task_list'] = json.loads(taskdata)
        back_dic['num'] = Task.num
        back_dic['role'] = Task.group_role
        back_dic['task_id']=Task.task_id
        back_dic['task_content']=Task.task_content
        back_dic['start_time']=str(Task.start_time)
        back_dic['end_time'] =str(Task.end_time)
        back_dic['type'] = Task.task_type
        back_dic['sub_id'] = Task.sub_id
        back_dic['resultCode'] = 200
        return HttpResponse(json.dumps(back_dic))
    else :
        back_dic['resultCode'] = -1
        return HttpResponse(json.dumps(back_dic))
def query_learn(request):
    id=request.POST.get('pk')
    print(id)
    learn = learn_obj.objects.filter(id=id).first()
    back_dic = {}
    if learn:
        back_dic['obj_author']=learn.obj_author
        back_dic['obj_type']=learn.obj_type
        back_dic['obj_topic']=learn.obj_topic
        back_dic['obj_content']=learn.obj_content
        back_dic['obj_time']=str(learn.obj_time)
        back_dic['resultCode'] = 200
        return HttpResponse(json.dumps(back_dic))
    else :
        back_dic['resultCode'] = -1
        return HttpResponse(json.dumps(back_dic))
def query_notice(request):
    id=request.POST.get('pk')
    notices = notice.objects.filter(id=id).first()
    back_dic = {}
    if notices:
        back_dic['send_num'] = notices.send_num
        back_dic['receive_num'] = notices.receive_num
        back_dic['notice_title'] = notices.notice_title
        back_dic['notice_content'] = notices.notice_content
        back_dic['notice_type'] = notices.notice_type
        back_dic['notice_time'] = str(notices.notice_time)
        back_dic['resultCode'] = 200
        return HttpResponse(json.dumps(back_dic))
    else :
        back_dic['resultCode'] = -1
        return HttpResponse(json.dumps(back_dic))
def sbg(request):
    id=request.POST.get('pk')
    group = UserGroup.objects.filter(id=id).first()
    back_dic = {'id': None, 'group_id': None, 'topic': None, 'group_score': None,'resultCode': None}
    if group:
        back_dic['id']=group.id
        back_dic['group_id']=group.group_id
        back_dic['topic']=group.topic
        back_dic['group_score']=group.group_score
        back_dic['resultCode'] = 200
        return HttpResponse(json.dumps(back_dic))
    else :
        back_dic['resultCode'] = 500
        return HttpResponse(json.dumps(back_dic))
def newtask_stu(request):
    id=request.POST.get('pk')#得到小组编号
    group_stu = Student.objects.filter(group_id=id)
    task_list = task.objects.filter(group_id=id)
    data={}
    if group_stu:
        newdata = serializers.serialize("json", group_stu)
        taskdata = serializers.serialize("json", task_list)
        data['list'] = json.loads(newdata)
        data['task_list'] = json.loads(taskdata)
        data['resultCode'] = 200
        return HttpResponse(json.dumps(data))
    else :
        data['resultCode'] = -1
        return HttpResponse(json.dumps(data))
def query_stu(request):
    num=request.POST.get('num')#得到小组编号
    stu_info = Student.objects.filter(num=num)
    data={}
    if stu_info:
        newdata = serializers.serialize("json", stu_info)
        data['list'] = json.loads(newdata)
        data['resultCode'] = 200
        return HttpResponse(json.dumps(data))
    else :
        data['resultCode'] = -1
        return HttpResponse(json.dumps(data))
def stu_list(request):
    if request.GET.get('Num'): #返回搜索框内容
        num=request.GET.get('Num')
        print(num)
        stu=Student.objects.filter(num=num)
        data={}
        newdata = serializers.serialize("json", stu)
        data['list'] = json.loads(newdata)
        data['count'] = 1
        return render(request, 'student-list.html',data)
    else : #返回所有

        mydata = Student.objects.all()
        data = {}
        newdata = serializers.serialize("json", mydata)
        data['list'] = json.loads(newdata)
        data['count'] = Student.objects.all().count()
    return render(request, 'student-list.html',data)
def task_list(request):
    if request.GET.get('group_id'): #返回搜索框内容
        id=request.GET.get('group_id')
        group=task.objects.filter(group_id=id)
        data={}
        newdata = serializers.serialize("json", group)
        data['list'] = json.loads(newdata)
        data['count'] = 1
        return render(request, 'task-list.html',data)
    else : #返回所有

        mydata = task.objects.all()
        data = {}
        newdata = serializers.serialize("json", mydata)
        data['list'] = json.loads(newdata)
        data['count'] = task.objects.all().count()
    return render(request, 'task-list.html',data)
def doc_list(request):
    if request.GET.get('group_id'): #返回搜索框内容
        id=request.GET.get('group_id')
        group=doc.objects.filter(group_id=id)
        data={}
        newdata = serializers.serialize("json", group)
        data['list'] = json.loads(newdata)
        data['count'] = 1
        return render(request, 'doc_list.html',data)
    else : #返回所有
        mydata = doc.objects.all()
        data = {}
        newdata = serializers.serialize("json", mydata)
        data['list'] = json.loads(newdata)
        data['count'] = doc.objects.all().count()
    return render(request, 'doc_list.html',data)
def notice_list(request):
    if request.GET.get('group_id'): #返回搜索框内容
        id=request.GET.get('group_id')
        group=notice.objects.filter(id=id)
        data={}
        newdata = serializers.serialize("json", group)
        data['list'] = json.loads(newdata)
        data['count'] = 1
        return render(request, 'notice_list.html',data)
    else : #返回所有
        mydata = notice.objects.all()
        data = {}
        newdata = serializers.serialize("json", mydata)
        data['list'] = json.loads(newdata)
        data['count'] = notice.objects.all().count()
    return render(request, 'notice_list.html',data)
def feedback_list(request):
    if request.GET.get('group_id'): #返回搜索框内容
        id=request.GET.get('group_id')
        group=feed_back.objects.filter(group_id=id)
        data={}
        newdata = serializers.serialize("json", group)
        data['list'] = json.loads(newdata)
        data['count'] = 1
        return render(request, 'feedback_list.html',data)
    else : #返回所有
        mydata = feed_back.objects.all()
        data = {}
        newdata = serializers.serialize("json", mydata)
        data['list'] = json.loads(newdata)
        data['count'] = doc.objects.all().count()
    return render(request, 'feedback_list.html',data)
def feedback_doclist(request):
    if request.GET.get('feedback_id'): #返回搜索框内容
        id=request.GET.get('feedback_id')
        print(id)
        group=feedbackfile.objects.filter(feedback_id=id)
        data={}
        newdata = serializers.serialize("json", group)
        data['list'] = json.loads(newdata)
        data['count'] = feedbackfile.objects.filter(feedback_id=id).count()
        return render(request, 'feedback_doclist.html',data)
    else : #返回所有
        mydata = feedbackfile.objects.all()
        data = {}
        newdata = serializers.serialize("json", mydata)
        data['list'] = json.loads(newdata)
        data['count'] = feedbackfile.objects.all().count()
    return render(request, 'feedback_doclist.html',data)
def systeminit(request):
    if request.GET.get('id'): #返回搜索框内容
        id=request.GET.get('id')
        group=init_info.objects.filter(id=id)
        data={}
        newdata = serializers.serialize("json", group)
        data['list'] = json.loads(newdata)
        data['count'] =init_info.objects.filter(id=id).count()
        return render(request, 'systeminit.html',data)
    else : #返回所有
        mydata = init_info.objects.all()
        data = {}
        newdata = serializers.serialize("json", mydata)
        data['list'] = json.loads(newdata)
        data['count'] = init_info.objects.all().count()
    return render(request, 'systeminit.html',data)
def learn_manage(request):
    if request.GET.get('id'): #返回搜索框内容
        id=request.GET.get('id')
        group=learn_obj.objects.filter(id=id)
        data={}
        newdata = serializers.serialize("json", group)
        data['list'] = json.loads(newdata)
        data['count'] =init_info.objects.filter(id=id).count()
        return render(request, 'learn_manage.html',data)
    else : #返回所有
        mydata = learn_obj.objects.all()
        data = {}
        newdata = serializers.serialize("json", mydata)
        data['list'] = json.loads(newdata)
        data['count'] = init_info.objects.all().count()
    return render(request, 'learn_manage.html',data)
def groupinfo(request):
    if request.GET.get('group_id'): #返回搜索框内容
        group_id=request.GET.get('group_id')
        print(group_id)
        group=UserGroup.objects.filter(group_id=group_id)
        data={}
        newdata = serializers.serialize("json", group)
        data['list'] = json.loads(newdata)
        data['count'] = 1
        return render(request, 'groupinfo.html',data)
    else : #返回所有
        mydata = UserGroup.objects.all()
        data = {}
        newdata = serializers.serialize("json", mydata)
        data['list'] = json.loads(newdata)
        data['count'] = Student.objects.all().count()
        print(data['list'][1])
        print(data['count'])
    return render(request, 'groupinfo.html',data)
def userpower(request):
    if request.GET.get('Name'): #返回搜索框内容
        name=request.GET.get('Name')

        user=User.objects.filter(name=name)
        data={}
        newdata = serializers.serialize("json", user)
        data['list'] = json.loads(newdata)
        data['count'] = 1
        return render(request, 'user-list.html',data)
    else : #返回所有
        mydata = User.objects.all()
        data = {}
        newdata = serializers.serialize("json", mydata)
        data['list'] = json.loads(newdata)
        data['count'] = Student.objects.all().count()

    return render(request, 'user-list.html',data)
def ste(request):
    import json
    mydata=Student.objects.all()
    data={}
    newdata=serializers.serialize("json", mydata)
    data['list']=json.loads(newdata)
    return JsonResponse(data)
def statistics(request):
    Student_count=Student.objects.all().count()
    User_count=User.objects.all().count()
    admin_count=User.objects.filter(power='管理员').count()
    print(Student_count)
    print(User_count)
    print(admin_count)
    back_dic = {'user': User_count, 'student': Student_count, 'admin': admin_count}
    import json
    return HttpResponse(json.dumps(back_dic))
def pj(request):
    import json
    #Eva=Evaluate.objects.all()

    data = {}
    book = Evaluate.objects.values()
    data['total'] = Evaluate.objects.all().count()
    data['rows'] = list(book)
    #print(data)
    return JsonResponse(data)
def pjgl(request):
    value = {'name': request.session.get('name'),
             'power': request.session.get('power'),
             'num': request.session.get('num')
             }
    return render(request, 'pj-edit.html',context=value)
def maxpjid(request):
    data={}
    maxid = Evaluate.objects.all().aggregate(Max('id'))
    if maxid:

        maxid['id__max'] = maxid['id__max'] + 1
        print(maxid)
        data['resultCode'] = 200
        data['max']=maxid['id__max']
        print('id最大值' + str(maxid['id__max']))
    else :
        data['resultCode'] = -1
    return JsonResponse(data)
def pjtijiao(request):
    print(request.POST)
    id = request.POST.get('id')
    evaluate_id= request.POST.get('evaluate_id')
    evaluate_type = request.POST.get('evaluate_type')
    evaluate_item = request.POST.get('evaluate_item')
    pub_time = request.POST.get('pub_time')
    evaluate_weight = request.POST.get('evaluate_weight')
    struct_type = request.POST.get('struct_type')
    back_dic = {'msg': None,
                'resultCode': None}
    eva_id = Evaluate.objects.filter(evaluate_id=evaluate_id).first()
    if  eva_id:  # 已有该评价
        back_dic['msg'] = '添加错误，已有评价编号' + eva_id
        back_dic['resultCode'] = -1
        return HttpResponse(json.dumps(back_dic))
    else:  # 添加该名新用户
        newpj = Evaluate(id=id, evaluate_id=evaluate_id,
                         evaluate_type=evaluate_type,
                         evaluate_item= evaluate_item,
                         pub_time=pub_time,
                         evaluate_weight=evaluate_weight,
                         struct_type=struct_type,
                         )
        newpj.save()
        back_dic['resultCode'] = 200
        return HttpResponse(json.dumps(back_dic))
def pjquery(request):
    import json
    print(request.GET.get('cxlx'))
    print(request.GET.get('cxnr'))
    cxlx=request.GET.get('cxlx')
    cxnr=request.GET.get('cxnr')
    data = {}
    if cxlx=='id':
        eva=Evaluate.objects.filter(id=cxnr).values()
        data['total'] = Evaluate.objects.filter(id=cxnr).count()
        data['rows'] = list(eva)
        if eva:
            data['code'] = 200
        else :
            data['code'] = -1
    elif cxlx=='evaluate_id':
        eva=Evaluate.objects.filter(evaluate_id=cxnr).values()
        data['total'] = Evaluate.filter(evaluate_id=cxnr).count()
        data['rows'] = list(eva)
        if eva:
            data['code'] = 200
        else:
            data['code'] = -1
    elif cxlx == 'evaluate_type':
        eva=Evaluate.objects.filter(evaluate_type=cxnr).values()
        data['total'] = Evaluate.objects.filter(evaluate_type=cxnr).count()
        data['rows'] = list(eva)
    elif cxlx == 'evaluate_item':
        eva=Evaluate.objects.filter(evaluate_item=cxnr).values()
        data['total'] = Evaluate.objects.filter(evaluate_item=cxnr).count()
        data['rows'] = list(eva)
        if eva:
            data['code'] = 200
        else :
            data['code'] = -1
    else :
        eva=Evaluate.objects.filter(evaluate_weight=cxnr).values()
        data['total'] = Evaluate.objects.filter(evaluate_weight=cxnr).count()
        data['rows'] = list(eva)
        if eva:
            data['code'] = 200
        else :
            data['code'] = -1
    return JsonResponse(data)