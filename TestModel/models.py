#models.py
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

class User(models.Model): #用户信息表
    id =models.AutoField(primary_key=True)

    num=models.CharField(max_length=11)

    pwd=models.CharField(max_length=32)

    power=models.CharField(max_length=16)

    name= models.CharField(max_length=32)

    email= models.CharField(max_length=32,default="xxxxxxxx")

    phone = models.CharField(max_length=13, default="xxxxxxxx")
class UserGroup(models.Model): #小组名单表
    id = models.AutoField(primary_key=True)

    group_id = models.IntegerField(verbose_name="小组编号", null=False)

    topic = models.CharField(max_length=255, null=False, verbose_name="学习主题")

    group_score = models.FloatField(
        default=0,  # 设置默认值为0
        validators=[
            MaxValueValidator(100),  # 限定存储的最大值为100
            MinValueValidator(0)
        ]  # 限定存储的最小值为1
    )
class Student(models.Model):  #学生基本信息表
    id =models.AutoField(primary_key=True)

    num=models.CharField(max_length=11,verbose_name="学生学号",null=False,unique=True)

    name=models.CharField(max_length=32,null=False,verbose_name="学生姓名")

    grade=models.CharField(max_length=16,verbose_name="学生班级")

    score= models.FloatField(
        default=0,                      #设置默认值为0
        validators=[
            MaxValueValidator(100),   # 限定存储的最大值为100
            MinValueValidator(0)
                    ]    # 限定存储的最小值为1
        )
    group_id = models.IntegerField(verbose_name="小组编号", null=False)

    group_role=models.CharField(max_length=32,verbose_name="组内角色")

    models.ForeignKey("UserGroup", to_field="group_id",default=1, on_delete=models.CASCADE)


class Evaluate(models.Model):  #评价库
    id = models.AutoField(primary_key=True)

    evaluate_id = models.CharField(max_length=10,verbose_name="评价编号", null=False, unique=True)

    evaluate_type = models.CharField(max_length=16, null=False, verbose_name="评价类型")

    evaluate_item = models.CharField(max_length=55, null=False, verbose_name="评价项目")

    struct_type = models.IntegerField(null=False, verbose_name="结构类型",default=0)

    pub_time = models.DateTimeField(auto_now_add=True)

    evaluate_weight = models.IntegerField(verbose_name="评价权重", default=0)


class task(models.Model):  #任务清单表
    id = models.AutoField(primary_key=True,verbose_name="总编号")

    group_id = models.IntegerField(verbose_name="小组编号", null=False)

    num = models.CharField(max_length=11,verbose_name="学生学号",null=False)

    group_role = models.CharField(max_length=32,verbose_name="组内角色")

    task_id = models.IntegerField(verbose_name="任务编号", null=False, unique=True)

    task_type = models.CharField(max_length=3, verbose_name="任务类型")

    task_content = models.CharField(max_length=255,verbose_name="任务内容", null=False)

    start_time = models.DateField(verbose_name="上传时间")

    end_time = models.DateField(verbose_name="上传时间")

    is_finish =models.BooleanField(default=False,verbose_name="是否完成")

    is_overtime=models.BooleanField(default=False,verbose_name="是否超时")

    overtime_days = models.IntegerField(verbose_name="延迟天数",default=0)

    sub_id = models.CharField(max_length=16, verbose_name="父任务编号")

    models.ForeignKey("UserGroup", to_field="group_id", default=1, on_delete=models.CASCADE)

    models.ForeignKey("Student", to_field="num", default=1, on_delete=models.CASCADE)

class doc(models.Model):  #任务提交表
    id = models.AutoField(primary_key=True) #系统自动生成id

    group_id =  models.IntegerField(verbose_name="小组编号", null=False)

    num=models.CharField(max_length=11,verbose_name="学生学号",null=False)

    task_id = models.CharField(max_length=16,verbose_name="任务编号", null=False)

    filepub_time = models.DateTimeField(auto_now_add=True,verbose_name="上传时间")

    file_content=models.TextField(verbose_name="文件路径/文本", null=False)

    task_remark=models.CharField(max_length=255,verbose_name="文档备注")

    submit_type=models.CharField(max_length=10, verbose_name="上传类型")

    is_check = models.BooleanField(verbose_name="是否通过审核")

    file_type = models.CharField(max_length=6, verbose_name="文件类型")

    models.ForeignKey("UserGroup", to_field="group_id", default=1, on_delete=models.CASCADE)

    models.ForeignKey("Student", to_field="num", default=1, on_delete=models.CASCADE)



class feed_back(models.Model):  #学习反馈记录表
    id = models.AutoField(primary_key=True)

    feedback_id = models.CharField(max_length=16, verbose_name="反馈表编号",default="0000")

    group_id = models.IntegerField(verbose_name="小组编号", null=False)

    num=models.CharField(max_length=11,verbose_name="学生学号",null=False,default="stu_num")#发送者

    feedback_time = models.DateTimeField(auto_now_add=True, verbose_name="反馈时间")

    feedback_type = models.CharField(max_length=32, verbose_name="反馈类型")

    feedback_title = models.CharField(max_length=32, verbose_name="反馈标题",default="title")

    feedback_content = models.TextField(verbose_name="反馈内容", null=False)

    feedback_file = models.IntegerField(verbose_name="文件个数", null=False,default=0)

    models.ForeignKey("UserGroup", to_field="group_id", default=1, on_delete=models.CASCADE)

    models.ForeignKey("Student", to_field="num", default=1, on_delete=models.CASCADE)
