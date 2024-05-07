$("#num").change(function()
{
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var obj = document.getElementById("num"); //定位id
     var index = obj.selectedIndex; // 选中索引
     var stu_num = obj.options[index].value; // 选中值
     $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/getstuinfo/" ,//url
            data: {'stu_num':stu_num,'csrfmiddlewaretoken': csrf},
            dataType: 'json',
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                  document.getElementById("name").value=result.name;
                  document.getElementById("role").value=result.group_role;
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

})
$(function () {
    $('#taskadd').bootstrapValidator({
        message: 'This value is not valid',
        //提供输入验证图标提示
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            content: {
                message: '内容不能为空',
                validators: {
                    notEmpty: {
                        message: '内容不能为空'
                    },
                     stringLength: {
                         min: 6,
                         max: 255,
                         message: '内容长度必须在2到255之间'
                     },

                }
            },
            starttime: {
                message: '内容不能为空',
                validators: {
                    notEmpty: {
                        message: '日期不能为空'
                    },
                       date: {
                         format: 'YYYY/MM/DD',
                         message: '日期无效'
                       },

                }
            },
            endtime: {
                message: '日期不能为空',
                validators: {
                    notEmpty: {
                        message: '日期不能为空'
                    },
                       date: {
                         format: 'YYYY/MM/DD',
                         message: '日期无效'
                       },

                }
            },


        }
    })

});


