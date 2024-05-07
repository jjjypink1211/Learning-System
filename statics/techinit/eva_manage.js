function displayeva(eva_type,valuer_num,beeva_name)
{
 $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/display_eva/" ,//url
            data: {'eva_type':eva_type,'valuer_num':valuer_num,'beeva_num':beeva_name},
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
function deleteeva(pj_id)
{
 $('#delete_pj_id').text(pj_id);
}
function delete_eva()
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