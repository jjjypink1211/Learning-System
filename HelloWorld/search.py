from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render
from TestModel.models import task
from TestModel.models import Student
from TestModel.models import UserGroup
from TestModel.models import GroupChat
from TestModel.models import eva_recollect
from TestModel.models import Evaluate
from TestModel.models import notice
from django.db.models import Avg,Max,Min,Count,Sum  #   引入函数
import numpy as np
import os
import docx
import re
import datetime
import jieba
import jieba.analyse
from wordcloud import WordCloud
import cv2
# 表单
def search_form(request):
    return render(request, 'search_form.html')
# 接收请求数据
def search(request):
    request.encoding = 'utf-8'
    if 'q' in request.GET and request.GET['q']:
        message = '你搜索的内容为: ' + request.GET['q']
    else:
        message = '你提交了空表单'
    return HttpResponse(message)
def get_pictures(word_path, result_path):
    """
    图片提取
    :param word_path: word路径
    :return:
    """
    try:
        doc = docx.Document(word_path)
        dict_rel = doc.part._rels
        for rel in dict_rel:
            rel = dict_rel[rel]
            if "image" in rel.target_ref:
                if not os.path.exists(result_path):
                    os.makedirs(result_path)
                img_name = re.findall("/(.*)", rel.target_ref)[0]
                word_name = os.path.splitext(word_path)[0]
                if os.sep in word_name:
                    new_name = word_name.split('\\')[-1]
                else:
                    new_name = word_name.split('/')[-1]
                img_name = f'{new_name}-'+'.'+f'{img_name}'
                with open(f'{result_path}/{img_name}', "wb") as f:
                    f.write(rel.target_part.blob)
    except:
        pass
def check_is_overtime():
    tasks=list(task.objects.all().values())
    for item in tasks :
        end_time=datetime.datetime.strptime(str(item['end_time']), '%Y-%m-%d')
        now_time=datetime.datetime.now()
        now_time=now_time.strftime('%Y-%m-%d')
        now_time=datetime.datetime.strptime(str(now_time), '%Y-%m-%d')
        if (end_time-now_time).days < 0 and item['is_finish'] == False and item['is_overtime'] == False:
            task.objects.filter(task_id=item['task_id']).update(
                is_overtime=True,
                overtime_days=(end_time-now_time).days,
            )
        elif (end_time-now_time).days < 0  and item['is_overtime'] == True:
            task.objects.filter(task_id=item['task_id']).update(
                overtime_days=(end_time - now_time).days,
            )
        elif (end_time-now_time).days > 0  and item['is_overtime'] == True:
            task.objects.filter(task_id=item['task_id']).update(
                is_overtime=False,
                overtime_days=0,
            )
        #和现在时间对比
def get_notice(num):
    # 用户的消息提醒
    notice_list = list(notice.objects.filter(receive_num=num).values())
    notice_count=len(notice_list)
    if notice_list:
        for item in notice_list:
            send_name = list(Student.objects.filter(num=item['send_num']).values())[0]['name']
            send_role = list(Student.objects.filter(num=item['send_num']).values())[0]['group_role']
            item['notice_time'] = item['notice_time'].strftime('%Y-%m-%d %H:%M:%S %p')
            item['send_name'] = send_name
            item['send_role'] = send_role
            item['notice_count'] = notice_count
        return notice_list
    else :
        notice_list=[{'notice_count':0}]
        return notice_list