function changetaskinfo()
{
  var td = event.srcElement; // 通过event.srcElement 获取激活事件的对象 td
  //alert("行号：" + (td.parentElement.rowIndex) + "，列号：" + td.cellIndex);
  var srows=td.parentElement.rowIndex;
  var scols=td.cellIndex;
  var tableId = document.getElementById("zero-conf");
  document.getElementById("stu_num").value=tableId.rows[srows].cells[scols-10].innerHTML
  document.getElementById("stu_name").value=tableId.rows[srows].cells[scols-9].innerHTML
  document.getElementById("task_id").value=tableId.rows[srows].cells[scols-8].innerHTML
  document.getElementById("task_content").value=tableId.rows[srows].cells[scols-7].innerHTML
  console.log(typeof(tableId.rows[srows].cells[scols-4].innerHTML));
  document.getElementById("start_time").value=tableId.rows[srows].cells[scols-6].innerHTML
  document.getElementById("end_time").value=tableId.rows[srows].cells[scols-5].innerHTML
  var all_options = document.getElementById("task_type").options;
  var optionID=tableId.rows[srows].cells[scols-4].innerHTML;
  for (i=0; i<all_options.length; i++)
    {
          if (all_options[i].innerHTML == optionID)  // 根据option标签的ID来进行判断  测试的代码这里是两个等号
            {
               all_options[i].selected = true;
            }
      }
  var all_options = document.getElementById("sub_id").options;
  var optionID=tableId.rows[srows].cells[scols-1].innerHTML;
  for (i=0; i<all_options.length; i++)
    {
          if (all_options[i].innerHTML == optionID)  // 根据option标签的ID来进行判断  测试的代码这里是两个等号
            {
               all_options[i].selected = true;
            }
      }

}
$("#submit_type").change(function()
{
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    var obj = document.getElementById("submit_type"); //定位id
     var index = obj.selectedIndex; // 选中索引
     var type = obj.options[index].value; // 选中值
     if(type==1)
     {
       var textarea1=document.createElement("textarea");
       var div1=document.getElementById("submit_there");
       $("#submit_there").html("");
       var label1=document.createElement("label");
       label1.setAttribute("class","form-label");
       label1.innerHTML="请填写文本";
       textarea1.setAttribute("id","submit_text");
       textarea1.setAttribute("class","form-control");
       div1.append(label1);
       div1.append(textarea1);

     }if(type==2)
     {
       var input1=document.createElement("input");
       var div1=document.getElementById("submit_there");
       $("#submit_there").html("");
       var label2=document.createElement("label");
       label2.setAttribute("class","form-label");
       label2.innerHTML="选择提交文件"
       input1.setAttribute("id","submit_file");
       input1.setAttribute("type","file");
       input1.setAttribute("class","form-control");
       div1.append(label2);
       div1.append(input1);
     }

})
function submittask()
{
  var td = event.srcElement; // 通过event.srcElement 获取激活事件的对象 td
  //alert("行号：" + (td.parentElement.rowIndex) + "，列号：" + td.cellIndex);
  var srows=td.parentElement.rowIndex;
  var scols=td.cellIndex;
  var tableId = document.getElementById("zero-conf");
  document.getElementById("task_id").value=tableId.rows[srows].cells[scols-9].innerHTML
  document.getElementById("task_content").value=tableId.rows[srows].cells[scols-8].innerHTML
  console.log(typeof(tableId.rows[srows].cells[scols-5].innerHTML));

}
function tasktijiao()
{
     //ajax上传文件必须通过Formdata对象传输数据
     var formdata=new FormData();
     var csrf = $('input[name="csrfmiddlewaretoken"]').val();
     var task_id=$("input[name='task_id']").val();//任务编号
     var obj = document.getElementById("submit_type"); //定位id
     var index = obj.selectedIndex; // 选中索引
     var submit_type = obj.options[index].value; // 选中值
     var task_remark=$("textarea[name='task_remark']").val();//任务备注
     if(task_remark== null || task_remark == "" )
     {
        task_remark="无";
     }
     if( submit_type==1)
     {
         //文本
         text_content=$("textarea[name='submit_text']").val();
         console.log(text_content);
         console.log(submit_type);
           formdata.append('task_id',task_id);
           formdata.append('file_content',text_content);
           //上传时间
           var time=new Date().format("yy/MM/dd hh:mm:ss");
           formdata.append('filepub_time',time);//上传时间
           formdata.append('file_content',text_content);
           formdata.append('submit_type',submit_type);
           formdata.append('is_check',false);
           formdata.append('task_remark',task_remark);
           formdata.append('csrfmiddlewaretoken',csrf);
     }else
     {
       //文件
        //获取上传文件对象(文件句柄):定位对象，转成DoM对象，取值（文件对象列表)
           var stufile=$('#submit_file')[0].files[0];
           formdata.append('task_id',task_id);
           formdata.append('file_content',stufile);
           //上传时间
           var time=new Date().format("yy/MM/dd hh:mm:ss");
           formdata.append('filepub_time',time);//上传时间
           formdata.append('submit_type',submit_type);
           formdata.append('is_check',false);
           formdata.append('task_remark',task_remark);
           formdata.append('csrfmiddlewaretoken',csrf);
     }
     $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/submitdoc/" ,//url
            data: formdata,
            dataType: 'json',
            processData:false,
            contentType:false,
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                    alert(result.msg);
                    location.reload();

                }
                if(result.resultCode==-1){
                    alert(result.msg);
                    //location.reload();
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
function showsubmit()
{
  var td = event.srcElement; // 通过event.srcElement 获取激活事件的对象 td
  //alert("行号：" + (td.parentElement.rowIndex) + "，列号：" + td.cellIndex);
  var srows=td.parentElement.rowIndex;
  var scols=td.cellIndex;
  var tableId = document.getElementById("zero-conf");
  var task_id=tableId.rows[srows].cells[scols-8].innerHTML;
  var csrf = $('input[name="csrfmiddlewaretoken"]').val();
  $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/showsubmit/" ,//url
            data: {'task_id':task_id,
            'csrfmiddlewaretoken': csrf},
            dataType: 'json',
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                    //alert(result.msg);
                     var data_tbody=document.getElementById("submitdata");
                     $('#submitdata').html("");
                    for(var i=0;i<result.check_list.length;i++)
                    {
                          var new_tr=document.createElement('tr');
                          var content_td=document.createElement('td');
                          content_td.setAttribute("style","white-space:nowrap;  overflow:hidden;text-overflow: ellipsis;")
                          if(result.check_list[i].submit_type=='1')
                          {
                             content_td.innerHTML=result.check_list[i].file_content;

                          }else
                           {
                              file_puth=result.check_list[i].file_content;
                              file_puth=file_puth.split('\\');
                              content_td.innerHTML=file_puth[file_puth.length-1];
                           }
                          new_tr.appendChild(content_td);
                          var time_td=document.createElement('td');
                          time_td.innerHTML=result.check_list[i].filepub_time;
                          new_tr.appendChild(time_td);
                          var remark_td=document.createElement('td');
                          remark_td.innerHTML=result.check_list[i].task_remark;
                          new_tr.appendChild(remark_td);
                          if(result.check_list[i].submit_type=='1')
                          {
                              var subtype_td=document.createElement('td');
                              subtype_td.setAttribute("value",result.check_list[i].submit_type);
                              subtype_td.setAttribute("type","button");
                              subtype_td.setAttribute("class","btn btn-warning");

                              subtype_td.innerHTML="文本";
                              new_tr.appendChild(subtype_td);
                          }else
                          {
                             var subtype_td=document.createElement('td');
                             subtype_td.setAttribute("value",result.check_list[i].submit_type);
                               subtype_td.setAttribute("type","button");
                              subtype_td.setAttribute("class","btn btn-info");

                              subtype_td.innerHTML="文件";
                              new_tr.appendChild(subtype_td);
                          }
                          var filetype_td=document.createElement('td');
                          filetype_td.innerHTML=result.check_list[i].file_type;
                          new_tr.appendChild(filetype_td);

                              if(result.check_list[i].submit_type=='1')
                              {
                                     var button_td=document.createElement('td');
                                     button_td.setAttribute("type","button");
                                      button_td.setAttribute("class","btn btn-warning");
                                      button_td.setAttribute("data-bs-toggle","modal");
                                      button_td.setAttribute("data-bs-target","#filedetail");
                                      button_td.setAttribute("onclick","showfiledetail()");
                                     button_td.innerHTML="预览";
                                     new_tr.appendChild(button_td);
                               }else
                               {
                                    var a_td=document.createElement('a');
                                    a_td.setAttribute("type","button");
                                    a_td.setAttribute("class","btn btn-warning");
                                    a_td.setAttribute("href","/readfile/?file_id="+result.check_list[i].id);
                                    a_td.innerHTML="下载查看";
                                    new_tr.appendChild(a_td);
                               }

                              data_tbody.appendChild(new_tr);
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
function showfiledetail()
{
 var td = event.srcElement; // 通过event.srcElement 获取激活事件的对象 td
  //alert("行号：" + (td.parentElement.rowIndex) + "，列号：" + td.cellIndex);
  var srows=td.parentElement.rowIndex;
  var scols=td.cellIndex;
  var tableId = document.getElementById("showsubmits");
  var submit_type=tableId.rows[srows].cells[scols-2].innerHTML;//上传类型
  var file_content=tableId.rows[srows].cells[scols-5].innerHTML;//文件内容
  var csrf = $('input[name="csrfmiddlewaretoken"]').val();
  if(submit_type=='文本')
  {
     $('#text_content').val(file_content);

  }else if(submit_type=='文件')
  {


  }
}
function submitinfo()
{
     var csrf = $('input[name="csrfmiddlewaretoken"]').val();
     var stu_num=$("input[name='stu_num']").val();
     var task_id=$("input[name='task_id']").val();
     var task_content=$("input[name='task_content']").val();
     var start_time=$("input[name='start_time']").val();
     console.log(start_time);
     var end_time=$("input[name='end_time']").val();
     console.log(end_time);
     var obj = document.getElementById("task_type"); //定位id
     var index = obj.selectedIndex; // 选中索引
     var task_type = obj.options[index].value; // 选中值
     var obj1 = document.getElementById("sub_id"); //定位id
     var index1 = obj1.selectedIndex; // 选中索引
     var sub_id = obj1.options[index1].value; // 选中值
     console.log(stu_num+task_content+ task_type+sub_id);
      $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/leader_taskchange/" ,//url
            data: {'stu_num':stu_num,'task_id':task_id,
            'task_content':task_content,'start_time':start_time,'end_time':end_time,'task_type':task_type,
            'sub_id': sub_id,
            'csrfmiddlewaretoken': csrf},
            dataType: 'json',
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                    alert(result.msg);
                    location.reload();
                }
                if(result.resultCode==-1){
                    alert(result.msg);
                    location.reload();
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
function addtaskinfo()
{
     var csrf = $('input[name="csrfmiddlewaretoken"]').val();
     var obj = document.getElementById("num"); //定位id
     var index = obj.selectedIndex; // 选中索引
     var num = obj.options[index].value; // 选中值
     var role=$("input[name='role']").val();
     var task_id=$("input[name='tasks_id']").val();
      var content=$("input[name='content']").val();
     var starttime=$("input[name='starttime']").val();
     var endtime=$("input[name='endtime']").val();
     //判断时间
     var start_time=starttime.toString().split("-");
     month=parseInt(start_time[1]);
     month=month-1;
     start_time[1]=month.toString();
     var sttime=new Date(start_time[0],start_time[1],start_time[2]);
     var end_time=endtime.toString().split("-");
     month=parseInt(end_time[1]);
     month=month-1;
     end_time[1]=month.toString();
     console.log(start_time)
     console.log(end_time)
     var entime=new Date(end_time[0],end_time[1],end_time[2]);
     var myDate = new Date();
      if(sttime.getTime() > entime.getTime()){
                alert("开始的时间不能比结束的时间还要晚！");
                return;
      }else if(myDate.getTime() > entime.getTime())
      {
           alert("结束的时间不能早于现在的时间！");
           return;
      }else if(myDate.getTime() > sttime.getTime())
      {
               alert("开始的时间不能早于现在的时间！");
               return;
      }
     var obj = document.getElementById("tasktype"); //定位id
     var index = obj.selectedIndex; // 选中索引
     var tasktype = obj.options[index].value; // 选中值
     var obj1 = document.getElementById("subid"); //定位id
     var index1 = obj1.selectedIndex; // 选中索引
     var subid = obj1.options[index1].value; // 选中值
     console.log(num+content+tasktype+subid);
      $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/leader_taskadd/" ,//url
            data: {
            'stu_num':num,
            'group_role':role,
            'task_id':task_id,
            'task_content': content,
            'start_time':starttime,
            'end_time': endtime,
            'task_type':tasktype,
            'sub_id': subid,
            'csrfmiddlewaretoken': csrf},
            dataType: 'json',
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                    alert(result.msg);
                    location.reload();
                }
                if(result.resultCode==-1){
                    alert(result.msg);
                    location.reload();
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
// 说明：JS时间Date格式化参数
// 参数：格式化字符串如：'yyyy-MM-dd hh:mm:ss'
// 结果：如2016-06-01 10:09:00
Date.prototype.format = function (fmt) {
    var o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), // 季度
        "S": this.getMilliseconds() // 毫秒
    };

    // 根据y的长度来截取年
    if (/(y+)/.test(fmt)){
	fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    }
    for (var k in o){
	if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    }
    return fmt;
}