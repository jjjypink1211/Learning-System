$(function(){
$("button").click(function()
{
   var id=$(this).attr("id");
   if(id=='yulan')
   {
        displaydata();
   }
   else if(id=='tijiaoshuju')
   {
      //文件提交到服务器
   }
   else if(id=='close1'){}else if(id=='close2'){}else if(id=='close3'){}else if(id=='close'){}
   else if(id=='sjksh')
   {
        dataview();
   }
   else if(id=='dataview')
   {
      submitinfo();
   }
   else
   {
     //alert(id);
     groupdetail(id);
   }
})

})
function groupdetail(group_id)
{
 var csrf = $('input[name="csrfmiddlewaretoken"]').val();
  $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/groupdetail/" ,//url
            data: {'group_id': group_id,'csrfmiddlewaretoken': csrf},
            dataType: 'json',
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                    var memtbody=document.getElementById("memdetail");//获得tbody标签
                    //先清空
                   $("#memdetail").html("");
                    for(var i=0;i<result.data.length;i++)
                    {
                        var memtr=document.createElement('tr');
                        var newmem1=document.createElement('td');
                        newmem1.innerHTML=result.data[i]['task_id'];
                        memtr.appendChild(newmem1);
                        var newmem2=document.createElement('td');
                        newmem2.innerHTML=result.data[i]['num'];
                        memtr.appendChild(newmem2);
                        var newmem3=document.createElement('td');
                        newmem3.innerHTML=result.data[i]['name'];
                        memtr.appendChild(newmem3);
                        var newmem4=document.createElement('td');
                        newmem4.innerHTML=result.data[i]['group_role'];
                        memtr.appendChild(newmem4);
                        var newmem5=document.createElement('td');
                        newmem5.innerHTML=result.data[i]['task_type'];
                        memtr.appendChild(newmem5);
                        var newmem6=document.createElement('td');
                        newmem6.innerHTML=result.data[i]['task_content'];
                        memtr.appendChild(newmem6);
                        var newmem7=document.createElement('td');
                        newmem7.innerHTML=result.data[i]['start_time'];
                        memtr.appendChild(newmem7);
                        var newmem8=document.createElement('td');
                        newmem8.innerHTML=result.data[i]['end_time'];
                        memtr.appendChild(newmem8);
                        var newmem9=document.createElement('td');
                        if(result.data[i]['is_finish'])
                        {
                            newmem9.innerHTML="<span class=\"badge bg-success\">"+"已完成"+"</span>";
                        }
                        else
                        {
                            newmem9.innerHTML="<span class=\"badge bg-danger\">"+"未完成"+"</span>";
                        }
                        memtr.appendChild(newmem9);
                         var newmem10=document.createElement('td');
                        if(result.data[i]['is_overtime'])
                        {
                            newmem10.innerHTML="<span class=\"badge bg-info\">"+"未超时"+"</span>";
                        }
                        else
                        {
                            newmem10.innerHTML="<span class=\"badge bg-danger\">"+"已超时"+"</span>";
                        }
                        memtr.appendChild(newmem10);
                        memtbody.appendChild(memtr);
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
                console.log(result);
                if(result.learn_list[3]=="开始作答时间")
                {
                         var mark=3;
                        for(var i=0;i<result.learn_list.length;i++)
                        {
                           mark=mark+result.cols;
                           if(mark>result.learn_list.length)
                           {
                              break;
                           }
                           result.learn_list[mark]=new Date(parseInt(result.learn_list[mark])).format("yyyy-MM-dd hh:mm:ss");
                        }

                }

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
                console.log(result);

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
 var y_list_time;
 var y_list_time1;
 var y_list_time2;//时间格式
 var x_name='';
 var y_name='';
 var pic1;
 var pic2;
  var pic3;
 function time_count(list_time)
 {
   var time_count=new Array();
   var time_mark=new Array();
   var flag=0;
   var flag_mark=false;

    for(var i=0;i<list_time.length;i++)
    {
        for(var j=0;j<list_time.length;j++)
        {
          if(time_mark[j]==false)
          {
            continue;//跳过
          }
          if(list_time[i]==list_time[j])
          {
             flag++;
             time_mark[j]=flag_mark;//标记已检查
          }
        }
        calender={'cale':list_time[i],'count':flag}
        if(flag==0)
        {
              continue;
        }
        time_count.push(calender);
        flag=0;
    }
    return time_count;
 }
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
                      y_list_dur=new Array();
                     for(var i=0;i<y_list.length;i++)
                          {
                             var duration=y_list[i].split(':')
                             var seconds=parseInt(duration[0])*60*60+parseInt(duration[1])*60+parseInt(duration[2]);
                             //console.log();
                             y_list_dur[i]=seconds;
                          }
                          console.log(y_list_dur);
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
                      addbarchart(y_list_dur,max,min);
                   }
                   if(format==2)
                   {
                      //姓名+开始作答时间
                     // 用法：
                     y_list_time=new Array();
                     y_list_time1=new Array();
                     y_list_time2=new Array();
                     for(var i=0;i<y_list.length;i++)
                     {
                         var time2 = new Date(parseInt(y_list[i])).format("yyyy-MM-dd hh:mm:ss");
                         var time3 = new Date(parseInt(y_list[i]));
                         var time1 = new Date(parseInt(y_list[i])).format("yyyy-MM-dd");
                          y_list_time[i]=time2;
                          y_list_time1[i]=time1;
                          y_list_time2[i]=time3;
                     }
                     let max = y_list[0];
                         let max_id=0;
                            for (let i = 0; i < y_list.length - 1; i++) {
                               if(max < y_list[i+1])
                                {
                                   max_id=i+1;
                                }
                                max = max < y_list[i+1] ? y_list[i+1] : max
                            }
                          //console.log(max+x_list[max_id]);
                        let min = y_list[0];
                         let min_id=0;
                            for (let i = 0; i < y_list.length - 1; i++) {
                               if(min > y_list[i+1])
                                {
                                   min_id=i+1;
                                }
                                min = min > y_list[i+1] ? y_list[i+1] : min
                            }
                            //设置最大值
                      $("#data_max").text("最晚"+y_name);
                      $("#MAX").text(y_list_time[max_id]);
                      $("#x_name1").text(x_list[max_id]);
                      //设置最小值
                      $("#data_min").text("最早"+y_name);
                      $("#MIN").text(y_list_time[min_id]);
                      $("#x_name2").text(x_list[min_id]);
                      var Count=time_count(y_list_time1);
                      $("#chart_title").text(y_name+"各时段分布人数");
                      //判断出学生选择哪些时段进行作答
                      var Day_count=setDay(y_list_time2);
                      //设置均值
                      $("#data_mean").text("作答时段分布");
                      $("#MEAN").text(mean_time);
                      var content="";
                      for(var i=0;i<Day_count.length;i++)
                      {
                         content=content+Day_count[i]['status']+": "+Day_count[i]['count']+"人"+"<br />";
                      }

                      $("#MEAN").html(content);
                      addareachart(Count);

                   }
                   if(format==3)
                   {
                      //姓名+开始学习时间
                     y_list_calender=new Array();
                     y_list_calender_split=new Array();
                     y_list_calender_split2=new Array();
                     y_list_time=new Array();
                     y_list_time2=new Array();

                     for(var i=0;i<y_list.length;i++)
                     {
                         y_list_calender[i]=y_list[i].split(' ');
                         y_list_time[i]=y_list_calender[i][0];
                         y_list_calender_split[i]=y_list_calender[i][0].split('-');
                         y_list_calender_split2[i]=y_list_calender[i][1].split(':');
                         var cale=new Date(
                         parseInt(y_list_calender_split[i][0]),
                         parseInt(y_list_calender_split[i][1])-1,
                         parseInt(y_list_calender_split[i][2]),
                         parseInt(y_list_calender_split2[i][0]),
                         parseInt(y_list_calender_split2[i][1]),0
                         );
                         //y_list_time2=cale;
                         //console.log(i);
                         //console.log(cale);
                         y_list_calender[i]=cale;
                     }
                     let max = y_list_calender[0];
                         let max_id=0;
                            for (let i = 0; i < y_list_calender.length - 1; i++) {
                               if(max < y_list_calender[i+1])
                                {
                                   max_id=i+1;
                                }
                                max = max < y_list_calender[i+1] ? y_list_calender[i+1] : max
                            }
                          //console.log(max+x_list[max_id]);
                        let min = y_list_calender[0];
                         let min_id=0;
                            for (let i = 0; i < y_list_calender.length - 1; i++) {
                               if(min > y_list_calender[i+1])
                                {
                                   min_id=i+1;
                                }
                                min = min > y_list_calender[i+1] ? y_list_calender[i+1] : min
                            }
                            //设置最大值
                      $("#data_max").text("最晚"+y_name);
                      $("#MAX").text(y_list[max_id]);
                      $("#x_name1").text(x_list[max_id]);
                      //设置最小值
                      $("#data_min").text("最早"+y_name);
                      $("#MIN").text(y_list[min_id]);
                      $("#x_name2").text(x_list[min_id]);
                      console.log(y_list_time);
                      var Count=time_count(y_list_time);
                      console.log(Count);
                      $("#chart_title").text(y_name+"各时段分布人数");
                      //判断出学生选择哪些时段进行作答
                      var Day_count=setDay(y_list_calender);
                      //设置均值
                      $("#data_mean").text("作答时段分布");
                      $("#MEAN").text(mean_time);
                      var content="";
                      for(var i=0;i<Day_count.length;i++)
                      {
                         content=content+Day_count[i]['status']+": "+Day_count[i]['count']+"人"+"<br />";
                      }

                      $("#MEAN").html(content);
                      addareachart(Count);

                   }
                   if(format==4)
                   {
                      //姓名+得分
                      y_list_float=new Array();
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
function setDay(time)
{
  var days=new Array();
  for(var i=0;i<time.length;i++)
  {
    var hours=time[i].getHours();//获取小时
    if(hours>=6&&hours<11)
    {
       var times={'time':time[i].format("yyyy-MM-dd hh:mm:ss"),'status':"上午(6~11)"};
       days.push(times);

    }else if(hours>=11&&hours<13)
    {
       var times={'time':time[i].format("yyyy-MM-dd hh:mm:ss"),'status':"中午(11~13)"};
       days.push(times);
    }else if(hours>=13&&hours<18)
    {
       var times={'time':time[i].format("yyyy-MM-dd hh:mm:ss"),'status':"下午(13~18)"};
       days.push(times);
    }else if(hours>=18&&hours<24)
    {
       var times={'time':time[i].format("yyyy-MM-dd hh:mm:ss"),'status':"晚上(18~24)"};
       days.push(times);

    }else if(hours>=0&&hours<6)
    {
       var times={'time':time[i].format("yyyy-MM-dd hh:mm:ss"),'status':"凌晨(0~6)"};
       days.push(times);
    }
  }
   var days_count=new Array();
   var days_mark=new Array();
   var flag=0;
   var flag_mark=false;

    for(var i=0;i<days.length;i++)
    {
        for(var j=0;j<days.length;j++)
        {
          if(days_mark[j]==false)
          {
            continue;//跳过
          }
          if(days[i]['status']==days[j]['status'])
          {
             flag++;
             days_mark[j]=flag_mark;//标记已检查
          }
        }
        calender={'status':days[i]['status'],'count':flag}
        if(flag==0)
        {
              continue;
        }
        days_count.push(calender);
        flag=0;
    }
  return days_count;
}
function addcharts( ) {
    checkcharts();
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
    pic1=chart1;
    chart1.render();
}
function addbarchart(y_list_dur,max,min) {
   checkcharts();
   backgroundColor=["rgba(255, 99, 132, 0.2)", "rgba(255, 159, 64, 0.2)", "rgba(255, 205, 86, 0.2)", "rgba(75, 192, 192, 0.2)", "rgba(54, 162, 235, 0.2)", "rgba(153, 102, 255, 0.2)", "rgba(201, 203, 207, 0.2)"];
   Count=parseInt(x_list.length/backgroundColor.length)-1;
   backgroundColor1=new Array();
   borderColor=new Array();
  for(var i=0;i<y_list_dur.length;i++)
  {
     if(y_list_dur[i]==max)
     {
         backgroundColor1.push("rgba(255, 99, 132, 0.2)");
         borderColor.push("rgba(255, 99, 132, 0.2)");

     }else if(y_list_dur[i]==min)
     {
        backgroundColor1.push("rgba(75, 192, 192, 0.2)");
       borderColor.push("rgba(75, 192, 192, 0.2)");

     }else
     {
       backgroundColor1.push("rgba(255, 205, 86, 0.2)");
       borderColor.push("rgba(255, 205, 86, 0.2)");
     }
  }
   pic2=new Chart(
   document.getElementById("chartjs2"),
   {
   "type": "bar",
   "data": {
      "labels": x_list,
      "datasets": [{
      "label": y_name,
      "data": y_list_dur,
      "fill": false,
      "backgroundColor": backgroundColor1,
       "borderColor": borderColor,
       "borderWidth": 1 }] },
        "options":
        { "scales":
           { "yAxes": [{ "ticks": { "beginAtZero": true } }] } } });

}
function comparecale(cale,people)
{
  var tmp_cale;
  var tmp_people;
  var date1=new Date(cale[0].replace(/-/g,"\/"));
  var date2=new Date(cale[1].replace(/-/g,"\/"));
 //冒泡排序
 for(var i=0;i<cale.length;i++)
 {
   for(var j=0;j<cale.length-1-i;j++)
   {
      var date1=new Date(cale[j].replace(/-/g,"\/"));
      var date2=new Date(cale[j+1].replace(/-/g,"\/"));
      if(date1>date2)
      {
         tmp_cale=cale[j];
         cale[j]=cale[j+1];
         cale[j+1]=tmp_cale;
         tmp_people=people[j];
         people[j]=people[j+1];
         people[j+1]=tmp_people;
      }
   }
 }
}
function checkcharts()
{
 if(pic1)
  {
    pic1.destroy();
  }
  if(pic2)
  {
    pic2.destroy();

  }if(pic3)
  {
    pic3.destroy();
  }
}
function addareachart(count)
{
   checkcharts();
  var people =new Array();
  var cale=new Array();
  for(var i=0;i<count.length;i++)
  {
    people[i]=count[i]['count'];
    cale[i]=count[i]['cale'];
  }
  //日期比较
   comparecale(cale,people);
var options2 = {
        chart: {
            height: 350,
            type: 'area',
        },
        dataLabels: {
            enabled: false
        },
        stroke: {
            curve: 'smooth'
        },
        series: [{
            name: '各日期人数',
            data: people,
        }, ],

        xaxis: {
            type: 'datetime',
            categories: cale,
            labels: {
                style: {
                    colors: 'rgba(94, 96, 110, .5)'
                }
            }
        },
        tooltip: {
            x: {
                format: 'yy/MM/dd'
            },
        },
        grid: {
            borderColor: 'rgba(94, 96, 110, .5)',
            strokeDashArray: 4
        }
    }

    var chart2 = new ApexCharts(
        document.querySelector("#apex3"),
        options2
    );
    pic3=chart2;
    chart2.render();
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