week_list = ["星期日","星期一","星期二","星期三","星期四","星期五","星期六"]
def time_format(group_talk):
    now_time=datetime.datetime.now()
    for item in group_talk:
        start_time=item['send_time']
        days=(now_time - start_time).days
        item['days']=(now_time - start_time).days
        if days == 0:
            #当天
            time = int(item['send_time'].strftime('%H'))
            if time>=0 and time<6:
                item['send_time']='凌晨'+item['send_time'].strftime('%H:%M')
            elif time >=6 and time<=12:
                item['send_time'] = '上午' + item['send_time'].strftime('%H:%M')
            elif time>12 and time <=18:
                item['send_time'] = '下午' + item['send_time'].strftime('%H:%M')
            elif time >18 and time <24:
                item['send_time'] = '晚上' + item['send_time'].strftime('%H:%M')
        elif days == 1:
            #昨天
            time = int(item['send_time'].strftime('%H'))
            if time >= 0 and time < 6:
                item['send_time'] = '昨天 凌晨' + item['send_time'].strftime('%H:%M')
            elif time >= 6 and time <= 12:
                item['send_time'] = '昨天 上午' + item['send_time'].strftime('%H:%M')
            elif time > 12 and time <= 18:
                item['send_time'] = '昨天 下午' + item['send_time'].strftime('%H:%M')
            elif time > 18 and time < 24:
                item['send_time'] = '昨天 晚上' + item['send_time'].strftime('%H:%M')
        elif days > 1 and days <= 7 :
            #星期
            # 昨天
            time = int(item['send_time'].strftime('%H'))
            weeks = int(item['send_time'].strftime('%w'))
            if time >= 0 and time < 6:
                item['send_time'] = week_list[weeks]+' 凌晨' + item['send_time'].strftime('%H:%M')
            elif time >= 6 and time <= 12:
                item['send_time'] = week_list[weeks]+' 上午' + item['send_time'].strftime('%H:%M')
            elif time > 12 and time <= 18:
                item['send_time'] = week_list[weeks]+' 下午' + item['send_time'].strftime('%H:%M')
            elif time > 18 and time < 24:
                item['send_time'] = week_list[weeks]+' 晚上' + item['send_time'].strftime('%H:%M')
        else:
            time = int(item['send_time'].strftime('%H'))
            time_ymd = item['send_time'].strftime('%Y年%m月%d日')
            if time >= 0 and time < 6:
                item['send_time'] = time_ymd + ' 凌晨' + item['send_time'].strftime('%H:%M')
            elif time >= 6 and time <= 12:
                item['send_time'] = time_ymd + ' 上午' + item['send_time'].strftime('%H:%M')
            elif time > 12 and time <= 18:
                item['send_time'] = time_ymd + ' 下午' + item['send_time'].strftime('%H:%M')
            elif time > 18 and time < 24:
                item['send_time'] = time_ymd + ' 晚上' + item['send_time'].strftime('%H:%M')
def is_user(group_talk,user_num):
    for item in group_talk:
        if item['send_num']==user_num:
            item['is_user'] = True
        else :
            item['is_user'] = False
