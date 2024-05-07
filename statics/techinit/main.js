function stutijiao() {
     var stu_num=$("input[name='stu_num']").val();
     var stu_name=$("input[name='stu_name']").val();
     var stu_grade=$("input[name='stu_grade']").val();
     var group_id=$('#stu_group').children('option:selected').val()
     console.log(group_id);
        $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/add_stuinits/" ,//url
            data: {'stu_num':stu_num,'stu_name':stu_name,'stu_grade':stu_grade,'group_id':group_id},
            dataType: 'json',
            success: function (result) {
                console.log(result);
                if (result.resultCode == 200) {
                    alert(result.msg);
                    location.reload();
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
function edituserinfo()
{
     var stu_num=$("input[name='stu_num']").val();
     var stu_name=$("input[name='stu_name']").val();
     var stu_grade=$("input[name='stu_grade']").val();
     var stu_phone=$("input[name='stu_phone']").val();
     var stu_email=$("input[name='stu_email']").val();
     if(stu_phone == "")
     {
       stu_phone = "xxxxxxxx";

     }
     if(stu_email == "")
     {
       stu_email = "xxxxxxxx";

     }
     $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/edit_userinfo/" ,//url
            data: {
            'stu_num':stu_num,
            'stu_name':stu_name,
            'stu_grade':stu_grade,
            'stu_phone':stu_phone,
            'stu_email':stu_email
            },
            dataType: 'json',
            success: function (result) {
                console.log(result);
                if (result.resultCode == 200) {
                    alert(result.msg);
                    location.reload();
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
function editpassword()
{
     var stu_num=$("input[name='stu_num']").val();
     var stu_name=$("input[name='stu_name']").val();
     var password=$("input[name='password']").val();
     var re_password=$("input[name='re_password']").val();
     if(password == "")
     {
       alert("请输入新密码！！！");
       return;
     }
     if(re_password == "")
     {
       alert("请再次输入新密码！！！");
       return;
     }
     if( password.length <= 6 || re_password.length <= 6 )
     {
       alert("密码长度需大于6个字符");
       return;
     }
     if(password !=  re_password )
     {
       alert("两次输入密码不同");
       return;
     }
     $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/pwd_edit/" ,//url
            data: {
            'stu_num':stu_num,
            'stu_name':stu_name,
            'password':password,
            },
            dataType: 'json',
            success: function (result) {
                if (result.resultCode == 200) {
                    alert(result.msg);
                    location.reload();
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
function group_tijiao() {
     var group_num=$("input[name='group_num']").val();
     var group_topic=$("input[name='group_topic']").val();
     console.log(group_topic)
        $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/add_groupsinitinfo/" ,//url
            data: {"group_num":group_num,"group_topic":group_topic},
            dataType: 'json',
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                    alert(result.msg);
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
function tijiao() {
     //ajax上传文件必须通过Formdata对象传输数据
     var formdata=new FormData();
     var csrf = $('input[name="csrfmiddlewaretoken"]').val();
     var obj_topic=$("input[name='obj_topic']").val();
     var obj_content=$("textarea[name='obj_content']").val();
     console.log(obj_content);
    //获取上传文件对象(文件句柄):定位对象，转成DoM对象，取值（文件对象列表)
    var stufile=$('#stu-file')[0].files[0];
    var groupfile=$('#group-file')[0].files[0];

    formdata.append('obj_topic',obj_topic);
    formdata.append('obj_content',obj_content);
    formdata.append('stufile',stufile);
    formdata.append('groupfile',groupfile);
    formdata.append('csrfmiddlewaretoken',csrf);
        $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/addinitinfo/" ,//url
            data: formdata,
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
                }
            },
            error : function() {
                alert("异常！");
            }
        });
    }
function displaystu()
{
var fileFlag=false
     $('#stu-file').each(function(){
     if($(this).val()!=""){
     fileFlag=true;
     }
     })
     if(!fileFlag)
     {
       alert("请选择好文件!")
       return;
     }
    var stufile=$('#stu-file')[0].files[0];
    var formdata=new FormData();
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    formdata.append('stufile',stufile);
    formdata.append('csrfmiddlewaretoken',csrf);
     $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/displaystu/" ,//url
            data: formdata,
            processData:false,
            contentType:false,
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                   //动态添加表单数据
                   var flag=0;
                   var row=result.rows;
                   var col=result.cols;
                   var stutable=document.getElementById("stulist");//获得table标签
                   for(var i=0;i<row;i++)
                   {
                      if(i==0)
                      { //创建表头
                        var head=document.createElement('thead')//创建表头
                        stutable.appendChild(head);
                        var stutr=document.createElement('tr');
                        head.appendChild(stutr);
                        for(var j=0;j<=col;j++)
                        {
                           if(j==0)
                           {
                             var idCell=document.createElement('th');
                             idCell.setAttribute('scope','col')
                             idCell.innerHTML='#'
                             stutr.appendChild(idCell)
                           }
                           else
                           {
                             var idCell=document.createElement('th');
                             idCell.setAttribute('scope','col');
                             idCell.innerHTML=result.stu_list[flag];
                             stutr.appendChild(idCell);
                             flag=flag+1;
                           }
                        }

                      }
                      else
                      {
                        if(i==1)
                        {
                          //创建表体
                          var bb=document.createElement('tbody')//创建表头
                          stutable.appendChild(bb);
                        }
                         var stuttr=document.createElement('tr');
                          bb.appendChild(stuttr);
                        for(var k=0;k<=col;k++)
                        {
                           if(k==0)
                           {
                             var idCell=document.createElement('th');
                             idCell.setAttribute('scope','col')
                             idCell.innerHTML=i;
                             stuttr.appendChild(idCell);
                           }
                           else
                           {
                             var idCell=document.createElement('td');
                             idCell.innerHTML=result.stu_list[flag];
                             stuttr.appendChild(idCell);
                             flag=flag+1;
                           }
                        }
                      }

                   }

                    alert(result.msg);
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
function undisplaystu()
{
    $("#stulist").html("");
}
function undisplaygroup()
{
    $("#grouplist").html("");
}
function displaygroup(){
var fileFlag=false
     $('#group-file').each(function(){
     if($(this).val()!=""){
     fileFlag=true;
     }
     })
     if(!fileFlag)
     {
       alert("请选择好文件!")
       return;
     }
    var groupfile=$('#group-file')[0].files[0];
    var formdata=new FormData();
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    formdata.append('groupfile',groupfile);
    formdata.append('csrfmiddlewaretoken',csrf);
     $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/displaygroup/" ,//url
            data: formdata,
            processData:false,
            contentType:false,
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                   //动态添加表单数据
                   var flag=0;
                   var row=result.rows;
                   var col=result.cols;
                   var grouptable=document.getElementById("grouplist");//获得table标签
                   for(var i=0;i<row;i++)
                   {
                      if(i==0)
                      { //创建表头
                        var head=document.createElement('thead')//创建表头
                        grouptable.appendChild(head);
                        var grouptr=document.createElement('tr');
                        head.appendChild(grouptr);
                        for(var j=0;j<=col;j++)
                        {
                           if(j==0)
                           {
                             var idCell=document.createElement('th');
                             idCell.setAttribute('scope','col')
                             idCell.innerHTML='#'
                             grouptr.appendChild(idCell)
                           }
                           else
                           {
                             var idCell=document.createElement('th');
                             idCell.setAttribute('scope','col');
                             idCell.innerHTML=result.group_list[flag];
                             grouptr.appendChild(idCell);
                             flag=flag+1;
                           }
                        }

                      }
                      else
                      {
                        if(i==1)
                        {
                          //创建表体
                          var bb=document.createElement('tbody')//创建表头
                          grouptable.appendChild(bb);
                        }
                         var groupttr=document.createElement('tr');
                          bb.appendChild(groupttr);
                        for(var k=0;k<=col;k++)
                        {
                           if(k==0)
                           {
                             var idCell=document.createElement('th');
                             idCell.setAttribute('scope','col')
                             idCell.innerHTML=i;
                             groupttr.appendChild(idCell);
                           }
                           else
                           {
                             var idCell=document.createElement('td');
                             idCell.innerHTML=result.group_list[flag];
                             groupttr.appendChild(idCell);
                             flag=flag+1;
                           }
                        }
                      }

                   }
                    alert(result.msg);
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
function displaydata()
{
var fileFlag=false
     $('#learn-file').each(function(){
     if($(this).val()!=""){
     fileFlag=true;
     }
     })
     if(!fileFlag)
     {
       alert("请选择好文件!")
       return;
     }
    var learnfile=$('#learn-file')[0].files[0];
    var formdata=new FormData();
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    formdata.append('learnfile',learnfile);
    formdata.append('csrfmiddlewaretoken',csrf);
     $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/displaydata/" ,//url
            data: formdata,
            processData:false,
            contentType:false,
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                   //动态添加表单数据
                   var flag=0;
                   var row=result.rows;
                   var col=result.cols;
                   var learntable=document.getElementById("learnlist");//获得table标签
                   //先清空
                   $("#learnlist").html("");
                   for(var i=0;i<row;i++)
                   {
                      if(i==0)
                      { //创建表头
                        var head=document.createElement('thead')//创建表头
                        learntable.appendChild(head);
                        var learntr=document.createElement('tr');
                        head.appendChild(learntr);
                        for(var j=0;j<=col;j++)
                        {
                           if(j==0)
                           {
                             var idCell=document.createElement('th');
                             idCell.setAttribute('scope','col')
                             idCell.innerHTML='#'
                             learntr.appendChild(idCell)
                           }
                           else
                           {
                             var idCell=document.createElement('th');
                             idCell.setAttribute('scope','col');
                             idCell.innerHTML=result.learn_list[flag];
                             learntr.appendChild(idCell);
                             flag=flag+1;
                           }
                        }

                      }
                      else
                      {
                        if(i==1)
                        {
                          //创建表体
                          var bb=document.createElement('tbody')//创建表头
                          learntable.appendChild(bb);
                        }
                         var learnttr=document.createElement('tr');
                          bb.appendChild(learnttr);
                        for(var k=0;k<=col;k++)
                        {
                           if(k==0)
                           {
                             var idCell=document.createElement('th');
                             idCell.setAttribute('scope','col')
                             idCell.innerHTML=i;
                             learnttr.appendChild(idCell);
                           }
                           else
                           {
                             var idCell=document.createElement('td');
                             idCell.innerHTML=result.learn_list[flag];
                             learnttr.appendChild(idCell);
                             flag=flag+1;
                           }
                        }
                      }

                   }

                    alert(result.msg);
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
function dataview()
{
var fileFlag=false
     $('#learn-file').each(function(){
     if($(this).val()!=""){
     fileFlag=true;
     }
     })
     if(!fileFlag)
     {
       alert("请选择好文件!")
       return;
     }
    var learnfile=$('#learn-file')[0].files[0];
    var formdata=new FormData();
    var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    formdata.append('learnfile',learnfile);
    formdata.append('csrfmiddlewaretoken',csrf);
     $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/displaydata/" ,//url
            data: formdata,
            processData:false,
            contentType:false,
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                   data=result.learn_list;
                   rows=result.rows;
                   cols=result.cols;
                   //动态添加表单数据
                   var flag=0;
                   var row=result.rows;
                   var col=result.cols;
                   var xdata=document.getElementById("x_data");//获得select标签
                   var ydata=document.getElementById("y_data");//获得select标签
                    //先清空
                    $("#x_data").html("");
                    $("#y_data").html("");
                    var flag=0;
                   for(var i=0;i<col;i++)
                   {
                             var idCell=document.createElement('option');
                             idCell.setAttribute('value',flag);
                             idCell.innerHTML=result.learn_list[i];
                             xdata.appendChild(idCell);
                             flag=flag+1;
                     }
                     var flag=0;
                     for(var i=0;i<col;i++)
                   {
                             var idCell=document.createElement('option');
                             idCell.setAttribute('value',flag);
                             idCell.innerHTML=result.learn_list[i];
                              ydata.appendChild(idCell);
                              flag=flag+1;
                     }
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
 var x_list='';
 var y_list='';
 var y_list_float=new Array();
 var y_list_dur=new Array();
 var x_name='';
 var y_name='';
function submitinfo()
{
    var obj = document.getElementById("x_data"); //定位id
     var index = obj.selectedIndex; // 选中索引
     var xdata = obj.options[index].value; // 选中值
     var obj1 = document.getElementById("y_data"); //定位id
     var index1 = obj1.selectedIndex; // 选中索引
     var ydata = obj1.options[index1].value; // 选中值
     var obj2 = document.getElementById("format"); //定位id
     var index2= obj2.selectedIndex; // 选中索引
     var format = obj2.options[index2].value; // 选中值
     var learnfile=$('#learn-file')[0].files[0];
     var formdata=new FormData();
     var csrf = $('input[name="csrfmiddlewaretoken"]').val();
    formdata.append('learnfile',learnfile);
    formdata.append('csrfmiddlewaretoken',csrf);
    formdata.append('xdata',xdata);
    formdata.append('ydata',ydata);
     $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/dataview/" ,//url
            data: formdata,
            processData:false,
            contentType:false,
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                   //动态加载表格
                   x_name=result.x_name;
                   y_name=result.y_name;
                   x_list=result.x_list;
                   y_list=result.y_list;
                   if(format==1)
                   {
                      //姓名+学习时长
                      console.log(y_list);
                      y_name=y_name+"(秒)"
                      //学习时长转化
                     for(var i=0;i<y_list.length;i++)
                          {
                             var duration=y_list[i].split(':')
                             var seconds=parseInt(duration[0])*60*60+parseInt(duration[1])*60+parseInt(duration[2]);
                             //console.log();
                             y_list_dur[i]=seconds;
                          }
                     let max = y_list_dur[0];
                         let max_id=0;
                            for (let i = 0; i < y_list_dur.length - 1; i++) {
                               if(max < y_list_dur[i+1])
                                {
                                   max_id=i+1;
                                }
                                max = max < y_list_dur[i+1] ? y_list_dur[i+1] : max

                            }
                          //console.log(max+x_list[max_id]);
                        let min = y_list_dur[0];
                         let min_id=0;
                            for (let i = 0; i < y_list_dur.length - 1; i++) {
                               if(min > y_list_dur[i+1])
                                {
                                   min_id=i+1;
                                }
                                min = min > y_list_dur[i+1] ? y_list_dur[i+1] : min
                            }
                         var mean=Math.round(y_list_dur.avg());
                         console.log(mean);
                         var hour=parseInt(mean/(60*60));
                         var minute=parseInt((mean-hour*(60*60))/60);
                         var seconds=mean-hour*(60*60)-minute*60;
                         var mean_time=hour+':'+minute+':'+seconds;
                         //设置半小时
                         learn_dur=30*60;
                        //设置最大值
                      $("#data_max").text("最大"+y_name);
                      $("#MAX").text(y_list[max_id]);
                      $("#x_name1").text(x_list[max_id]);
                      var max_per=max/learn_dur*100+'%'
                      $('#progress1').attr('aria-valuenow',max);
                      $('#progress1').attr('aria-valuemax',learn_dur);
                      $('#progress1').attr('style',"width:"+max_per);
                      //设置最小值
                      $("#data_min").text("最小"+y_name);
                      $("#MIN").text(y_list[min_id]);
                      $("#x_name2").text(x_list[min_id]);
                      var min_per=min/learn_dur*100+'%'
                      $('#progress2').attr('aria-valuenow',min);
                      $('#progress2').attr('aria-valuemax',learn_dur);
                      $('#progress2').attr('style',"width:"+min_per);
                      //设置均值
                      $("#data_mean").text("平均"+y_name);
                      $("#MEAN").text(mean_time);
                      $("#x_name3").text("显示数据的平均"+y_name);
                      var mean_per=mean/learn_dur*100+'%'
                      $('#progress3').attr('aria-valuenow',mean);
                      $('#progress3').attr('aria-valuemax',learn_dur);
                      $('#progress3').attr('style',"width:"+mean_per);
                       $("#chart_title").text(x_name+"与"+y_name);
                      addbarchart(y_list_dur);
                   }
                   if(format==2)
                   {
                      //姓名+开始作答时间

                   }
                   if(format==3)
                   {
                      //姓名+开始学习时间

                   }
                   if(format==4)
                   {
                      //姓名+得分
                        for(var i=0;i<y_list.length;i++)
                          {
                             y_list_float[i]=parseFloat(y_list[i]);

                          }
                         let max = y_list_float[0];
                         let max_id=0;
                            for (let i = 0; i < y_list_float.length - 1; i++) {
                               if(max < y_list_float[i+1])
                                {
                                   max_id=i+1;
                                }
                                max = max < y_list_float[i+1] ? y_list_float[i+1] : max

                            }
                          //console.log(max+x_list[max_id]);
                        let min = y_list_float[0];
                         let min_id=0;
                            for (let i = 0; i < y_list_float.length - 1; i++) {
                               if(min > y_list_float[i+1])
                                {
                                   min_id=i+1;
                                }
                                min = min > y_list_float[i+1] ? y_list_float[i+1] : min
                            }
                         var mean=y_list_float.avg();
                        //设置最大值
                      $("#data_max").text("最大"+y_name);
                      $("#MAX").text(max);
                      $("#x_name1").text(x_list[max_id]);
                      var max_per=max/25*100+'%'
                      $('#progress1').attr('aria-valuenow',max);
                      $('#progress1').attr('aria-valuemax',25);
                      $('#progress1').attr('style',"width:"+max_per);
                      //设置最小值
                      $("#data_min").text("最小"+y_name);
                      $("#MIN").text(min);
                      $("#x_name2").text(x_list[min_id]);
                      var min_per=min/25*100+'%'
                      $('#progress2').attr('aria-valuenow',min);
                      $('#progress2').attr('aria-valuemax',25);
                      $('#progress2').attr('style',"width:"+min_per);
                      //设置均值
                      $("#data_mean").text("平均"+y_name);
                      $("#MEAN").text(mean.toFixed(2));//保留两位小数
                      $("#x_name3").text("显示数据的平均"+y_name);
                      var mean_per=mean/25*100+'%';

                      $('#progress3').attr('aria-valuenow',mean);
                      $('#progress3').attr('aria-valuemax',25);
                      $('#progress3').attr('style',"width:"+mean_per);
                      $("#chart_title").text(x_name+"与"+y_name);
                      addcharts();
                   }

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
function feedback_delete(obj)
{
  var feedback_id = obj.id;
   $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/feedback_delete/" ,//url
            data: {'id':feedback_id},
            success: function (result) {
                if (result.resultCode == 200)
                {
                   alert(result.msg);
                   //移除dom元素
                   var name=
                   document.getElementById("邮件"+feedback_id).remove();
                   document.getElementById("maildetail").innerHTML="";
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
function feedback_reply(obj)
{
   var feedback_id = obj.id;
   var name=document.getElementById('author_name').innerHTML;
   var group_id=document.getElementById('author_groupid').innerHTML;
   var group_role=document.getElementById('author_role').innerHTML;
   //alert(name);
   $('#reply-info').text("TO/From:  "+group_id+" "+group_role+name);
}
function load_mail(result)
 {
                 //动态加载邮件内容
                   $('#maildetail').html('');//清空
                   var maildetail=document.getElementById('maildetail');
                   var mail_header=document.createElement('div');
                   mail_header.setAttribute("class","mail-header");
                    var mail_title=document.createElement('div');
                   mail_title.setAttribute("class","mail-title");
                   var title_h4=document.createElement('h4');
                   title_h4.innerHTML=result.feedback_list[0].feedback_title;
                   mail_title.appendChild(title_h4);
                   mail_header.appendChild(mail_title);
                   var mail_actions=document.createElement('div');
                   mail_actions.setAttribute("class","mail-actions");
                    var button_reply=document.createElement('button');
                   button_reply.setAttribute("type","button");
                   button_reply.setAttribute("id",result.feedback_list[0].feedback_id);
                   button_reply.setAttribute("data-bs-toggle","modal");
                   button_reply.setAttribute("data-bs-target","#replymail");
                   button_reply.setAttribute("onclick","feedback_reply(this)");
                   button_reply.setAttribute("class","btn btn-secondary");
                   button_reply.innerHTML='回复'
                   var button_delete=document.createElement('button');
                   button_delete.setAttribute("type","button");
                   button_delete.setAttribute("id",result.feedback_list[0].feedback_id);
                   button_delete.setAttribute("onclick","feedback_delete(this)");
                   button_delete.setAttribute("class","btn btn-danger");
                   button_delete.innerHTML='删除'
                   mail_actions.appendChild(button_reply);
                   mail_actions.appendChild(button_delete);
                   mail_header.append(mail_actions);
                   var mail_info=document.createElement('div');
                   mail_info.setAttribute("class","mail-info");
                   var mail_author=document.createElement('div');
                   mail_author.setAttribute("class","mail-author");
                   var user_img=document.createElement('img');
                   user_img.setAttribute("src","/statics/assets_tech/images/avatars/profile-image.png");
                   user_img.setAttribute("alt","");
                   var mail_author_info=document.createElement('div');
                   mail_author_info.setAttribute("class","mail-author-info");
                   var span1=document.createElement('span');
                   span1.setAttribute("id","author_name");
                   span1.setAttribute("class","mail-author-name");
                   span1.innerHTML=result.feedback_list[0].name;
                   var span2=document.createElement('span');
                   span2.setAttribute("id","author_role");
                   span2.setAttribute("class","mail-author-address");
                   span2.innerHTML=result.feedback_list[0].group_role;
                   var span4=document.createElement('span');
                   span4.setAttribute("id","author_groupid");
                   span4.setAttribute("class","mail-author-address");
                   span4.innerHTML=result.feedback_list[0].num;
                   var mail_other_info=document.createElement('div');
                   mail_author_info.setAttribute("class","mail-other-info");
                   var span3=document.createElement('span');
                   span3.innerHTML=result.feedback_list[0].feedback_time;
                   mail_author_info.appendChild(span1);
                   mail_author_info.appendChild(span2);
                   mail_author_info.appendChild(span4);
                   mail_other_info.appendChild(span3);
                   mail_author.appendChild(user_img);
                   mail_author.appendChild(mail_author_info);
                   mail_info.appendChild(mail_author);
                   mail_info.appendChild(mail_other_info);
                   mail_header.append(mail_info);
                   maildetail.appendChild(mail_header);
                   var mail_text=document.createElement('div');
                    mail_text.setAttribute("class","mail-text");
                    mail_text.innerHTML=result.feedback_list[0].feedback_content;
                    maildetail.appendChild(mail_text);
                    var mail_attachment=document.createElement('div');
                    mail_attachment.setAttribute("class","mail-attachment");
                    var span4=document.createElement('span');
                    span4.setAttribute("class","attachment-info");
                    span4.innerHTML=result.feedback_list[0].feedback_file+'个 附件';
                    var mail_attachment_files=document.createElement('div');
                    mail_attachment_files.setAttribute("class","mail-attachment-files");
                    if(parseInt(result.feedback_list[0].feedback_file)>0)
                    {
                       for(var i=0;i<result.feedback_list[0].file_list.length;i++)
                       {
                         var card=document.createElement('div');
                         card.setAttribute("class","card");
                         var img1=document.createElement('img');
                         img1.setAttribute("src","/statics/assets_tech/images/card-bg.png");
                         img1.setAttribute("class","card-img-top");
                         img1.setAttribute("alt","...");
                         var card_body=document.createElement('div');
                         card_body.setAttribute("class","card-body");
                         var card_title=document.createElement('h5');
                         card_title.setAttribute("class","card-title");
                         card_title.innerHTML=result.feedback_list[0].file_list[i].file_name
                         var card_text=document.createElement('p');
                         card_text.setAttribute("class","card-text text-secondary");
                         card_text.innerHTML=result.feedback_list[0].file_list[i].fsize+" KB";
                         card_body.appendChild(card_title);
                         card_body.appendChild(card_text);
                          var a2=document.createElement('a');
                              a2.setAttribute("href","/readfiles/?file_id="+result.feedback_list[0].file_list[i].id);
                              a2.innerHTML='下载查看';
                         card_body.appendChild(a2);
                         card.appendChild(img1);
                         card.appendChild(card_body);
                         mail_attachment_files.appendChild(card);
                       }
                       mail_attachment.appendChild(span4);
                       mail_attachment.appendChild(mail_attachment_files);
                       maildetail.appendChild(mail_attachment);
                       }
}
function showmaildetail(feedback_id)
{
   console.log(feedback_id);
   var name='邮件'+feedback_id;
   var li=document.getElementById(name);
   li.setAttribute("class","active");
   $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/showmaildetail/" ,//url
            data: {'id':feedback_id},
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                        load_mail(result);

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
 function addcharts( ) {
    $("#apex1").html("");
    $("#chartjs2").html("");
   var options = {
        chart: {
            height: 350,
            type: 'line',
            zoom: {
                enabled: false
            }
        },
        series: [{
            name: y_name,
            data: y_list
        }],
        dataLabels: {
            enabled: false
        },
        stroke: {
            curve: 'straight'
        },
        title: {
            text: x_name,
            align: 'left'
        },
        grid: {
            row: {
                colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
                opacity: 0.5
            },
            borderColor: 'rgba(94, 96, 110, .5)',
            strokeDashArray: 4
        },
        xaxis: {
            categories: x_list,
            labels: {
                style: {
                    colors: 'rgba(94, 96, 110, .5)'
                }
            }
        }
    }

    var chart1 = new ApexCharts(
        document.querySelector("#apex1"),
        options
    );

    chart1.render();
}
function addbarchart(y_list_dur) {
    $("#apex1").html("");
    $("#chartjs2").html("");
   console.log(y_list_dur);
   console.log(x_list);
   new Chart(
   document.getElementById("chartjs2"),
   {
   "type": "bar",
   "data": {
      "labels": x_list,
      "datasets": [{
      "label": x_name+"与"+y_name,
      "data": y_list_dur,
      "fill": false,
      "backgroundColor": ["rgba(255, 99, 132, 0.2)", "rgba(255, 159, 64, 0.2)", "rgba(255, 205, 86, 0.2)", "rgba(75, 192, 192, 0.2)", "rgba(54, 162, 235, 0.2)", "rgba(153, 102, 255, 0.2)", "rgba(201, 203, 207, 0.2)"],
       "borderColor": ["rgb(255, 99, 132)", "rgb(255, 159, 64)", "rgb(255, 205, 86)", "rgb(75, 192, 192)", "rgb(54, 162, 235)", "rgb(153, 102, 255)", "rgb(201, 203, 207)"],
       "borderWidth": 1 }] },
        "options":
        { "scales":
           { "yAxes": [{ "ticks": { "beginAtZero": true } }] } } });

}
//数组求平均值
Array.prototype.avg = function (call) {
    let type = Object.prototype.toString.call(call);
    let sum = 0;
    if (type === '[object Function]') {
        sum = this.reduce((pre, cur, i) => pre + call(cur, i), 0);
    } else {
        sum = this.reduce((pre, cur) => pre + cur);
    }
    return sum / this.length;
};
/**
 * 数组求和
 * @param call {Function}适用于对象中的某个属性求和场景,回调时会传回 item, index
 * @returns {Number} 返回数组的和。
 */
Array.prototype.sum = function (call) {
    let type = Object.prototype.toString.call(call);
    if (type === '[object Function]') {
        return this.reduce((pre, cur, i) => pre + call(cur, i), 0);
    } else {
        return this.reduce((pre, cur) => pre + cur);
    }
};