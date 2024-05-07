function manage_talkfile(group_id)
{
  $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/dp_talkdata/" ,//url
            data: {group_id : group_id},
            success: function (result) {
                console.log(result);
                //先清空
                   $("#learnlist").html("");
                if (result.resultCode == 200) {
                   //动态添加表单数据
                   var flag=6;
                   var row=result.rows;
                   var col=result.cols;
                   var learntable=document.getElementById("learnlist");//获得table标签

                   for(var i=0;i<row-1;i++)
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
                             idCell.setAttribute('style','display: inline-block;white-space: nowrap;width: 100px;overflow: hidden;text-overflow:ellipsis;')
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
                        for(var k=0;k<=col+1;k++)
                        {
                           if(k==0)
                           {
                             var idCell=document.createElement('th');
                             idCell.setAttribute('scope','col')
                             idCell.innerHTML=i;
                             learnttr.appendChild(idCell);
                           }
                           else if(k==col+1)
                           {
                             var idCell=document.createElement('td');
                             idCell.setAttribute('style','display: inline-block;white-space: nowrap;width: 180px;overflow: hidden;text-overflow:ellipsis;')
                             send_name=result.learn_list[flag-col+3]
                              send_content=result.learn_list[flag-col+4]
                             idCell.innerHTML="<button class='btn btn-primary' data-bs-toggle='modal' data-bs-target='#delete_chat' onclick=deletechat('"+result.learn_list[flag-col]+"','"+ send_name+"','"+send_content+"') >删除记录</button>";
                             learnttr.appendChild(idCell);
                           }
                           else
                           {
                             var idCell=document.createElement('td');
                             idCell.setAttribute('style','display: inline-block;white-space: nowrap;width: 100px;overflow: hidden;text-overflow:ellipsis;')
                             idCell.innerHTML=result.learn_list[flag];
                             learnttr.appendChild(idCell);
                             flag=flag+1;
                           }
                        }
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
function deletechat(chat_id,send_name,send_content)
{
   console.log(send_name);
    $('#delete_chat_id').text(parseInt(chat_id));
    $('#send_name').text(send_name);
    $('#delete_chat_content').text(send_content);
}
function delete_chat()
{
  var chat_id=$('#delete_chat_id').text();
  $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/delete_chat_id/" ,//url
            data: {'chat_id':chat_id},
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
function deleteallchat(group_id)
{
    $('#delete_group_id').text(group_id);
}
function delete_allchat()
{
  var group_id=$('#delete_group_id').text();
  $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/delete_alltalk/" ,//url
            data: {'group_id':group_id},
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