def find_talk(group_peo,member_info):
    for item in member_info:
        stu_num=item['num']
        if GroupChat.objects.filter(send_num=stu_num).last():
            start_time=GroupChat.objects.filter(send_num=stu_num).values('send_time').last()['send_time']
            if GroupChat.objects.filter(send_num=stu_num).values('send_content','send_type').last()['send_type']=='2':
                file_path = GroupChat.objects.filter(send_num=stu_num).values('send_content').last()['send_content']
                import os
                if os.sep in file_path:
                    file_name = file_path.split('\\')[-1]
                else:
                    file_name = file_path.split('/')[-1]
                item['recent_content'] =file_name
            else:
                item['recent_content']=GroupChat.objects.filter(send_num=stu_num).values('send_content').last()['send_content']
            now_time = datetime.datetime.now()
            days = (now_time - start_time).days
            if days == 0:
                # 当天
                time = int(start_time.strftime('%H'))
                if time >= 0 and time < 6:
                    item['recent_talk'] = '凌晨' + start_time.strftime('%H:%M')
                elif time >= 6 and time <= 12:
                    item['recent_talk'] = '上午' + start_time.strftime('%H:%M')
                elif time > 12 and time <= 18:
                    item['recent_talk'] = '下午' + start_time.strftime('%H:%M')
                elif time > 18 and time < 24:
                    item['recent_talk'] = '晚上' + start_time.strftime('%H:%M')
            elif days == 1:
                # 昨天
                time = int(start_time.strftime('%H'))
                if time >= 0 and time < 6:
                    item['recent_talk'] = '昨天 凌晨' + start_time.strftime('%H:%M')
                elif time >= 6 and time <= 12:
                    item['recent_talk'] = '昨天 上午' + start_time.strftime('%H:%M')
                elif time > 12 and time <= 18:
                    item['recent_talk'] = '昨天 下午' + start_time.strftime('%H:%M')
                elif time > 18 and time < 24:
                    item['recent_talk'] = '昨天 晚上' + start_time.strftime('%H:%M')
            elif days > 1 and days <= 7:
                # 星期
                # 昨天
                time = int(start_time.strftime('%H'))
                weeks = int(start_time.strftime('%w'))
                if time >= 0 and time < 6:
                    item['recent_talk'] = week_list[weeks] + ' 凌晨' + start_time.strftime('%H:%M')
                elif time >= 6 and time <= 12:
                    item['recent_talk'] = week_list[weeks] + ' 上午' + start_time.strftime('%H:%M')
                elif time > 12 and time <= 18:
                    item['recent_talk'] = week_list[weeks] + ' 下午' + start_time.strftime('%H:%M')
                elif time > 18 and time < 24:
                    item['recent_talk'] = week_list[weeks] + ' 晚上' + start_time.strftime('%H:%M')
            else:
                time = int(start_time.strftime('%H'))
                time_ymd = start_time.strftime('%Y年%m月%d日')
                if time >= 0 and time < 6:
                    item['recent_talk'] = time_ymd + ' 凌晨' + start_time.strftime('%H:%M')
                elif time >= 6 and time <= 12:
                    item['recent_talk'] = time_ymd + ' 上午' + start_time.strftime('%H:%M')
                elif time > 12 and time <= 18:
                    item['recent_talk'] = time_ymd + ' 下午' + start_time.strftime('%H:%M')
                elif time > 18 and time < 24:
                    item['recent_talk'] = time_ymd + ' 晚上' + start_time.strftime('%H:%M')
        else:
            item['recent_talk'] = '无'
        item['talk_count'] = 0
        for talk in group_peo:
            num=talk['send_num']
            if num == item['num']:
                item['talk_count']=talk['count']
def check_is_submit(num,group_id,eva_type,eva_list):
    is_submit=False
    submit_list=list(eva_recollect.objects.filter(
        valuer_num=num,
        group_id=group_id,
        eva_type=eva_type
    ).values())
    if submit_list:
        is_submit = True
        return is_submit
    else:
        return is_submit
def is_evagroup(diffgroup_info,num,group_id,eva_type):
    for item in diffgroup_info:
        diffgroup_id=item['group_id']
        is_submit = False
        submit_list = list(eva_recollect.objects.filter(
            valuer_num=num,
            group_id=group_id,
            beeva_num=diffgroup_id,
            eva_type=eva_type
        ).values())
        if submit_list:
            is_submit = True
            item['is_submit']=is_submit
        else:
            item['is_submit']=is_submit
def is_evamember(mem_list, num, group_id,eva_type):
    for item in mem_list:
        mem_num=item['num']
        is_submit = False
        submit_list = list(eva_recollect.objects.filter(
            valuer_num=num,
            group_id=group_id,
            beeva_num=mem_num,
            eva_type=eva_type
        ).values())
        if submit_list:
            is_submit = True
            item['is_submit']=is_submit
        else:
            item['is_submit']=is_submit
def get_title(eva_type):
    title_list=list(Evaluate.objects.filter(evaluate_type=eva_type).values('evaluate_id',"evaluate_type","evaluate_item"))
    return title_list
def get_titles(eva_type):
    title_list=list(Evaluate.objects.filter(evaluate_type=eva_type,struct_type=1).values('evaluate_id',"evaluate_type","evaluate_item"))
    return title_list
def averagescore(item,count,title_list,avg_list):
    if count==0:
        item['PSQ'] = 0
    else :
        for title in title_list:
            avg_list.append({'group_id':item['group_id'],'evaluate_item':title['evaluate_item'],'score':item[title['evaluate_item']]})
