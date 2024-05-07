$(function ()
{
    // 获取组间互评数据
        const groups_list= JSON.parse(document.getElementById('groups_list').textContent);
        const titles_list= JSON.parse(document.getElementById('titles_list').textContent);
        const group_list= JSON.parse(document.getElementById('group_list').textContent);
        //小组多元综合评价
        const group_multiple= JSON.parse(document.getElementById('group_multiple').textContent);
        const multi_title_list= JSON.parse(document.getElementById('multi_title_list').textContent);
        drawcharts(group_multiple,multi_title_list)
      for(var j=0;j<groups_list.length;j++)
      {
           var eva_group=new Array();//评价

           var score_list=new Array();//评价
           var data_list=new Array();//评价
           var title_list=new Array();//评价
           for(var i=0;i<group_list.length;i++)
           {
              var group_id=group_list[i].group_id;
              if (typeof(groups_list[j][group_id]) != "undefined")
                {
                    //console.log("来自评价"+group_id);//评价的
                    eva_group.push(group_id);
                    var score=new Array();//评价
                    //console.log(groups_list[j][group_id]);
                    for(var k=0;k<titles_list.length;k++)
                        {
                           title=titles_list[k].evaluate_item;
                           //console.log(title+groups_list[j][group_id][title]);
                           score.push(groups_list[j][group_id][title])
                        }
                    score_list.push(score);
                }
            }
            //console.log("评价小组"+groups_list[j].group_id);//受到评价小组
            //console.log(eva_group);
            //console.log(score_list);
            for(var k=0;k<eva_group.length;k++)
            {
               data_list.push(
                       {
                         'name':'第'+eva_group[k]+'组',
                         'data': score_list[k]
                       }

               );
            }
            for(var k=0;k<titles_list.length;k++)
            {
               title_list.push(titles_list[k].evaluate_item)
            }
            var name='#apex_'+groups_list[j].group_id;
            //console.log(data_list);

            makechart(name,data_list,title_list);

      }
});
function makechart(name,data_list,title_list)
{

 var options3 = {
        chart: {
            height: 400,
            type: 'bar',
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: '55%',
                endingShape: 'rounded',
                borderRadius: 10
            },
        },
        dataLabels: {
            enabled: false
        },
        stroke: {
            show: true,
            width: 2,
            colors: ['transparent']
        },
        series: data_list,
        xaxis: {
            categories: title_list,
            labels: {
                style: {
                    colors: 'rgba(94, 96, 110, .5)'
                }
            }
        },
        yaxis: {
            title: {
                text: '评价得分'
            }
        },
        fill: {
            opacity: 1

        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return  val + "(分/时长)"
                }
            }
        },
        grid: {
            borderColor: 'rgba(94, 96, 110, .5)',
            strokeDashArray: 4
        }
    }

    var chart3 = new ApexCharts(
        document.querySelector(name),
        options3
    );

    chart3.render();



}
function detail_groupinfo(group_id)
{
  $.ajax({
        //几个参数需要注意一下
            type: "GET",//方法类型
            url: "/detail_groupinfo/?group_id="+group_id ,//url
            success: function (result) {},
            error : function() {
                alert("异常！");
            }
        });




}
function drawcharts(group_multiple,multi_title_list)
{
   dataset=data_create(group_multiple);
   title=new Array();
   for(var i=0;i<multi_title_list.length;i++)
   {
      title.push(multi_title_list[i].evaluate_item);
   }
    new Chart(document.getElementById("chartjs3"),
        {
        "type": "radar",
        "data": {
         "labels": title,
        "datasets":dataset
        },
        "options": {
        "elements":
         { "line":
          { "tension": 0, "borderWidth": 3 } } }

          });


}
function data_create(group_multiple)
{
  var backgroundColor= ["rgba(255, 99, 132, 0.2)", "rgba(255, 159, 64, 0.2)", "rgba(255, 205, 86, 0.2)", "rgba(75, 192, 192, 0.2)", "rgba(54, 162, 235, 0.2)", "rgba(153, 102, 255, 0.2)", "rgba(201, 203, 207, 0.2)","rgba(201, 90, 158, 0.2)","rgba(201, 67, 124, 0.2)","rgba(201, 177, 134, 0.2)"]
   var data=[];
   for(var i=0;i<group_multiple.length;i++)
   {
          var newdata={
        "label": group_multiple[i].group_name,
        "data": group_multiple[i].score_list,
        "fill": true,
        "backgroundColor": backgroundColor[i],
        "borderColor": backgroundColor[i],
        "pointBackgroundColor": backgroundColor[i],
        "pointBorderColor": "#fff",
         "pointHoverBackgroundColor": "#fff",
        "pointHoverBorderColor": backgroundColor[i] };
         data.push(newdata);
   }
return data;
}