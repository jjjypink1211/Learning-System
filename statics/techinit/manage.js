$('#addstunum').change(function(){
const nonlist= JSON.parse(document.getElementById('nonlist').textContent);
       var stu_num=$(this).children('option:selected').val();  //弹出select的值
        for(var i=0;i<nonlist.length;i++)
        {
           if(nonlist[i].fields.num==stu_num)
           {
             $('#new_name').val(nonlist[i].fields.name);
             $('#new_grade').val(nonlist[i].fields.grade);
             break;
           }
        }


 });
 var choose_stu=new Array();
 $('#choose_mem').change(function(){
        console.log(choose_stu);
        var stu_num=$(this).children('option:selected').val();  //弹出select的值
        for(var i=0;i<choose_stu.length;i++)
        {
           if(choose_stu[i].num==stu_num)
           {
             $("#choose_name").val(choose_stu[i].name);
             $("#choose_grade").val(choose_stu[i].grade);
           }
        }

 });
 function addnewstu(group_id)
 {
    $('#addnewmemLabel').html(group_id);
 }
 function addnewmember()
 {
  if (!$('#addstunum').children('option:selected').val())
  {
     alert("请选择学生信息!");
     return;
  }
  stu_num=$('#addstunum').children('option:selected').val();
  group_id=$('#addnewmemLabel').html();
  $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/addnewgroupmember/" ,//url
            data: {'stu_num':stu_num,'group_id':group_id
            },
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
 function onloadinfo(group_id)
 {
   $('#onloadgroupLabel').html(group_id);
   $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/onloadgroupinfo/" ,//url
            data: {'group_id':group_id },
            dataType: 'json',
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                  $("#choose_role").html("");
                  $("#choose_mem").html("");
                  $("#choose_name").val("");
                  $("#choose_grade").val("");
                  var sub_list=result.sub_list;
                  new_option=$("<option selected disabled >选择角色...</option>");
                  $("#choose_role").append(new_option);
                  for(var i=0;i<sub_list.length;i++)
                  {
                    var newoption=$("<option value="+sub_list[i]+">"+sub_list[i]+"</option>")
                    $("#choose_role").append(newoption);
                  }
                  var stu_list=result.stu_list;
                  choose_stu=stu_list;
                  $("#choose_mem").append($("<option selected disabled >选择学号...</option>"));
                  for(var i=0;i<stu_list.length;i++)
                  {
                    var newoption=$("<option value="+stu_list[i].num+">"+stu_list[i].num+"</option>")
                    $("#choose_mem").append(newoption);
                  }
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
 function submitchooserole()
 {
       if (!$('#choose_mem').children('option:selected').val())
      {
         alert("请选择学生信息!");
         return;
      }if (!$('#choose_role').children('option:selected').val())
      {
         alert("请选择担任角色!");
         return;
      }
   var group_id=$('#onloadgroupLabel').html();
   var stu_num=$('#choose_mem').children('option:selected').val();
   var stu_role=$('#choose_role').children('option:selected').val();
    $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/submitchooserole/" ,//url
            data: {'stu_num':stu_num,'group_id':group_id,'stu_role':stu_role
            },
            dataType: 'json',
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                    alert(result.msg);
                    onloadinfo(group_id);
                    //location.reload();
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
function changeinfo()
{
  var td = event.srcElement; // 通过event.srcElement 获取激活事件的对象 td
  //alert("行号：" + (td.parentElement.rowIndex) + "，列号：" + td.cellIndex);
  var srows=td.parentElement.rowIndex;
  var scols=td.cellIndex;
  var tableId = document.getElementById("zero-conf");
  //alert(tableId.rows[srows].cells[scols-1].innerHTML);
  document.getElementById("stu_num").value=tableId.rows[srows].cells[scols-5].innerHTML
  document.getElementById("stu_name").value=tableId.rows[srows].cells[scols-4].innerHTML
  document.getElementById("stu_grade").value=tableId.rows[srows].cells[scols-3].innerHTML
  document.getElementById("stu_group").value=tableId.rows[srows].cells[scols-2].innerHTML
  var all_options = document.getElementById("stu_po").options;
  var optionID=tableId.rows[srows].cells[scols-1].innerHTML
  for (i=0; i<all_options.length; i++)
    {
          if (all_options[i].value == optionID)  // 根据option标签的ID来进行判断  测试的代码这里是两个等号
            {
               all_options[i].selected = true;
            }
      }
}
function changenoninfo()
{
  var td = event.srcElement; // 通过event.srcElement 获取激活事件的对象 td
  //alert("行号：" + (td.parentElement.rowIndex) + "，列号：" + td.cellIndex);
  var srows=td.parentElement.rowIndex;
  var scols=td.cellIndex;
  var tableId = document.getElementById("nonzero-conf");
  //alert(tableId.rows[srows].cells[scols-1].innerHTML);
  document.getElementById("stu_num").value=tableId.rows[srows].cells[scols-5].innerHTML
  document.getElementById("stu_name").value=tableId.rows[srows].cells[scols-4].innerHTML
  document.getElementById("stu_grade").value=tableId.rows[srows].cells[scols-3].innerHTML
  document.getElementById("stu_group").value=tableId.rows[srows].cells[scols-2].innerHTML
  var all_options = document.getElementById("stu_po").options;
  var optionID=tableId.rows[srows].cells[scols-1].innerHTML
  for (i=0; i<all_options.length; i++)
    {
          if (all_options[i].value == optionID)  // 根据option标签的ID来进行判断  测试的代码这里是两个等号
            {
               all_options[i].selected = true;
            }
      }
}

function changescoreinfo()
{
  var td = event.srcElement; // 通过event.srcElement 获取激活事件的对象 td
  //alert("行号：" + (td.parentElement.rowIndex) + "，列号：" + td.cellIndex+",组号："+td.id);
  var srows=td.parentElement.rowIndex;
  var scols=td.cellIndex;
  var group_id="group"+td.id;
  var tableId = document.getElementById(group_id);
  document.getElementById("stu_num").value=tableId.rows[srows].cells[scols-5].innerHTML
  document.getElementById("stu_name").value=tableId.rows[srows].cells[scols-4].innerHTML
  document.getElementById("stu_grade").value=tableId.rows[srows].cells[scols-3].innerHTML
  document.getElementById("stu_group").value=td.id;
  document.getElementById("stu_score").value=tableId.rows[srows].cells[scols-1].innerHTML
}
function submitinfo()
{
     var csrf = $('input[name="csrfmiddlewaretoken"]').val();
     var stu_num=$("input[name='stu_num']").val();
     var stu_name=$("input[name='stu_name']").val();
     var stu_grade=$("input[name='stu_grade']").val();
     var stu_group=$("input[name='stu_group']").val();
     var obj = document.getElementById("stu_po"); //定位id
     var index = obj.selectedIndex; // 选中索引
     var stu_po = obj.options[index].value; // 选中值
     console.log(stu_num+stu_grade+ stu_po);
      $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/stumanagechange/" ,//url
            data: {'stu_num':stu_num,'stu_name':stu_name,
            'stu_grade':stu_grade,'stu_group':stu_group,'stu_po':stu_po,
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
function submitscoreinfo()
{
     var csrf = $('input[name="csrfmiddlewaretoken"]').val();
     var stu_num=$("input[name='stu_num']").val();
     var stu_score=$("input[name='stu_score']").val();

      $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/scoremanagechange/" ,//url
            data: {'stu_num':stu_num,'stu_score':stu_score,
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
                if(result.resultCode==300){
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

var tempDiv=document.getElementById('butdiv');
var teBut=tempDiv.getElementsByTagName('button');
console.log(teBut.length)
for(var i=0;i<teBut.length;i++){
teBut[i].onclick=function(){
console.log(this.id)
var group_id=this.id;
var csrf = $('input[name="csrfmiddlewaretoken"]').val();
$.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/memberscore/" ,//url
            data: {'group_id':group_id,
            'csrfmiddlewaretoken': csrf},
            dataType: 'json',
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                   //alert(result.msg);
                  //动态添加表单数据
                   row=result.listgroup.length;
                   t_name="stuinfo"+group_id;
                   var bb=document.getElementById(t_name);//获得tbody标签
                   //清空数据
                   $("#"+t_name).html("");
                   for(var i=0;i<row;i++)
                   {
                        var stuttr=document.createElement('tr');
                          bb.appendChild(stuttr);
                          var idCell=document.createElement('td');
                          idCell.innerHTML=result.listgroup[i].fields.num;
                          stuttr.appendChild(idCell);
                          var idCell=document.createElement('td');
                          idCell.innerHTML=result.listgroup[i].fields.name;
                          stuttr.appendChild(idCell);
                          var idCell=document.createElement('td');
                          idCell.innerHTML=result.listgroup[i].fields.grade;
                          stuttr.appendChild(idCell);
                          var idCell=document.createElement('td');
                          idCell.innerHTML=result.listgroup[i].fields.group_role;
                          stuttr.appendChild(idCell);
                          var idCell=document.createElement('td');
                          idCell.innerHTML=result.listgroup[i].fields.score;
                          stuttr.appendChild(idCell);
                          var idCell=document.createElement('td');
                          idCell.setAttribute("class","btn btn-primary");
                          idCell.setAttribute("id",group_id);
                          idCell.setAttribute("data-bs-toggle","modal");
                          idCell.setAttribute("data-bs-target","#staticBackdrop");
                          idCell.setAttribute("onclick","changescoreinfo()");
                          idCell.innerHTML="修改成绩";
                          stuttr.appendChild(idCell);
                      }

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
}

