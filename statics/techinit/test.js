function stutijiao() {
     var csrf = $('input[name="csrfmiddlewaretoken"]').val();
     var stu_num=$("input[name='stu_num']").val();
     var stu_name=$("input[name='stu_name']").val();
     var stu_grade=$("input[name='stu_grade']").val();
     console.log({'stu_num':stu_num,'stu_name':stu_name,'stu_grade':stu_grade,'csrfmiddlewaretoken': csrf});
        $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/add_stuinitinfo/" ,//url
            data: {'stu_num':stu_num,'stu_name':stu_name,'stu_grade':stu_grade,'csrfmiddlewaretoken': csrf},
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
function grouptijiao() {
     //ajax上传文件必须通过Formdata对象传输数据
     var formdata=new FormData();
     var csrf = $('input[name="csrfmiddlewaretoken"]').val();
     var group_num=$("input[name='group_num']").val();
     var group_topic=$("input[name='group_topic']").val();
    formdata.append('group_num',group_num);
    formdata.append('group_topic',group_topic);
    formdata.append('csrfmiddlewaretoken',csrf);
        $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/add_groupinitinfo/" ,//url
            data: formdata,
            dataType: 'json',
            processData:false,
            contentType:false,
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
function hello1()
{
   var csrf = $('input[name="csrfmiddlewaretoken"]').val();
   $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/hello1/" ,//url
            data: {'csrfmiddlewaretoken': csrf},
            dataType: 'json',
            success: function (result) {
                console.log(result)

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