def group_weight(group_list):#评价所占权重
   group_id=group_list['group_id']
   stu_list=list(Student.objects.filter(group_id=group_id).values("num","name","group_role"))
   stu_count=Student.objects.filter(group_id=group_id).count()
   for stu in stu_list:
       if stu_count == 1:
             stu['weight'] = 1
       elif stu_count == 2:
             stu['weight'] = 0.5
       elif stu_count == 3:
           if stu['group_role']=='组长':
                 stu['weight']=0.34
           else:
               stu['weight'] = 0.33
       elif stu_count == 4:
           if stu['group_role']=='组长':
                stu['weight']=0.4
           elif stu['group_role']=='检察员':
               stu['weight'] = 0.2
           elif stu['group_role']=='记录员':
               stu['weight'] = 0.2
           elif stu['group_role'] == '报告员':
               stu['weight'] = 0.2
           elif stu['group_role'] == '尚未指定' or stu['group_role'] == '组员':
               stu['weight'] = 0.2
       elif stu_count == 5:
           if stu['group_role']=='组长':
                stu['weight']=0.5
           elif stu['group_role']=='检察员':
               stu['weight'] = 0.2
           elif stu['group_role']=='记录员':
               stu['weight'] = 0.1
           elif stu['group_role'] == '报告员':
               stu['weight'] = 0.1
           elif stu['group_role'] == '组员' or stu['group_role'] == '尚未指定':
               stu['weight'] = 0.1
   return stu_list
def sum_weight(score,num,member_weight):#计算加权值
    score_weight=0
    for item in member_weight:
        if item['num'] == num:
            score_weight = round(score * item['weight'],2)
    return score_weight
def sum_avggroup(item,eva_list):
    data={}
    data['group_id']=item['group_id']
    group_list = list(UserGroup.objects.all().values())
    for eva in eva_list:
        stu_list=list(eva_recollect.objects.filter(pj_id=eva['pj_id']).values())
        for group in group_list:
            if group['group_id']!= data['group_id'] and stu_list[0]['group_id']== group['group_id']:
                member_weight = group_weight(group)  # 计算各组的权重
                if str(group['group_id']) in data :
                    for score in stu_list:
                        question = Evaluate.objects.filter(evaluate_id=score['eva_id']).first().evaluate_item
                        data[str(group['group_id'])][str(question)] = data[str(group['group_id'])][str(question)] + sum_weight(int(score['eva_content']), score['valuer_num'], member_weight)
                else:
                      data[str(group['group_id'])]={}
                      for score in stu_list:
                          question = Evaluate.objects.filter(evaluate_id=score['eva_id']).first().evaluate_item
                          data[str(group['group_id'])][str(question)] = sum_weight(int(score['eva_content']),score['valuer_num'], member_weight)
    return data
def diffgroupavg():#计算组间互评加权平均值
    avg_list = []
    group_list = list(UserGroup.objects.all().values())
    #print(eva_list)
    for item in group_list:
        #member_weight = group_weight(item)  # 计算各组的权重
        eva_list = list(eva_recollect.objects.filter(eva_type='组间互评',beeva_num=item['group_id']) \
                        .values("pj_id") \
                        .annotate(count=Count('pj_id')) \
                        .values("pj_id", "valuer_num", "beeva_num", "eva_type", "group_id"))
        if eva_list:
            group_avg=sum_avggroup(item,eva_list)
            avg_list.append(group_avg)
    return avg_list
def get_groupeva(group_id,eva_type):
    eva_data={}
    data=[]
    mem_list=list(Student.objects.filter(group_id=group_id).values())
    for member in mem_list:
        eva_data[member['num']]=[]
    eva_data['name'] = []
    eva_list=list(eva_recollect.objects.filter(group_id=group_id,eva_type=eva_type)\
                        .values("pj_id") \
                        .annotate(count=Count('pj_id')) \
                        .values("pj_id", "valuer_num", "beeva_num", "eva_type", "group_id"))
    for eva in eva_list:
        stu_list=list(eva_recollect.objects.filter(pj_id=eva['pj_id'],form_type=1).values())
        for item in stu_list:
            eva_content=Evaluate.objects.filter(evaluate_id=item['eva_id']).first().evaluate_item
            eva_data[item['valuer_num']].append(item['eva_content'])
    for member in mem_list:
        eva_data['name'].append({
            'name':member['name'],
            'num':member['num']
        })
    return eva_data
