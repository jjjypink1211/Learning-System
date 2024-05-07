$(document).ready(function() {
    $.ajax({
            type: "GET",//方法类型
            dataType: "json",//预期服务器返回的数据类型
            url: "/statistics/" ,//url
            success: function(data) {
                console.log(data);//打印服务端返回的数据(调试用)
                str = "<tr><td>" + "总数" + 
                "</td><td>" + data.student +
	            "</td><td>" + data.admin +
	            "</td><td>" + data.user +
	            "</td></tr>";
	            //追加到table中
	            $("#statislist").append(str);
                
            },
            error : function() {
                alert("异常！");
            }
        });
});