class feedbackfile(models.Model):  #学习反馈记录表-文件
    id = models.AutoField(primary_key=True)

    feedback_id = models.IntegerField(verbose_name="反馈编号", null=False)

    file_path = models.CharField(max_length=255, verbose_name="反馈标题", default="title")

    models.ForeignKey("feed_back", to_field="feedback_id", default=1, on_delete=models.CASCADE)

class eva_recollect(models.Model):  #评论收集表
    id = models.AutoField(primary_key=True)

    pj_id = models.IntegerField(verbose_name="评价编号",default='0')

    eva_id = models.CharField(max_length=16, verbose_name="评价问卷编号")

    group_id = models.IntegerField(verbose_name="小组编号", null=False,default=0)

    eva_time = models.DateTimeField(auto_now_add=True, verbose_name="评价时间")

    eva_type = models.CharField(max_length=32, verbose_name="评价类型",default='尚未指定')

    form_type = models.CharField(max_length=6, verbose_name="问卷结构类型",null=False,default='0')

    act_name = models.CharField(max_length=64, verbose_name="活动名称(小组学习名称)")

    valuer_num = models.CharField(max_length=32, verbose_name="评价者学号",default='00000000')

    beeva_num = models.CharField(max_length=32, verbose_name="被评价者学号/被评价小组编号",default='无')

    eva_content = models.CharField(max_length=255, verbose_name="评价内容(根据问卷结构类型的不同而不同)(分值/时长/文本)",default='无')

    models.ForeignKey("Student", to_field="valuer_num", default=1, on_delete=models.CASCADE)
    models.ForeignKey("Evaluate", to_field="eva_id", default=1, on_delete=models.CASCADE)
    models.ForeignKey("Student", to_field="beeva_num", default=1, on_delete=models.CASCADE)
    models.ForeignKey("UserGroup", to_field="group_id", default=1, on_delete=models.CASCADE)

class learn_obj(models.Model):  #学习目标设置
    OBJ_choice = (
        (1, '总教学目标'),
        (2, '小组教学目标'),
    )
    id = models.AutoField(primary_key=True)

    obj_topic = models.CharField(max_length=255, verbose_name="教学主题", null=False)

    obj_content = models.CharField(max_length=255, verbose_name="教学目标", null=False)

    obj_time = models.DateTimeField(auto_now_add=True, verbose_name="目标时间")

    obj_author = models.CharField(max_length=16, verbose_name="作者")

    obj_type = models.CharField(max_length=2, verbose_name="目标类型",choices=OBJ_choice)
class init_info(models.Model):  #初始文件上传

    id = models.AutoField(primary_key=True)

    file_name = models.CharField(max_length=32, verbose_name="文件名称", null=False)

    file_path = models.CharField(max_length=255, verbose_name="文件路径", null=False)

    file_time = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")

    file_type = models.CharField(max_length=6, verbose_name="文件类型")
class notice(models.Model):  #通知栏
    id = models.AutoField(primary_key=True) #系统自动生成id

    send_num=models.CharField(max_length=11,verbose_name="学生学号",null=False)#发送者

    receive_num = models.CharField(max_length=11, verbose_name="学生学号", null=False)#接收者

    notice_title = models.CharField(max_length=255, verbose_name="通知标题")#通知标题

    notice_content=models.TextField(verbose_name="通知信息", null=False)

    notice_type=models.CharField(max_length=10, verbose_name="通知类型")

    notice_time = models.DateTimeField(auto_now_add=True,verbose_name="通知时间")

    models.ForeignKey("Student", to_field="send_num", default=1, on_delete=models.CASCADE)
    models.ForeignKey("Student", to_field="receive_num", default=1, on_delete=models.CASCADE)
class GroupChat(models.Model):  #群内聊天记录
    id = models.AutoField(primary_key=True) #系统自动生成id

    group_id = models.IntegerField(verbose_name="小组编号", null=False)

    send_num=models.CharField(max_length=11,verbose_name="学生学号",null=False)#发送者

    send_content=models.TextField(verbose_name="发送内容", null=False)#发送内容

    send_type = models.TextField(verbose_name="发送类型", null=False)  #发送类型 文字 音频 文件 图片

    send_time = models.DateTimeField(auto_now_add=True,verbose_name="发送时间")

    models.ForeignKey("Student", to_field="send_num", default=1, on_delete=models.CASCADE)
    models.ForeignKey("UserGroup", to_field="group_id", default=1, on_delete=models.CASCADE)
# Create your models here.
#以上的类名代表了数据库表名，且继承了models.Model，类里面的字段代表数据表中的字段(name)，
# 数据类型则由CharField（相当于varchar）、DateField（相当于datetime）， max_length 参数限定长度。