def get_grouplearn():
    time_avgdata=[]
    group_list = list(UserGroup.objects.all().values())
    for group in group_list:
            eva_list = list(eva_recollect.objects.filter(group_id=group['group_id'],eva_type='组内评价') \
                            .values("pj_id") \
                            .annotate(count=Count('pj_id')) \
                            .values("pj_id", "valuer_num", "beeva_num", "eva_type", "group_id"))
            if eva_list:
                avgtime=[]
                for eva in eva_list:
                    time_data=int(eva_recollect.objects.filter(pj_id=eva['pj_id'],eva_id='03-04-06',eva_type='组内评价').first().eva_content)
                    avgtime.append(time_data)
                time_avgdata.append(
                    {
                        'group_id': '第'+str(group['group_id'])+'组',
                        'avg_time': np.mean(avgtime)
                    }
                )
            else:
                time_avgdata.append(
                    {
                        'group_id': '第'+str(group['group_id'])+'组',
                        'avg_time': 0
                    }
                )
    #print(time_avgdata);
    return time_avgdata
def get_grouptask(group_id):
    data=[]
    mem_list=list(Student.objects.filter(group_id=group_id).values("num","name","group_role"))
    #print(mem_list)
    for stu in mem_list:
        task_list=list(task.objects.filter(num=stu['num']).values("num","task_id","is_finish","is_overtime","overtime_days"))
        task_count=len(task_list)#小组任务总数
        task_fin_over=0
        task_nonfin_over=0
        task_fin_nonover=0
        task_nonfin_nonover=0
        for tasks in task_list:
            if tasks["is_finish"]== True and tasks["is_overtime"]==True:
                task_fin_over =task_fin_over+1
            elif tasks["is_finish"]== False and tasks["is_overtime"]==True:
                task_nonfin_over = task_nonfin_over+1
            elif tasks["is_finish"]== True and tasks["is_overtime"]== False:
                task_fin_nonover=task_fin_nonover+1
            elif tasks["is_finish"]== False and tasks["is_overtime"]== False :
                task_nonfin_nonover = task_nonfin_nonover+1
        #print(str(task_fin_over)+":"+str(task_nonfin_over)+":"+str(task_fin_nonover)+":"+str(task_nonfin_nonover)+":")
        data.append(
            {
              'name':stu['name'],
              'num' :stu['num'],
              '超时完成': task_fin_over,
              '超时未完成':task_nonfin_over,
              '已完成':task_fin_nonover,
              '未完成':task_nonfin_nonover,
            })
    return data
def get_membertimedata(group_id):
    data_1 = []
    data_2 = []
    data=[]
    alldata={}
    name_list=[]
    mem_list = list(Student.objects.filter(group_id=group_id).values("num", "name", "group_role"))
    eva_list = list(eva_recollect.objects.filter(group_id=group_id, eva_type='个人评价') \
                    .values("pj_id") \
                    .annotate(count=Count('pj_id')) \
                    .values("pj_id", "valuer_num", "beeva_num", "eva_type", "group_id"))
    for eva in eva_list:
        name_list.append(
            Student.objects.filter(num=eva['valuer_num']).first().name,
        )
        time_data=list(eva_recollect.objects.filter(pj_id=eva['pj_id'],form_type=2).values("pj_id", "valuer_num","eva_id","eva_content"))
        for item in time_data:
            if item['eva_id']=='03-05-08':
                data_1.append(item['eva_content'])
            elif item['eva_id']=='03-05-09':
                data_2.append(item['eva_content'])
    data.append({
        'name':Evaluate.objects.filter(evaluate_id='03-05-08').first().evaluate_item,
        'data':data_1
    }
    )
    data.append({
        'name': Evaluate.objects.filter(evaluate_id='03-05-09').first().evaluate_item,
        'data': data_2
    }
    )
    alldata={
        'name_list':name_list,
        'data':data
    }
    return alldata
