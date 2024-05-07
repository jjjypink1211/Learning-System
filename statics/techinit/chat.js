       // 获取房间名
        const roomName = JSON.parse(document.getElementById('room-name').textContent);

        // 根据roomName拼接websocket请求地址，建立长连接
        //  请求url地址为/ws/chat/<room_name>/
        const wss_protocol = (window.location.protocol == 'https:') ? 'wss://': 'ws://';
        const chatSocket = new WebSocket(
             wss_protocol + window.location.host + '/ws/chat/'  + roomName + '/'
             );

        // 建立websocket连接时触发此方法，展示欢迎提示
        chatSocket.onopen = function(e) {
             document.getElementById('group_title').innerHTML = ('[公告]欢迎来到' +"第"+ roomName +"组"+ '讨论群。请文明发言!\n')
         }

        // 从后台接收到数据时触发此方法
        // 接收到后台数据后对其解析，并加入到聊天记录chat-log
         chatSocket.onmessage = function(e) {
             const data = JSON.parse(e.data);
             console.log(data);
             var num=data.user_num;
              var name=data.user_name;
              var type=data.type
             const user_num=JSON.parse(document.getElementById('stu_info').textContent)[0].num;
             if(type=='msg')
             {
                 if(user_num==num)
                 {
                   user_name=JSON.parse(document.getElementById('stu_info').textContent)[0].name;
                   var user_li=document.createElement('li');
                   user_li.setAttribute("class","message sent");
                   var div_opt=document.createElement('div');
                   div_opt.setAttribute("class","message__options");
                   var icon_i=document.createElement('i');
                   icon_i.setAttribute("class","mdi mdi-dots-horizontal");
                   div_opt.appendChild(icon_i);
                   user_div1=document.createElement('div');
                   user_div1.setAttribute("class","message__text");
                   user_div1.innerHTML=data.message;
                   user_div2=document.createElement('div');
                   user_div2.setAttribute("class","metadata")
                   user_span=document.createElement('span');
                   user_span.setAttribute("class","time");
                   user_span.innerHTML=data.time;
                   user_div3=document.createElement('div');
                   user_div3.setAttribute("class","user-avatar user-avatar-rounded")
                   user_div4=document.createElement('div');
                   user_div4.setAttribute("class","user-avatar user-avatar-rounded avatar-info")
                   user_span2=document.createElement('span');
                   user_span2.innerHTML=user_name;
                   user_div4.appendChild( user_span2);
                   user_div3.appendChild(user_div4);
                   user_div2.appendChild(user_span);
                   user_div1.appendChild(user_div2);
                   user_li.appendChild(user_div1);
                   user_li.appendChild(div_opt);
                   user_li.appendChild(user_div3);
                   var ul=document.getElementById('group_talk');
                   ul.appendChild(user_li);
                 }else
                 {
                   var user_li=document.createElement('li');
                   user_li.setAttribute("class","message received");
                   var div_opt=document.createElement('div');
                   div_opt.setAttribute("class","message__options");
                   var icon_i=document.createElement('i');
                   icon_i.setAttribute("class","mdi mdi-dots-horizontal");
                   div_opt.appendChild(icon_i);
                   user_div1=document.createElement('div');
                   user_div1.setAttribute("class","message__text");
                   user_div1.innerHTML=data.message;
                   user_div2=document.createElement('div');
                   user_div2.setAttribute("class","metadata");
                   user_div3=document.createElement('div');
                   user_div3.setAttribute("class","user-avatar user-avatar-rounded avatar-info")
                   user_div3.setAttribute("style","margin-right: 0px ;height:50px;width:50px")
                   user_span1=document.createElement('span');
                   user_span1.innerHTML=name;
                   user_div3.appendChild(user_span1);
                   user_span=document.createElement('span');
                   user_span.setAttribute("class","time");
                   user_span.innerHTML=data.time;
                   user_div2.appendChild(user_span);
                   user_div1.appendChild(user_div2);
                   user_li.appendChild(user_div3);
                   user_li.appendChild(user_div1);
                   user_li.appendChild(div_opt);
                   var ul=document.getElementById('group_talk');
                   ul.appendChild(user_li);
                 }
              }else if(type=='file')
              {
                 for(var i=0;i<data.message.length;i++)
                 {
                    var file_type=data.message[i].file_type;
                    var file_size=data.message[i].fsize;
                    var file_name=data.message[i].file_name;
                    if(file_type=='pdf')
                    {
                       showfile("iconbox__icon mdi mdi-file-pdf-box"
                       ,"docicon iconbox btn-solid-danger",file_size,file_name,data.time,user_num,num,data.id);

                    }
                    else if(file_type=='xls'||file_type=='xlsx' )
                    {
                      showfile("iconbox__icon mdi mdi-file-excel-box",
                      "docicon iconbox btn-solid-success",file_size,file_name,data.time,user_num,num,data.id);
                    }
                    else if(file_type=='doc'||file_type=='docx')
                    {
                         showfile("iconbox__icon mdi mdi-file-word-box",
                         "docicon iconbox btn-solid-info",file_size,file_name,data.time,user_num,num,data.id);
                    }
                    else if(file_type=='pptx')
                    {
                      showfile("iconbox__icon mdi mdi-file-powerpoint-box",
                      "docicon iconbox btn-solid-warning",file_size,file_name,data.time,user_num,num,data.id);
                    }
                    else
                    {
                      showfile("iconbox__icon mdi mdi-file-word-box",
                         "docicon iconbox btn-solid-info",file_size,file_name,data.time,user_num,num,data.id);

                    }




                 }



              }
            var div = document.getElementById('scrolldiv');
            div.scrollTop = div.scrollHeight;
             //document.getElementById('chat-log').innerHTML += (data.message + '\n');
         };

         // websocket连接断开时触发此方法
         chatSocket.onclose = function(e) {
             console.error('Chat socket closed unexpectedly');
         };

         document.querySelector('#chat-message-input').focus();
         document.querySelector('#chat-message-input').onkeyup = function(e) {
             if (e.keyCode === 13) {  // enter, return
                 document.querySelector('#chat-message-submit').click();
             }
         };

         // 每当点击发送消息按钮，通过websocket的send方法向后台发送信息。
         document.querySelector('#chat-message-submit').onclick = function(e) {
              var obj = document.getElementById("xFile");
                 if(obj.files.length!=0)
                 {
                       //console.log(obj.files.length);
                       //提交文件
                       var formdata=new FormData();
                       var fileList=[];
                       for (var i = 0; i < obj.files.length; i++)
                         {
                             fileList.push(obj.files[i]);
                         }
                         fileList.forEach(function (file) {
                                formdata.append('groupmsg_file', file, file.name);
                          });

                          stu=JSON.parse(document.getElementById('stu_info').textContent)[0];
                           formdata.append('group_id',stu.group_id);
                           formdata.append('num',stu.num);
                           formdata.append('name',stu.name);
                           formdata.append('type','2');
                         //注意这里:先把文本数据转成json格式,然后调用send方法发送。
                        $.ajax({
                        //几个参数需要注意一下
                            type: "POST",//方法类型
                            url: "/grouptalkfile/" ,//上传小组文件
                            data: formdata,
                            processData:false,
                            contentType:false,
                            success: function (result) {
                                console.log(result)
                                if (result.resultCode == 200) {
                                var inputdiv = document.querySelector('#chat-message-input');
                                inputdiv.value = '';
                                chatSocket.send(JSON.stringify({
                                            'files': result.file_info,
                                            'stu_info':stu,
                                            'type':'file'
                                        }));

                                }
                                if(result.resultCode==-1){
                                    alert(result.msg);
                                }
                            },
                            error : function() {
                                alert("异常！");
                            }
                        });

                 }
                 else
                 {
                     const messageInputDom = document.querySelector('#chat-message-input');
                     const message = messageInputDom.value;
                     const stu_info = JSON.parse(document.getElementById('stu_info').textContent)[0];//用户信息
                     //注意这里:先把文本数据转成json格式,然后调用send方法发送。
                     chatSocket.send(JSON.stringify({
                          'message': message,
                          'stu_info':stu_info,
                          'type':'msg'
                      }));
                     messageInputDom.value = '';
                 }
         };
