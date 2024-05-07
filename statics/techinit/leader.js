function displaymem(obj)
{
   //alert(obj.id)
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
   var num=obj.id;
    $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/memberinfo/" ,//url
            data: {'num': num,
            'csrfmiddlewaretoken': csrf},
            dataType: 'json',
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                    //将成员信息显示模态框中
                    //console.log(result.meminfo[0].fields['name'])
                    //document.getElementById("member_name").innerHTMl=result.meminfo[0].fields['name']
                    num=result.meminfo[0].fields['num'];//学生学号
                    $('#member_name').html(result.meminfo[0].fields['name']); //赋值
                    $('#position').html(result.meminfo[0].fields['group_role']); //赋值
                    $('#memclass ').html(result.meminfo[0].fields['grade']); //赋值
                    $('#email').html(result.user_info[0].email); //赋值
                    $('#phone').html(result.user_info[0].phone); //赋值
                    //构造任务列表
                    var b1=document.getElementById("member_task");//获得div标签
                    //清空数据
                   $("#member_task").html("");
                    var title=document.createElement('h5');
                    title.setAttribute("class","card-title");
                    title.innerHTML="任务列表";
                    b1.appendChild(title);
                    for(var i=0;i<result.taskinfo.length;i++)
                    {

                       task_id=result.taskinfo[i].fields['task_id'];
                       var div1=document.createElement('div');
                       div1.setAttribute("class","transactions-list");
                       b1.appendChild(div1);
                       var div2=document.createElement('div');
                       div2.setAttribute("class","tr-item");
                       div1.appendChild(div2);
                       var div3=document.createElement('div');
                       div3.setAttribute("class","tr-company-name");
                       div2.appendChild(div3);
                       var div5=document.createElement('div');
                       div5.setAttribute("class","tr-text");
                       div3.appendChild(div5);
                       var hh=document.createElement('h3');
                       hh.setAttribute("id",result.taskinfo[i].fields['task_id'])
                       hh.innerHTML=result.taskinfo[i].fields['task_content']
                       div5.appendChild(hh);
                        var pp=document.createElement('p');
                       pp.innerHTML=result.taskinfo[i].fields['start_time']+"--"+result.taskinfo[i].fields['end_time']
                       div5.appendChild(pp);
                       var div6=document.createElement('div');
                       div6.setAttribute("class","tr-rate");
                       div6.setAttribute("style","margin:50px");
                       div3.appendChild(div6);
                       var butt1=document.createElement('button');
                           var is_finish=result.taskinfo[i].fields['is_finish'];
                           var is_overtime=result.taskinfo[i].fields['is_overtime'];
                            if(is_finish && is_overtime)
                            {
                              //完成但超时
                              console.log('已完成');
                              butt1.setAttribute("type","button");
                              butt1.setAttribute("class","btn btn-success m-b-xs");
                              butt1.innerHTML="已完成";
                              var butt2=document.createElement('button');
                                butt2.setAttribute("type","button");
                                butt2.setAttribute("class","btn btn-warning m-b-xs");
                                butt2.innerHTML="超时"+Math.abs(parseInt(result.taskinfo[i].fields['overtime_days']))+'天提交';
                                div6.appendChild(butt2);
                            }else if(!is_finish && is_overtime)
                            {
                               //没完成也超时了
                                butt1.setAttribute("type","button");
                                butt1.setAttribute("class","btn btn-danger m-b-xs");
                                butt1.innerHTML="超时"+Math.abs(parseInt(result.taskinfo[i].fields['overtime_days']))+'天';
                                var butt2=document.createElement('button');
                                butt2.setAttribute("type","button");
                                butt2.setAttribute("class","btn btn-warning m-b-xs");
                                 butt2.setAttribute("id",num+"_"+task_id);
                                 butt2.setAttribute("onclick","notice_stu(this)");
                                butt2.innerHTML="提醒提交";
                                div6.appendChild(butt2);
                            }else if(is_finish && !is_overtime)
                            {
                               //完成 也没超时
                               butt1.setAttribute("type","button");
                               butt1.setAttribute("class","btn btn-success m-b-xs");
                               butt1.innerHTML="已完成";
                            }else
                            {
                                //没完成+没超时
                                butt1.setAttribute("type","button");
                                butt1.setAttribute("class","btn btn-warning m-b-xs");
                                butt1.setAttribute("onclick","notice_stu(this)");
                                butt1.setAttribute("id",num+"_"+task_id);
                                butt1.innerHTML="提醒提交";
                            }
                       div6.appendChild(butt1);

                    }
                }
                if(result.resultCode==-1){
                    alert(result.msg);

                }
            },
            error : function(xhr, textStatus, errorThrown) {
               /*错误信息处理*/
　　　　　　　　alert("进入error---");
　　　　　　　　alert("状态码："+xhr.status);
　　　　　　　　alert("状态:"+xhr.readyState);//当前状态,0-未初始化，1-正在载入，2-已经载入，3-数据进行交互，4-完成。
　　　　　　　　alert("错误信息:"+xhr.statusText );
　　　　　　　　alert("返回响应信息："+xhr.responseText );//这里是详细的信息
　　　　　　　　alert("请求状态："+textStatus); 　　　　　　　　
　　　　　　　　alert(errorThrown); 　　　　　　　　
　　　　　　　　alert("请求失败");
            }
        });
}
function showfiledetail(index)
{
  var tableId = document.getElementById("zero-conf");
  var csrf = $('input[name="csrfmiddlewaretoken"]').val();
   $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/check_file_content/" ,//url
            data: {'id':index,
            'csrfmiddlewaretoken': csrf},
            dataType: 'json',
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                     $('#text_content').val(result.file_content);
                }
                if(result.resultCode==-1){
                    alert(result.msg);
                }
            },
            error : function(xhr, textStatus, errorThrown) {
               /*错误信息处理*/
　　　　　　　　alert("进入error---");
　　　　　　　　alert("状态码："+xhr.status);
　　　　　　　　alert("状态:"+xhr.readyState);//当前状态,0-未初始化，1-正在载入，2-已经载入，3-数据进行交互，4-完成。
　　　　　　　　alert("错误信息:"+xhr.statusText );
　　　　　　　　alert("返回响应信息："+xhr.responseText );//这里是详细的信息
　　　　　　　　alert("请求状态："+textStatus); 　　　　　　　　
　　　　　　　　alert(errorThrown); 　　　　　　　　
　　　　　　　　alert("请求失败");
            }
        });

}
function reviewpass(index)
{
  var tableId = document.getElementById("zero-conf");
  var csrf = $('input[name="csrfmiddlewaretoken"]').val();
   $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/reviewpass/" ,//url
            data: {'id':index,
            'csrfmiddlewaretoken': csrf},
            dataType: 'json',
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                   alert(result.msg)

                }
                if(result.resultCode==-1){
                    alert(result.msg);
                }
            },
            error : function(xhr, textStatus, errorThrown) {
               /*错误信息处理*/
　　　　　　　　alert("进入error---");
　　　　　　　　alert("状态码："+xhr.status);
　　　　　　　　alert("状态:"+xhr.readyState);//当前状态,0-未初始化，1-正在载入，2-已经载入，3-数据进行交互，4-完成。
　　　　　　　　alert("错误信息:"+xhr.statusText );
　　　　　　　　alert("返回响应信息："+xhr.responseText );//这里是详细的信息
　　　　　　　　alert("请求状态："+textStatus); 　　　　　　　　
　　　　　　　　alert(errorThrown); 　　　　　　　　
　　　　　　　　alert("请求失败");
            }
        });

}
function notice_stu(obj)
{ //设置通知提醒
  notice_id=obj.id.split('_');
  receive_num= notice_id[0];
  task_id=notice_id[1];
  var csrf = $('input[name="csrfmiddlewaretoken"]').val();
  //console.log(receive_num);
 $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/send_notice/" ,//url
            data: {
            'receive_num':receive_num,
            'task_id': task_id,
            'csrfmiddlewaretoken': csrf},
            dataType: 'json',
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                   alert(result.msg)

                }
                if(result.resultCode==-1){
                    alert(result.msg);
                }
            },
            error : function(xhr, textStatus, errorThrown) {
               /*错误信息处理*/
　　　　　　　　alert("进入error---");
　　　　　　　　alert("状态码："+xhr.status);
　　　　　　　　alert("状态:"+xhr.readyState);//当前状态,0-未初始化，1-正在载入，2-已经载入，3-数据进行交互，4-完成。
　　　　　　　　alert("错误信息:"+xhr.statusText );
　　　　　　　　alert("返回响应信息："+xhr.responseText );//这里是详细的信息
　　　　　　　　alert("请求状态："+textStatus); 　　　　　　　　
　　　　　　　　alert(errorThrown); 　　　　　　　　
　　　　　　　　alert("请求失败");
            }
        });



}
Date.prototype.Format = function (fmt) { // author: meizz
  var o = {
    "M+": this.getMonth() + 1, // 月份
    "d+": this.getDate(), // 日
    "h+": this.getHours(), // 小时
    "m+": this.getMinutes(), // 分
    "s+": this.getSeconds(), // 秒
    "q+": Math.floor((this.getMonth() + 3) / 3), // 季度
    "S": this.getMilliseconds() // 毫秒
  };
  if (/(y+)/.test(fmt))
    fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
  for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
      return fmt;
}
