$(function ()
{
        const group_data= JSON.parse(document.getElementById('group_data').textContent);
        const title_list= JSON.parse(document.getElementById('title_list').textContent);
        const member_weight= JSON.parse(document.getElementById('member_weight').textContent);
        const time_data= JSON.parse(document.getElementById('time_data').textContent);
        const task_finished= JSON.parse(document.getElementById('task_finished').textContent);
        const member_time_data= JSON.parse(document.getElementById('member_time_data').textContent);
        title=new Array();
        for(var i=0;i<title_list.length;i++)
        {
            title.push(title_list[i].evaluate_item)
        }
        var group_name=group_data.name;
         dataset=data_create(group_name,group_data);
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
	  var name_list=new Array();
	  var weight_list=new Array();
	  for(var i=0;i<member_weight.length;i++)
	  {
	    name_list.push(member_weight[i].name);
	    weight_list.push(member_weight[i].weight);
	  }
 new Chart(
      document.getElementById("chartjs4"),{ "type": "doughnut",
	"data": {
	"labels": name_list,
	"datasets": [{
	 "label": "My First Dataset",
	 "data": weight_list,
	"backgroundColor": ["rgb(255, 99, 132)", "rgb(54, 162, 235)", "rgb(255, 205, 86)","rgba(255, 159, 64)","rgba(75, 192, 192)"] }] } });
      var time_label=new Array();
      var times_data=new Array();
	   //console.log(time_data);
	  for(var i=0;i<time_data.length;i++)
	  {
	    time_label.push(time_data[i].group_id);
	    times_data.push(time_data[i].avg_time);
	  }
	  //console.log(time_label)
   new Chart(document.getElementById("chartjs2"),
	{ "type": "bar",
	"data":
	{ "labels": time_label,
	"datasets": [{ "label": "各小组平均学习时长(分钟)",
	"data": times_data,
	"fill": false,
	"backgroundColor": ["rgba(255, 99, 132, 0.2)", "rgba(255, 159, 64, 0.2)", "rgba(255, 205, 86, 0.2)", "rgba(75, 192, 192, 0.2)", "rgba(54, 162, 235, 0.2)", "rgba(153, 102, 255, 0.2)", "rgba(201, 203, 207, 0.2)"],
	"borderColor": ["rgb(255, 99, 132)", "rgb(255, 159, 64)", "rgb(255, 205, 86)", "rgb(75, 192, 192)", "rgb(54, 162, 235)", "rgb(153, 102, 255)", "rgb(201, 203, 207)"], "borderWidth": 1 }] },
	"options":
	{ "scales":
	{ "yAxes":
	 [{ "ticks": { "beginAtZero": true } }] } } });
	 //小组成员任务完成量
	 console.log(task_finished);
	 task_status=['已完成','未完成','超时完成','超时未完成'];
	 task_series=new Array();
	 name_series=new Array();
	 for(var i=0;i<task_status.length;i++)
	  {
	     dataset=new Array();
	   for(var j=0;j<task_finished.length;j++)
	   {
	       dataset.push(task_finished[j][task_status[i]])
       }
       task_series.push({
       name: task_status[i],
       data: dataset
       })
	  }
	  for(var j=0;j<task_finished.length;j++)
	   {
	       name_series.push(task_finished[j].name);
       }
	 drawchart(name_series,task_series);
	 console.log(member_time_data);
	 drawchart_column(member_time_data.data,member_time_data.name_list);

});
function drawchart_column(dataset,name_list)
{
      var options3 = {
        chart: {
            height: 350,
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
        series: dataset,
        xaxis: {
            categories: name_list,
            labels: {
                style: {
                    colors: 'rgba(94, 96, 110, .5)'
                }
            }
        },
        yaxis: {
            title: {
                text: '所花时间 (分钟)'
            }
        },
        fill: {
            opacity: 1

        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return   val + " 分钟"
                }
            }
        },
        grid: {
            borderColor: 'rgba(94, 96, 110, .5)',
            strokeDashArray: 4
        }
    }

    var chart3 = new ApexCharts(
        document.querySelector("#apex3"),
        options3
    );

    chart3.render();
}
function drawchart(name_series,task_series)
{
 var options4 = {
        series: task_series,
        chart: {
            type: 'bar',
            height: 350,
            stacked: true,
            stackType: '100%'
        },
        plotOptions: {
            bar: {
                horizontal: true,
            },
        },
        stroke: {
            width: 1,
            colors: ['#fff']
        },
        title: {
            text: '小组成员任务完成量'
        },
        xaxis: {
            categories: name_series,
        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return val + "项任务"
                }
            }
        },
        fill: {
            opacity: 1

        },
        legend: {
            position: 'top',
            horizontalAlign: 'left',
            offsetX: 40
        },
        grid: {
            borderColor: 'rgba(94, 96, 110, .5)',
            strokeDashArray: 4
        }
    };
    var chart4 = new ApexCharts(document.querySelector("#apex4"), options4);
    chart4.render();


}
function data_create(group_name,group_data)
{
  var backgroundColor= ["rgba(255, 99, 132, 0.2)", "rgba(255, 159, 64, 0.2)", "rgba(255, 205, 86, 0.2)", "rgba(75, 192, 192, 0.2)", "rgba(54, 162, 235, 0.2)", "rgba(153, 102, 255, 0.2)", "rgba(201, 203, 207, 0.2)"]
   var data=[];
   for(var i=0;i<group_name.length;i++)
   {
      var newdata={
	"label": group_name[i].name,
	"data": group_data[group_name[i].num],
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

