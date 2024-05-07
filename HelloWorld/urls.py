from django.conf.urls import url
from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from . import views,search,search2
urlpatterns = [
    url('chat/',include('TestModel.urls')),#小组群聊室
    url('grouptalkfile/', views.grouptalkfile),#上传小组聊天文件
    url('dlgroupfile/', views.dlgroupfile),#下载小组文件
    url('index/', views.index),
    url('indextech/', views.indextech), #教师管理主页
    url('feedbackemail/', views.feedbackemail), #教师管理-反馈邮箱
    url('feedback_delete/', views.feedback_delete), #教师管理-删除反馈邮箱
    url('showmaildetail/', views.showmaildetail), #教师管理-显示邮件详情
    url('sendfeedback/', views.sendfeedback), #组长管理-发送反馈
    url('replyfeedback/', views.replyfeedback), #组长管理-发送反馈
    url('addfeedbackmsg/', views.addfeedbackmsg), #组长-提交反馈信息
    url('addreplyfeedbackmsg/', views.addreplyfeedbackmsg), #教师-回复反馈信息
    url('stumanage/', views.stumanage),  #教师/组长-成员管理模块
    url('scoremanage/', views.scoremanage),  #教师管理-成绩管理模块
    url('memberscore/', views.memberscore),  #教师管理-成绩管理-显示个人成绩
    url('scoremanagechange/', views.scoremanagechange),  #教师管理-成绩管理-修改成绩
    url('stumanagechange/', views.stumanagechange),  #教师管理-成员管理-修改状态
    url('addnewgroupmember/', views.addnewgroupmember),  #教师管理-成员管理-添加成员
    url('onloadgroupinfo/', views.onloadgroupinfo),  #教师管理-成员管理-加载信息
    url('submitchooserole/', views.submitchooserole),  #教师管理-成员管理-指定角色
    url('data_analysis/', views.data_analysis),  #教师管理-评论分析
    url('detail_groupinfo/', views.detail_groupinfo),  #教师管理-评论分析-各小组评论详情
    url('detail_memberinfo/', views.detail_memberinfo),  #教师管理-评论分析-小组成员个人情况
    url('tech_eva_manage/', views.tech_eva_manage),  #教师管理-评论管理
    url('stu_pj_manage/', views.stu_pj_manage),  #学生主页-评论管理
    url('display_eva/', views.display_eva),  #教师管理-评价信息展示
    url('display_stu_eva/', views.display_stu_eva),  #学生管理-评价信息展示
    url('delete_stu_eva/', views.delete_stu_eva),  #学生管理-评价信息删除
    url('techinit/', views.techinit), #教师登录初始界面
    url('techinitinfo/', views.techinitinfo), #初始化信息界面
    url('stuinitinfo/', views.stuinitinfo), #手动添加学生信息
    url('userset/', views.user_info), #用户设置
    url('groupinitinfo/', views.groupinitinfo), #手动添加小组信息
    url('addinitinfo/', views.addinitinfo), #初始化信息提交
    url('add_stuinits/', views.add_stuinits), #学生信息提交
    url('add_groupsinitinfo/', views.add_groupsinitinfo), #小组信息提交
    url('displaystu/', views.displaystu), #预览文件
    url('displaydata/', views.displaydata), #预览上传学习文件
    url('dataview/', views.dataview),  # 数据可视化
    url('displaygroup/', views.displaygroup), #预览文件
    url('groupdetail/', views.groupdetail), #小组详情
    url('login/', views.login),
    url('stutask/', views.stutask),#显示学生界面
    url('check_file/', views.check_file),#检察员-审核文件
    url('check_file_content/', views.check_file_content),#检察员-预览文件
    url(r'^reviewpass/', views.reviewpass),#检察员-文件通过审核
    url('memberinfo/', views.memberinfo),#组长界面-显示成员信息
    url('leader_taskmanage/', views.leader_taskmanage),#组长界面-任务管理界面
    url('grouptalk/', views.group_chat),  # 讨论区
    url('send_notice/', views.send_notice),#组长-消息提醒提交
    url('member_taskmanage/', views.member_taskmanage),#除组长角色外的任务管理界面
    url('submitdoc/', views.submitdoc),#组员提交任务
    url('showsubmit/', views.showsubmit),#组员查看已提交任务
    url(r'^readfile/', views.readfile),#预览文件
    url(r'^readfiles/', views.readfiles),#下载预览多个文件
    url('leader_taskchange/', views.leader_taskchange),#组长界面-任务修改
    url('leader_taskadd/', views.leader_taskadd),#组长界面-任务添加
    url('getstuinfo/', views.getstuinfo),#组长界面-任务添加信息查询
    url('calendar_check/', views.calendar_check),#组长界面-日历查看
    url('stu_eva/', views.stu_eva),  #学生自评
    url('group_eva/', views.group_eva),  #小组评价
    url('diff_eva/', views.diff_eva),  #组间互评
    url('mem_eva/', views.mem_eva),  #成员互评
    url('teacher_eva/', views.teacher_eva),  #成员互评
    url('addstueva/', views.addstueva),  #提交评价
    url('modifystueva/', views.modifystueva),  #修改评价
    url('enter_talking/', views.enter_talking),#教师界面-进入小组讨论区
    url('mark_assess/', views.mark_assess),#教师界面-成绩评分
    url('submitfinalscore/', views.submitfinalscore),#教师界面-提交小组综合成绩
    url('upload_stuscore/', views.upload_stuscore),#教师界面-上传学生成绩文件
    url('uploadselfscore/', views.uploadselfscore),#教师界面-提交学生个人成绩
    url('stuchat/', views.stuchat),
    url('stucalls/', views.stucalls),
    url('stucontacts/', views.stucontacts),
    url('statistics/', views.statistics),
    url(r'^stu_list/$', views.stu_list),
    url(r'^task_list/$', views.task_list),
    url(r'^doc_list/$', views.doc_list),
    url(r'^notice_list/$', views.notice_list),
    url(r'^feedback_list/$', views.feedback_list),
    url(r'^feedback_doclist/$', views.feedback_doclist),
    url(r'^systeminit/$', views.systeminit),
    url(r'^learn_manage/$', views.learn_manage),
    url(r'^groupinfo/$', views.groupinfo),
    url('newgroup/', views.newgroup),
    url('userpower/', views.userpower),
    url('newuser/', views.newuser),
    url('newtask/', views.newtask),
    url('newtask_stu/', views.newtask_stu),
    url('ste/', views.ste),
    url('re/', views.re),
    url('learn_new/', views.learn_new),
    url('pjgl/', views.pjgl),
    url('maxpjid/', views.maxpjid),
    url('pj-tijiao/', views.pjtijiao),
    url('bms_eva/', views.bms_eva),
    url('delete_stu/', views.delete_stu),
    url('delete_user/', views.delete_user),
    url('delete_feedback/', views.delete_feedback),
    url('delete_feedbackfile/', views.delete_feedbackfile),
    url('delete_task/', views.delete_task),
    url('delete_doc/', views.delete_doc),
    url('delete_notice/', views.delete_notice),
    url('delete_group/', views.delete_group),
    url('delete_chat_id/', views.delete_chat_id),
    url('delete_alltalk/', views.delete_alltalk),
    url('delete_initfile/', views.delete_initfile),
    url('delete_learn/', views.delete_learn),
    url('newstuinfo/', views.newstuinfo),
    url('newuserinfo/', views.newuserinfo),
    url('newgroupinfo/', views.newgroupinfo),
    url('newlearninfo/', views.newlearninfo),
    url('changestuinfo/', views.changestuinfo),
    url('changeuserinfo/', views.changeuserinfo),
    url('changegroupinfo/', views.changegroupinfo),
    url('sbi/', views.sbi),
    url('sbc/', views.sbc),
    url('sbg/', views.sbg),
    url('student_edit/', views.student_edit),
    url('user_edit/', views.user_edit),
    url('task_edit/', views.task_edit),
    url('learn_edit/', views.learn_edit),
    url('edit_userinfo/', views.edit_userinfo),
    url('edit_password/', views.edit_password),
    url('pwd_edit/', views.pwd_edit),
    url('notice_edit/', views.notice_edit),
    url('query_task/', views.query_task),
    url('query_learn/', views.query_learn),
    url('query_notice/', views.query_notice),
    url('group_edit/', views.group_edit),
    url('bms/', views.bms),
    url('welcome/', views.welcome),
    url('pjbz/', views.pjbz),
    url('pj/', views.pj),
    url('pjquery/', views.pjquery),
    url('query_stu/', views.query_stu),
    url('bms_addtask/', views.bms_addtask),
    url('bms_edittask/', views.bms_edittask),
    url('bms_editlearn/', views.bms_editlearn),
    url('bms_editnotice/', views.bms_editnotice),
    url('bms_readfile/', views.bms_readfile),
    url('reg/', views.reg),
    url(r'^search-form/$', search.search_form),
    url(r'^search-post/$', search2.search_post),
    url(r'^admin/', admin.site.urls),
    url(r'^search/$', search.search),
    url('talk_manage/', views.talk_manage),
    url('export_talk/', views.export_talk),
    url('get_file/', views.get_file),
    url('dp_talkdata/', views.dp_talkdata),
]