def get_memberrank(group_id):#返回成员个人信息
    alldata={}
    data=[]
    mem_list = list(Student.objects.filter(group_id=group_id).values("num", "name", "group_role"))

    for member in mem_list:
       num=member['num']
       eva_list = list(eva_recollect.objects.filter(valuer_num=num,group_id=group_id, form_type=1,eva_type='个人评价').values())
       score=[]
       if eva_list:
           for eva in eva_list:
               score.append(int(eva['eva_content']))
       else:
           score=[0]
       mem_score=[]
       inter_eva = list(eva_recollect.objects.filter(valuer_num=num, group_id=group_id, form_type=1, eva_type='成员互评').values())
       if inter_eva:
           for inter in inter_eva:
               mem_score.append(int(inter['eva_content']))
       else:
           mem_score = [0]
       data.append({
           'name':member['name'],
           'role': member['group_role'],
           'self_eva': round(np.mean(score), 2),
           'inter_eva':round(np.mean(mem_score),2),
           'sum_score': round(np.mean(score)*0.3+0.7*np.mean(mem_score),2)
       })

    data=sorted(data, key=lambda da: da['sum_score'],reverse=True)
    i=1
    for rank in data:
        rank['rank']=i
        i=i+1
    return data
def get_wordcloud(group_id):
    text=[]
    alldata = {}
    chat=list(GroupChat.objects.filter(group_id=group_id,send_type=1).values("send_content"))
    chat_count=GroupChat.objects.filter(group_id=group_id,send_type=1).count()
    if chat_count==0:
        alldata = {
            'chat_count': '0',
            'file_count': '0',
            'word_count': '0',
            'data': ['0','0%']
        }
        return alldata
    file_count = GroupChat.objects.filter(group_id=group_id, send_type=2).count()
    word_count = GroupChat.objects.filter(group_id=group_id, send_type=1).count()
    for item in chat:
        text.append(item['send_content'])
    # 切割分词
    wordlist = jieba.lcut_for_search(''.join(text))
    result = ' '.join(wordlist)

    # 设置停用词
    stop_words = ['你', '我', '的', '了', '们','可以','具有','和','与','所']
    ciyun_words = ''

    # 过滤后的词
    for word in result:
        if word not in stop_words:
            ciyun_words += word
    import os
    file_path = os.path.join(settings.BASE_DIR, 'statics', 'wordyun', 'tree.png')
    # 读取图片
    im = cv2.imread(file_path)
    # 设置参数，创建WordCloud对象
    wc = WordCloud(
        font_path='msyh.ttc',  # 中文
        background_color='white',  # 设置背景颜色为白色
        #stopwords=stop_words,  # 设置禁用词，在生成的词云中不会出现set集合中的词
        mask=im,
    )
    # 根据文本数据生成词云
    wc.generate(ciyun_words)
    # 保存词云文件
    file_path = os.path.join(settings.BASE_DIR, 'statics', 'wordyun', 'img.jpg')
    wc.to_file(file_path)
    # 权重分析
    tag = jieba.analyse.extract_tags(sentence=ciyun_words, topK=5, withWeight=True)
    tag_data=[]
    for item in tag:
        tag_data.append({
            'word': item[0],
            'weight':"%.2f%%" % (item[1]*100),
        })
    alldata = {
        'chat_count': chat_count,
        'file_count': file_count,
        'word_count': word_count,
        'data': tag_data
    }
    return alldata
