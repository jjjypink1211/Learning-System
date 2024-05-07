$(function ()
{
   const self_eva= JSON.parse(document.getElementById('self_eva').textContent);
   const title_list= JSON.parse(document.getElementById('title_list').textContent);
   const inter_eva= JSON.parse(document.getElementById('inter_eva').textContent);
   const inter_title_list= JSON.parse(document.getElementById('inter_title_list').textContent);
   const chat_data= JSON.parse(document.getElementById('chat_data').textContent);
   console.log(chat_data);
        title=new Array();
        for(var i=0;i<title_list.length;i++)
        {
            title.push(title_list[i].evaluate_item)
        }

   self_radar(title,self_eva);
   inter_title=new Array();
   for(var i=0;i<inter_title_list.length;i++)
        {
            inter_title.push(inter_title_list[i].evaluate_item)
        }
   dataset=data_create(inter_eva);
   inter_radar(inter_title,dataset);

});
function inter_radar(inter_title,dataset)
{
   new Chart(document.getElementById("chartjs3"),
	{
	"type": "radar",
	"data": {
	 "labels": inter_title,
	"datasets":dataset
	},
	"options": {
	"elements":
	 { "line":
	  { "tension": 0, "borderWidth": 3 } } }

	  });
}
function self_radar(title,self_eva)
{
 var options7 = {
        series: self_eva,
        chart: {
            height: 350,
            type: 'radar',
        },
        dataLabels: {
            enabled: true
        },
        plotOptions: {
            radar: {
                size: 140,
                polygons: {
                    strokeColors: '#e9e9e9',
                    fill: {
                        colors: ['#f8f8f8', '#fff']
                    }
                }
            }
        },
        title: {
            text: '成员自我评价'
        },
        colors: ['#FF4560'],
        markers: {
            size: 4,
            colors: ['#fff'],
            strokeColor: '#FF4560',
            strokeWidth: 2,
        },
        tooltip: {
            y: {
                formatter: function (val) {
                    return val
                }
            }
        },
        xaxis: {
            categories: title
        },
        yaxis: {
            tickAmount: 5,
            labels: {
                formatter: function (val, i) {
                    if (i % 2 === 0) {
                        return val
                    } else {
                        return ''
                    }
                }
            }
        }
    };

    var chart7 = new ApexCharts(document.querySelector("#apex7"), options7);
    chart7.render();
}
function data_create(inter_eva)
{
  var backgroundColor= ["rgba(255, 99, 132, 0.2)", "rgba(255, 159, 64, 0.2)", "rgba(255, 205, 86, 0.2)", "rgba(75, 192, 192, 0.2)", "rgba(54, 162, 235, 0.2)", "rgba(153, 102, 255, 0.2)", "rgba(201, 203, 207, 0.2)"]
   var data=[];
   for(var i=0;i<inter_eva.length;i++)
   {
      var newdata={
	"label": inter_eva[i].name,
	"data": inter_eva[i].data,
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