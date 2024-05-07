function submit_techeva()
{
  //获得题目列表
  eva_list = JSON.parse(document.getElementById('eva_list').textContent);
  eva_type = eva_list[0].evaluate_type;
  //获得时间
  eva_time = JSON.parse(document.getElementById('time1').textContent);
  act_name = '教师评价';
   group_id = '0';
  submit_form=new Array();
     var obj = document.getElementById('diff_group'); //定位id
     var index = obj.selectedIndex; // 选中索引
     var diff_group = obj.options[index].value; // 选中值
     if(diff_group == 'none')
             {
               alert('必须选择评价小组!');
               return;
             }
     var beeva_num=diff_group;
     //获得教师信息
    teacher_info = JSON.parse(document.getElementById('teacher_info').textContent);
    valuer_num = teacher_info[0].num;
  for(var i=0;i<eva_list.length;i++)
  {
     eva_id=eva_list[i].evaluate_id;
    if(eva_list[i].struct_type==1)
    {
         //radio分值
        var mark=$("input[name='"+eva_id+"']:checked").val();
        submit_form.push({
        "eva_type":eva_type,
        "group_id":group_id,
        "act_name":act_name,
         "valuer_num": valuer_num,
         "eva_time" : eva_time,
        "beeva_num": beeva_num,
        'eva_id':eva_id,
        'eva_content':mark,
        'form_type':eva_list[i].struct_type});

    }else if(eva_list[i].struct_type==2)
    {
             var obj = document.getElementById(""+eva_id+""); //定位id
             var index = obj.selectedIndex; // 选中索引
             var time = obj.options[index].value; // 选中值
             submit_form.push({
             "eva_type":eva_type,
             "group_id":group_id,
             "act_name":act_name,
             "valuer_num": valuer_num,
             "eva_time" : eva_time,
             "beeva_num": beeva_num,
             'eva_id':eva_id,
             'eva_content':time,
             'form_type':eva_list[i].struct_type});
             if(time=='none')
             {
               alert('必须选择时长');
               return;
             }
    }
  }
   $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/addstueva/" ,//url
            data: {"submit_data":JSON.stringify(submit_form)} ,
            //traditional:true,
            success: function (result) {
                console.log(result);
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
function submit_eva()
{
  //获得题目列表
  eva_list = JSON.parse(document.getElementById('eva_list').textContent);
  eva_type = eva_list[0].evaluate_type;
  //获得小组信息
  group_info = JSON.parse(document.getElementById('group_info').textContent);
  group_id = group_info[0].group_id;
  act_name = group_info[0].topic;
  //获得学生信息
  stu_info = JSON.parse(document.getElementById('stu_info').textContent);
  valuer_num = stu_info[0].num;
  //获得时间
  eva_time = JSON.parse(document.getElementById('time1').textContent);
  submit_form=new Array();
  var beeva_num='无';
  if(eva_type ==  '个人评论')
  {
     var beeva_num='无';
  }
  else if(eva_type == '组内评论')
  {
     var beeva_num=group_id;
  }else if(eva_type == '组间互评')
  {
     var obj = document.getElementById('diff_group'); //定位id
     var index = obj.selectedIndex; // 选中索引
     var diff_group = obj.options[index].value; // 选中值
     if( diff_group == 'none')
             {
               alert('必须选择评价小组!');
               return;
             }
     var beeva_num=diff_group;
  }else if(eva_type == '成员互评')
  {
     var obj = document.getElementById('mem_group'); //定位id
     var index = obj.selectedIndex; // 选中索引
     var mem_group = obj.options[index].value; // 选中值
     if(mem_group == 'none')
             {
               alert('必须选择评价小组!');
               return;
             }
     var beeva_num=mem_group;
  }else if(eva_type == '教师互评')
  {
     var obj = document.getElementById('diff_group'); //定位id
     var index = obj.selectedIndex; // 选中索引
     var mem_group = obj.options[index].value; // 选中值
     if(diff_group == 'none')
             {
               alert('必须选择评价小组!');
               return;
             }
     var beeva_num=mem_group;
     //获得教师信息
    teacher_info = JSON.parse(document.getElementById('teacher_info').textContent);
    valuer_num = teacher_info[0].num;
    act_name = '教师评价';
    group_id = '0';
  }
  for(var i=0;i<eva_list.length;i++)
  {
     eva_id=eva_list[i].evaluate_id;
    if(eva_list[i].struct_type==1)
    {
         //radio分值
        var mark=$("input[name='"+eva_id+"']:checked").val();
        submit_form.push({
        "eva_type":eva_type,
        "group_id":group_id,
        "act_name":act_name,
         "valuer_num": valuer_num,
         "eva_time" : eva_time,
        "beeva_num": beeva_num,
        'eva_id':eva_id,
        'eva_content':mark,
        'form_type':eva_list[i].struct_type});

    }else if(eva_list[i].struct_type==2)
    {
             var obj = document.getElementById(""+eva_id+""); //定位id
             var index = obj.selectedIndex; // 选中索引
             var time = obj.options[index].value; // 选中值
             submit_form.push({
             "eva_type":eva_type,
             "group_id":group_id,
             "act_name":act_name,
             "valuer_num": valuer_num,
             "eva_time" : eva_time,
             "beeva_num": beeva_num,
             'eva_id':eva_id,
             'eva_content':time,
             'form_type':eva_list[i].struct_type});
             if(time=='none')
             {
               alert('必须选择时长');
               return;
             }
    }
  }
   $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/addstueva/" ,//url
            data: {"submit_data":JSON.stringify(submit_form)} ,
            //traditional:true,
            success: function (result) {
                console.log(result);
                if (result.resultCode == 200) {
                    alert(result.msg);
                     window.location.reload();
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
function displayeva(pj_id)
{
 $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/display_stu_eva/" ,//url
            data: {'pj_id':pj_id},
            success: function (result) {
                console.log(result);
                $('#valuer_name').text(
                function(i,origText){
                    return  "评价者:" +' '+result.eva_list[0].valuer_name;
                  });
                $('#group_id').text(
                function(i,origText){
                    return  "小组编号:" +' '+ result.eva_list[0].group_id;
                  });
                $('#eva_time').text(
                function(i,origText){
                    return  "评价时间:" +' '+result.eva_list[0].eva_time;
                  });
                $('#eva_type').text(
                function(i,origText){
                    return  "评价类型:" +' '+result.eva_list[0].eva_type;
                  });
                $('#beeva_num').text(
                function(i,origText){
                    return  "被评价者:" +' '+result.eva_list[0].beeva_num;
                  });
                if (result.resultCode == 200) {
                   //动态添加表单数据
                   var evatable=document.getElementById("evainfo");//获得tbody标签
                   //先清空
                   $("#evainfo").html("");

                   for(var i=0;i<result.eva_list.length;i++)
                   {
                         var evatr=document.createElement('tr');
                         evatable.appendChild(evatr);
                          var idCell=document.createElement('td');
                          idCell.innerHTML=i+1;
                          evatr.appendChild(idCell);
                          var idCell=document.createElement('td');
                          idCell.innerHTML=result.eva_list[i].eva_id;
                          evatr.appendChild(idCell);
                          var idCell=document.createElement('td');
                          idCell.innerHTML=result.eva_list[i].eva_title;
                          evatr.appendChild(idCell);
                          var idCell=document.createElement('td');
                          idCell.innerHTML=result.eva_list[i].eva_content;
                          evatr.appendChild(idCell);
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
function create_select(eva_content,i,text)
{
                    var newoption=document.createElement('option');
                                newoption.setAttribute("value",i);
                             if(parseInt(eva_content) == i)
                               {
                                 newoption.setAttribute("selected","true");
                               }
                               newoption.innerHTML=text;
  return newoption;
}
function display_modify_eva(pj_id)
{
 $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/display_stu_eva/" ,//url
            data: {'pj_id':pj_id},
            success: function (result) {
                console.log(result);
                $('#modify_valuer_name').text(
                function(i,origText){
                    return  "评价者:" +' '+result.eva_list[0].valuer_name;
                  });
                $('#modify_group_id').text(
                function(i,origText){
                    return  "小组编号:" +' '+ result.eva_list[0].group_id;
                  });
                $('#modify_eva_time').text(
                function(i,origText){
                    return  "评价时间:" +' '+result.eva_list[0].eva_time;
                  });
                $('#modify_eva_type').text(
                function(i,origText){
                    return  "评价类型:" +' '+result.eva_list[0].eva_type;
                  });
                $('#modify_beeva_num').text(
                function(i,origText){
                    return  "被评价者:" +' '+result.eva_list[0].beeva_num;
                  });
                  $('#modify_pj_id').text(
                function(i,origText){
                    return  "评价编号:" +' '+result.eva_list[0].pj_id;
                  });
                if (result.resultCode == 200) {
                   //动态添加表单数据
                   var evatable=document.getElementById("modify_evainfo");//获得tbody标签
                   //先清空
                   $("#modify_evainfo").html("");

                   for(var i=0;i<result.eva_list.length;i++)
                   {
                         var evatr=document.createElement('tr');
                         evatable.appendChild(evatr);
                          var idCell=document.createElement('td');
                          idCell.innerHTML=i+1;
                          evatr.appendChild(idCell);
                          var idCell=document.createElement('td');
                          idCell.innerHTML=result.eva_list[i].eva_id;
                          evatr.appendChild(idCell);
                          var idCell=document.createElement('td');
                          idCell.innerHTML=result.eva_list[i].eva_title;
                          evatr.appendChild(idCell);
                          if(result.eva_list[i].form_type=='1')
                          {
                            //评价类型为分值
                            var idCell=document.createElement('td');
                            var select1=document.createElement('select');
                            select1.setAttribute("class","form-select");
                            select1.setAttribute("id",result.eva_list[i].eva_id);
                            for(var j=0;j<6;j++)
                            {
                               var newoption=document.createElement('option');
                               newoption.setAttribute("value",j);
                               if(parseInt(result.eva_list[i].eva_content) == j)
                               {
                                 newoption.setAttribute("selected","true");
                               }
                               newoption.innerHTML=j;
                               select1.appendChild(newoption);
                            }
                            idCell.appendChild(select1);
                            evatr.appendChild(idCell);
                          }else if(result.eva_list[i].form_type=='2')
                          {
                            //评价类型为时长
                            var idCell=document.createElement('td');
                             var select1=document.createElement('select');
                            select1.setAttribute("class","form-select");
                            select1.setAttribute("id",result.eva_list[i].eva_id);
                            newoption=create_select(result.eva_list[i].eva_content,30,'半小时');
                            select1.appendChild(newoption);
                            newoption=create_select(result.eva_list[i].eva_content,60,'1小时');
                            select1.appendChild(newoption);
                             newoption=create_select(result.eva_list[i].eva_content,120,'2小时');
                             select1.appendChild(newoption);
                              newoption=create_select(result.eva_list[i].eva_content,180,'3小时');
                             select1.appendChild(newoption);
                             newoption=create_select(result.eva_list[i].eva_content,240,'4小时');
                             select1.appendChild(newoption);
                             newoption=create_select(result.eva_list[i].eva_content,300,'4小时及以上');
                             select1.appendChild(newoption);
                             idCell.appendChild(select1);
                             evatr.appendChild(idCell);
                          }

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
function deleteeva(pj_id)
{
 $('#delete_pj_id').text(pj_id);
}
function delete_eva(pj_id)
{
  var pj_id=$('#delete_pj_id').text();
  $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/delete_stu_eva/" ,//url
            data: {'pj_id':pj_id},
            success: function (result) {
                console.log(result);
                if (result.resultCode == 200) {
                    alert(result.msg);
                    window.location.reload();
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
function submit_modify()
{
   var tableId = document.getElementById("modify_Evalist");
    var rows = tableId.rows.length;
    var colums = tableId.rows[0].cells.length;
    var pj_id=document.getElementById("modify_pj_id").innerHTML.split(':')[1];
    var modify_form=new Array();
     for(var i=1;i<rows;i++)
     {
        select_id=tableId.rows[i].cells[1].innerHTML;
        var obj = document.getElementById(select_id); //定位id
        var index = obj.selectedIndex; // 选中索引
        var score = obj.options[index].value; // 选中值
         modify_form.push({
          'pj_id': pj_id,
          'eva_id': select_id,
          'eva_content': score
         })
     }
     $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/modifystueva/" ,//url
            data: {"modify_data":JSON.stringify(modify_form)} ,
            //traditional:true,
            success: function (result) {
                console.log(result);
                if (result.resultCode == 200) {
                    alert(result.msg);
                    display_modify_eva(pj_id);
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