def get_memberwordcloud(num):
    text=[]
    alldata={}
    chat=list(GroupChat.objects.filter(send_num=num,send_type=1).values("send_content"))
    chat_count = GroupChat.objects.filter(send_num=num).count()
    if chat_count==0:
        alldata = {
            'chat_count': '0',
            'file_count': '0',
            'word_count': '0',
            'data': ['0','0%']
        }
        return alldata
    file_count = GroupChat.objects.filter(send_num=num,send_type=2).count()
    word_count = GroupChat.objects.filter(send_num=num, send_type=1).count()
    for item in chat:
        text.append(item['send_content'])
    # 切割分词
    wordlist = jieba.lcut_for_search(''.join(text))
    result = ' '.join(wordlist)

    # 设置停用词
    stop_words = ['你', '我', '的', '了', '们','可以','具有','和','与','所']
    ciyun_words = ''

    # 过滤后的词
    for word in result:
        if word not in stop_words:
            ciyun_words += word
    import os
    file_path = os.path.join(settings.BASE_DIR, 'statics', 'wordyun', 'tree.png')
    # 读取图片
    im = cv2.imread(file_path)
    # 设置参数，创建WordCloud对象
    wc = WordCloud(
        font_path='msyh.ttc',  # 中文
        background_color='white',  # 设置背景颜色为白色
        #stopwords=stop_words,  # 设置禁用词，在生成的词云中不会出现set集合中的词
        mask=im,
    )
    # 根据文本数据生成词云
    wc.generate(ciyun_words)
    # 保存词云文件
    file_path = os.path.join(settings.BASE_DIR, 'statics', 'wordyun', 'mem_img.jpg')
    wc.to_file(file_path)
    # 权重分析
    tag = jieba.analyse.extract_tags(sentence=ciyun_words, topK=5, withWeight=True)
    tag_data=[]
    for item in tag:
        tag_data.append({
            'word': item[0],
            'weight':"%.2f%%" % (item[1]*100),
        })
    alldata = {
        'chat_count':chat_count,
        'file_count':file_count,
        'word_count':word_count,
        'data': tag_data
    }
    return alldata
def get_selfeva(num):
    score_data=[]
    data=[]
    eva_list=list(eva_recollect.objects.filter(valuer_num=num,eva_type='个人评价',form_type=1).values("pj_id","eva_id","eva_content"))
    for item in eva_list:
        score_data.append(item['eva_content'])
    data.append({
        'name': Student.objects.filter(num=num).first().name,
        'data': score_data
    })
    return data
def get_intereva(num):
    score_data=[]
    data=[]
    eva_list = list(eva_recollect.objects.filter(beeva_num=num,eva_type='成员互评',form_type=1) \
                    .values("pj_id") \
                    .annotate(count=Count('pj_id')) \
                    .values("pj_id", "valuer_num", "beeva_num", "eva_type", "group_id"))
    for eva in eva_list:
        stu_list=list(eva_recollect.objects.filter(pj_id=eva['pj_id']).values("pj_id","valuer_num","eva_id","eva_content"))
        num=stu_list[0]['valuer_num']
        for item in stu_list:
            score_data.append(item['eva_content']);
        data.append({
            'name': Student.objects.filter(num=num).first().name,
            'data': score_data
        })
    return data
def get_titledata():
    data=[]
    alldata={}
    group_list=list(UserGroup.objects.all().values("group_id","topic"))
    evaid_list=["03-04-01","03-04-04","03-04-05","03-04-02"]
    for item in evaid_list:
        for group in group_list:
            member_weight = group_weight(group)  # 计算各组成员的权重
            eva_list=list(eva_recollect.objects.filter(eva_id=item,group_id=group['group_id']).values("pj_id","valuer_num","eva_id","eva_content"))
            if len(eva_list) == 0:
                data.append({
                    'group_id':group['group_id'],
                    'topic': group['topic'],
                    'avg_data':0
                })
                continue
            score=0
            for eva in eva_list:
                score=round(score+sum_weight(int(eva['eva_content']),eva['valuer_num'],member_weight),2)#计算加权值
            data.append({
                'group_id': group['group_id'],
                'topic': group['topic'],
                'avg_data': score
            })
        name=Evaluate.objects.filter(evaluate_id=item).first().evaluate_item
        alldata[name]=data
        alldata[name]=sorted(alldata[name], key=lambda da: da['avg_data'], reverse=True)
        data=[]
    return alldata
