
const group_list = JSON.parse(document.getElementById('group_list').textContent);
console.log(group_list);

function calculate(group_id)
{
  var name1="final_score_"+group_id;
  var name2="multi_mark_"+group_id;
  var name3="group_score_"+group_id;
  var multi_score = $('input[name="'+name2+'"]').val();
  var final_score = $('input[name="'+name1+'"]').val();

  if (isNaN(parseFloat(final_score)))
  {
    alert("分数格式错误！！");
    return;
  }
  else
  {
    final_score=parseFloat(final_score);
     if ( final_score < 0 || final_score > 100 )
     {
         alert("输入的数字需要大于0且小于100");
         return;

     }else
     {
          end_score=final_score*0.6+multi_score*0.4;
          $("#"+name3+"").val(end_score.toFixed(2));
     }

  }


}
function submitgroupscore(group_id)
{
   var group_score = $('input[name="group_score"]').val();
   if (isNaN(parseFloat(group_score)))
      {
        alert("还没有计算出综合成绩！");
        return;
      }
       $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/submitfinalscore/" ,//url
            data: {'group_id': group_id,'group_score': group_score },
            dataType: 'json',
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                   $("#final_score").val('');
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
function submitstuscore(group_id)
{
var fileFlag=false
     $('#stu-file-group'+group_id).each(function(){
     if($(this).val()!=""){
        fileFlag=true;
     }
     })
     if(!fileFlag)
     {
       alert("请选择好文件!")
       return;
     }
     var obj = document.getElementById("stu-file-group"+group_id);
     if(obj.files.length>1)
     {
             alert("仅支持上传一个文件");
             return;

     }
     var stufile=$('#stu-file-group'+group_id)[0].files[0];
      //获取最后一个.的位置
      var filename=stufile.name;
      var index= filename.lastIndexOf(".");
      //获取后缀
      var ext = filename.substr(index+1);
         if(ext != 'xlsx' && ext != 'xls')
         {
            alert("请上传正确格式文件!");
             return;
          }
     var formdata=new FormData();
       formdata.append('stu_file',stufile);

                      $.ajax({
                        //几个参数需要注意一下
                            type: "POST",//方法类型
                            url: "/upload_stuscore/" ,//上传学生成绩
                            data: formdata,
                            processData:false,
                            contentType:false,
                            success: function (result) {
                                console.log(result)
                                if (result.resultCode == 200){
                                alert("导入成功!!");
                                  for(var i=0;i<result.data.length;i++)
                                  {
                                    if(result.data[i].group_score==0)
                                    {
                                       alert("第"+result.data[i].group_id+"小组未提交综合成绩，请提交成绩后再进行个人成绩计算");

                                    }else
                                    {
                                    //个人测验满分为25
                                       var score=result.data[i].group_score*0.6+result.data[i].score*4*0.4;
                                       $("#"+result.data[i].num).html(score.toFixed(2));

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
function submitselfscore(group_id)
{
 data=new Array();
for(var i=0;i<group_list.length;i++)
{
    if( group_list[i].group_id == group_id)
    {
       stu_list=group_list[i].stu_list;
       for(var j=0;j<stu_list.length;j++)
       {
           data.push({
           "num":stu_list[j].num,
           "score": $("#"+stu_list[j].num).text()
           })
       }
       console.log(data);
       $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/uploadselfscore/" ,//url
            data: {"submit_data":JSON.stringify(data)} ,
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
       break;
    }
}
}
function selfinput(group_id)
{
  for(var i=0;i<group_list.length;i++)
{
    if( group_list[i].group_id == group_id)
    {
       stu_list=group_list[i].stu_list;
       var form1=document.getElementById("selfinputForm");
       $('#selfinputForm').html('');
       var hh=document.createElement('h5');
       hh.setAttribute("id","group_num")
       hh.innerHTML=group_id;
       form1.appendChild(hh);
       for(var j=0;j<stu_list.length;j++)
       {
            var num = stu_list[j].num;
            var name=stu_list[j].name;
            console.log(name);
            var div1=document.createElement('div');
            div1.setAttribute("class","row mb-3");
            var label1=document.createElement('label');
            label1.setAttribute("class","col-sm-2 col-form-label");
            label1.innerHTML=name;
            var div2=document.createElement('div');
            div2.setAttribute("class","col-sm-10");
            var input1=document.createElement('input');
            input1.setAttribute("class","form-control");
            input1.setAttribute("id","selfinput_"+num);
            form1.appendChild(div1);
            div1.appendChild(label1);
            div1.appendChild(div2);
            div2.appendChild(input1);
       }
       break;
    }
}



}
function scoretijiao()
{
 var group_id=$("#group_num").text();
  data=new Array();
    for(var i=0;i<group_list.length;i++)
    {
        if( group_list[i].group_id == group_id)
        {
           stu_list=group_list[i].stu_list;
           for(var j=0;j<stu_list.length;j++)
           {
              var score=$("#selfinput_"+stu_list[j].num).val()

              if (isNaN(parseFloat(score)))
              {
                 alert("输入数据有误,请重新输入");
                 return ;
              }
              if (parseFloat(score)<0 || parseFloat(score)>100)
              {
                 alert("输入数值有误,请重新输入");
                 return ;
              }
               data.push({
               "num":stu_list[j].num,
               "score": score
               })
           }
           console.log(data);
           $.ajax({
            //几个参数需要注意一下
                type: "POST",//方法类型
                url: "/uploadselfscore/" ,//url
                data: {"submit_data":JSON.stringify(data)} ,
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
           break;
        }
    }
}