function time_format(time)
{
  time=time.split(' ');
  time_ymd=time[0].split('-');
  time_hmd=time[1].split(':');
  var send_time = new Date(time_ymd[0], parseInt(time_ymd[1])-1 ,time_ymd[2], time_hmd[0], time_hmd[1], time_hmd[2]);
  var now=new Date();

	var difftime = (now - send_time)/1000; //计算时间差,并把毫秒转换成秒

	var days = parseInt(difftime/86400); // 天  24*60*60*1000
   	var hours = parseInt(difftime/3600)-24*days;    // 小时 60*60 总小时数-过去的小时数=现在的小时数
   	var minutes = parseInt(difftime%3600/60); // 分钟 -(day*24) 以60秒为一整份 取余 剩下秒数 秒数/60 就是分钟数
   	var seconds = parseInt(difftime%60);  // 以60秒为一整份 取余 剩下秒数

   	alert("时间差是: "+days+"天, "+hours+"小时, "+minutes+"分钟, "+seconds+"秒");
  console.log(now);
  console.log(send_time);
 console.log(now-send_time);

}
function change()
{
        var obj = document.getElementById("xFile");

        var len = obj.files.length;
        var fileName="";
        for (var i = 0; i < len; i++) {
            var path =obj.files[i].name;
            fileName=path+","+fileName;
        }
        document.getElementById("chat-message-input").value=fileName;
}
function showfile(icon_type,div_type,file_size,file_name,time,user_num,num,id)
{
                if(user_num==num)
                         {
                           user_name=JSON.parse(document.getElementById('stu_info').textContent)[0].name;
                           var user_li=document.createElement('li');
                           user_li.setAttribute("class","message sent");
                           var div_opt=document.createElement('div');
                           div_opt.setAttribute("class","message__options");
                           var icon_i=document.createElement('i');
                           icon_i.setAttribute("class","mdi mdi-dots-horizontal");
                           div_opt.appendChild(icon_i);
                           user_div1=document.createElement('div');
                           user_div1.setAttribute("class","message__text");
                           var file_div1=document.createElement('div');
                           file_div1.setAttribute("class","doclist");
                           var file_div2=document.createElement('div');
                           file_div2.setAttribute("class",div_type);
                           var file_icon=document.createElement('i');
                           file_icon.setAttribute("class",icon_type);
                           file_icon.setAttribute("onclick","downloadfile("+id+","+file_name+")");
                           file_div2.appendChild(file_icon);
                           var file_div3=document.createElement('div');
                           file_div3.setAttribute("class","doctitle");
                           var file_div4=document.createElement('div');
                           file_div4.setAttribute("class","docname");
                           file_div4.innerHTML=file_name;
                           var file_div5=document.createElement('div');
                           file_div5.setAttribute("class","docsize");
                           file_div5.innerHTML=file_size+'KB';
                           file_div3.appendChild(file_div4);
                           file_div3.appendChild(file_div5);
                           file_div1.appendChild(file_div2);
                           file_div1.appendChild(file_div3);
                           user_div2=document.createElement('div');
                           user_div2.setAttribute("class","metadata")
                           user_span=document.createElement('span');
                           user_span.setAttribute("class","time");
                           user_span.innerHTML=time;
                           user_div3=document.createElement('div');
                           user_div3.setAttribute("class","user-avatar user-avatar-rounded")
                           user_div4=document.createElement('div');
                           user_div4.setAttribute("class","user-avatar user-avatar-rounded avatar-info")
                           user_span2=document.createElement('span');
                           user_span2.innerHTML=user_name;
                           user_div4.appendChild( user_span2);
                           user_div3.appendChild(user_div4);
                           user_div2.appendChild(user_span);
                           user_div1.appendChild(file_div1);
                           user_div1.appendChild(user_div2);
                           user_li.appendChild(user_div1);
                           user_li.appendChild(div_opt);
                           user_li.appendChild(user_div3);
                           var ul=document.getElementById('group_talk');
                           ul.appendChild(user_li);
                         }else
                         {
                           var user_li=document.createElement('li');
                           user_li.setAttribute("class","message received");
                           var div_opt=document.createElement('div');
                           div_opt.setAttribute("class","message__options");
                           var icon_i=document.createElement('i');
                           icon_i.setAttribute("class","mdi mdi-dots-horizontal");
                           div_opt.appendChild(icon_i);
                           user_div1=document.createElement('div');
                           user_div1.setAttribute("class","message__text");
                           file_div1=document.createElement('div');
                           file_div1.setAttribute("class","doclist");
                           file_div2=document.createElement('div');
                           file_div2.setAttribute("class",div_type);
                           file_icon=document.createElement('i');
                           file_icon.setAttribute("class",icon_type);
                           file_icon.setAttribute("onclick","downloadfile("+id+","+file_name+")");
                           file_div2.appendChild(file_icon);
                           file_div3=document.createElement('div');
                           file_div3.setAttribute("class","doctitle");
                           file_div4=document.createElement('div');
                           file_div4.setAttribute("class","docname");
                           file_div4.innerHTML=file_name;
                           file_div5=document.createElement('div');
                           file_div5.setAttribute("class","docsize");
                           file_div5.innerHTML=file_size+'KB';
                           file_div3.appendChild(file_div4);
                           file_div3.appendChild(file_div5);
                           file_div1.appendChild(file_div2);
                           file_div1.appendChild(file_div3);
                           user_div2=document.createElement('div');
                           user_div2.setAttribute("class","metadata");
                           user_div3=document.createElement('div');
                           user_div3.setAttribute("class","user-avatar user-avatar-rounded avatar-info")
                           user_div3.setAttribute("style","margin-right: 0px ;height:50px;width:50px")
                           user_span1=document.createElement('span');
                           user_span1.innerHTML=name;
                           user_div3.appendChild(user_span1);
                           user_span=document.createElement('span');
                           user_span.setAttribute("class","time");
                           user_span.innerHTML=data.time;
                           user_div2.appendChild(user_span);
                           user_div1.appendChild(file_div1);
                           user_div1.appendChild(user_div2);
                           user_li.appendChild(user_div3);
                           user_li.appendChild(user_div1);
                           user_li.appendChild(div_opt);
                           var ul=document.getElementById('group_talk');
                           ul.appendChild(user_li);
                         }


}
function downloadfile(id,obj)
{
  var chat_id=id;
  var file_name=obj;
   var url="/dlgroupfile/?id="+chat_id+"&file_name="+file_name ;//下载文件
   window.location.href=url;
}