def sum_techeva(tech_list,group_id,num):
    datas=[]
    score = []
    for item in tech_list:
        eva_list=list(eva_recollect.objects.filter(valuer_num=num,eva_id=item,beeva_num=group_id).values("eva_id","eva_content"))
        if eva_list:
            for eva in eva_list:
                score.append(int(eva['eva_content']))
            score=np.mean(score)
            datas.append(score)
            score = []
        else :
            datas.append(0)
    score=np.mean(datas)
    #print(score)
    return score

def sum_stueva(stu_list,group_id):
    datas = []
    allscore=0
    member_weight = group_weight({'group_id':group_id})  # 计算各组的权重
    for item in stu_list:
        eva_list = list(eva_recollect.objects.filter(eva_id=item, group_id=group_id).values("valuer_num","eva_id", "eva_content"))
        if eva_list:
            score=0
            for eva in eva_list:
                num=eva['valuer_num']
                score=int(eva['eva_content'])
                allscore=allscore+sum_weight(score, num, member_weight) # 计算加权值
            datas.append(allscore)
            allscore = 0
        else:
            datas.append(0)
    allscore = np.mean(datas)
    return allscore
def get_multiple(num):
    multi_evalist=[{
        'multi_evaid':'03-01-01',
        'teacher_eva':['03-03-04'],
        'stu_eva':['03-04-04'],
    },{
        'multi_evaid': '03-01-02',
        'teacher_eva': ['03-03-02'],
        'stu_eva': ['03-04-01'],

    },{
        'multi_evaid': '03-01-03',
        'teacher_eva': ['03-02-02'],
        'stu_eva': ['03-04-03'],

    },{
        'multi_evaid': '03-01-04',
        'teacher_eva': ['03-03-01','03-01-11'],
        'stu_eva': ['03-04-05'],

    }]
    group_list=list(UserGroup.objects.all().values())
    data=[]
    for group in group_list:
        group_id=group['group_id']
        score_list=[]
        for multi_item in multi_evalist:
            tech_list=multi_item['teacher_eva']
            stu_list=multi_item['stu_eva']
            tech_score=sum_techeva(tech_list,group_id,num)
            stu_score=sum_stueva(stu_list,group_id)
            allscore=round(0.5*tech_score+0.5*stu_score,2)
            score_list.append(allscore)
        data.append({
            'group_name':'第'+str(group['group_id'])+'组',
            'score_list':score_list
        })
    return data
def get_multiplescore(group_multiple,group_list):
    i=0
    for item in group_multiple:
          mark=0
          for score in item['score_list']:
              mark=mark+score*5
          group_list[i]['mark']=mark
          i=i+1
def member_manage():
    group_role=['组长','记录员','报告员','检察员','组员']
    group_list=list(UserGroup.objects.all().values("group_id","topic"))
    group_count = list(Student.objects.exclude(group_id=0).values("group_id").annotate(count=Count('group_id')).values("group_id","count"))
    for item in group_list:
        item['group_count']=Student.objects.filter(group_id=item['group_id']).count()
        stu_list=list(Student.objects.filter(group_id=item['group_id']).values('num','group_role'))
        item['hasbeen_spec']=[]
        item['nothasbeen_spec']=[]
        for stu in stu_list:
            if stu['group_role'] in group_role:
                item['hasbeen_spec'].append(stu['group_role'])
            else:
                #分配小组,没分配角色
                item['nothasbeen_spec'].append(stu['num'])
    return group_list
def id_is_same(group_num,group_con):
    group_list=UserGroup.objects.filter(group_id=group_num)
    if group_list:
        group_topic=UserGroup.objects.filter(topic=group_con)
        if group_topic:
            return True
        else:
            maxid = UserGroup.objects.all().aggregate(Max('group_id'))
            print(maxid)
            if maxid['group_id__max'] == None:
                maxid['group_id__max'] = 1
            else:
                maxid['group_id__max'] = maxid['group_id__max'] + 1
            group_num=maxid['group_id__max']
            return False

    else:
        group_topic = UserGroup.objects.filter(topic=group_con)
        if group_topic:
            return True
        else:
            return False