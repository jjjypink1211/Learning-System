import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from TestModel.models import GroupChat
from django.db.models import Avg,Max,Min,Count,Sum  #   引入函数
import datetime


class ChatConsumer(WebsocketConsumer):
    # websocket建立连接时执行方法
    def connect(self):
        # 从url里获取聊天室名字，为每个房间建立一个频道组
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name


        # 将当前频道加入频道组
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        # 接受所有websocket请求
        self.accept()

    # websocket断开时执行方法
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # 从websocket接收到消息时执行函数
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        type=text_data_json['type']
        if type == 'msg':
            message = text_data_json['message']
            stu_info = text_data_json['stu_info']
            if 'power' in stu_info:
                group_id=stu_info['group_id']
                send_num = stu_info['num']
                send_name = stu_info['power']

            else:
                group_id = stu_info['group_id']
                send_num = stu_info['num']
                send_name = stu_info['name']
            send_content = message
            send_type = '1'
            send_time = datetime.datetime.now()
            datetime_str = send_time.strftime('%H:%M')
            newmsg = GroupChat(
                    group_id=group_id,
                    send_num=send_num,
                    send_content=send_content,
                    send_type=send_type,
                    send_time=send_time
            )
            newmsg.save()
            # 发送消息到频道组，频道组调用chat_message方法
            async_to_sync(self.channel_layer.group_send)(
               self.room_group_name,
                {
                    'type': 'chat_message',
                    'msg_type': 'msg',
                     'message': message,
                    'stu_info': stu_info
                }
            )
        elif type == 'file':
            stu_info = text_data_json['stu_info']
            if 'power' in stu_info:
                group_id = stu_info['group_id']
                send_num = stu_info['num']
                send_name = stu_info['power']

            else:
                group_id = stu_info['group_id']
                send_num = stu_info['num']
                send_name = stu_info['name']
            send_type = '2'#表示文件
            file_info = text_data_json['files']
            send_time = datetime.datetime.now()
            datetime_str = send_time.strftime('%H:%M')
            max_id = GroupChat.objects.all().aggregate(Max('id'))
            max_id['id__max'] = max_id['id__max'] + 1
            id=max_id['id__max']
            for file in file_info:
                newmsg = GroupChat(
                    group_id=group_id,
                    send_num=send_num,
                    send_content=file['file_path'],
                    send_type=send_type,
                    send_time=send_time
                )
                newmsg.save()
         # 发送消息到频道组，频道组调用chat_message方法
            async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'msg_type': 'file',
                        'message': file_info,
                        'stu_info': stu_info,
                        'id':id
                    }
                )
    # 从频道组接收到消息后执行方法
    def chat_message(self, event):
        type=event['msg_type']
        if type == 'msg':
                message = event['message']
                stu_info=event['stu_info']
                send_num = stu_info['num']
                send_name = stu_info['name']
                send_time = datetime.datetime.now()
                datetime_str = send_time
                # 当天
                time = int(datetime_str.strftime('%H'))
                if time >= 0 and time < 6:
                    datetime_str = '凌晨' + datetime_str.strftime('%H:%M')
                elif time >= 6 and time <= 12:
                    datetime_str = '上午' + datetime_str.strftime('%H:%M')
                elif time > 12 and time <= 18:
                    datetime_str = '下午' + datetime_str.strftime('%H:%M')
                elif time > 18 and time < 24:
                    datetime_str = '晚上' + datetime_str.strftime('%H:%M')
                # 通过websocket发送消息到客户端
                self.send(text_data=json.dumps({
                    'message': f'{message}',
                    'user_num': send_num,
                    'user_name':send_name,
                    'time': datetime_str,
                    'type':type
                }))
        elif type == 'file':
                message = event['message']
                stu_info = event['stu_info']
                send_num = stu_info['num']
                send_name = stu_info['name']
                id = event['id']
                send_time = datetime.datetime.now()
                datetime_str = send_time
                # 当天
                time = int(datetime_str.strftime('%H'))
                if time >= 0 and time < 6:
                    datetime_str = '凌晨' + datetime_str.strftime('%H:%M')
                elif time >= 6 and time <= 12:
                    datetime_str = '上午' + datetime_str.strftime('%H:%M')
                elif time > 12 and time <= 18:
                    datetime_str = '下午' + datetime_str.strftime('%H:%M')
                elif time > 18 and time < 24:
                    datetime_str = '晚上' + datetime_str.strftime('%H:%M')
                # 通过websocket发送消息到客户端
                self.send(text_data=json.dumps({
                    'message': message,
                    'user_num': send_num,
                    'user_name': send_name,
                    'time': datetime_str,
                    'type': type,
                    'id':id
                }))