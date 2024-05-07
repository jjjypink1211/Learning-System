
$(document).ready(function() {
    $.ajax({
            type: "GET",//方法类型
            dataType: "json",//预期服务器返回的数据类型
            url: "/maxpjid/" ,//url
            success: function (result) {
                console.log(result);//打印服务端返回的数据(调试用)
                if (result.resultCode == 200) {
                    $('#id').attr("value",result.max);
                }
                if(result.resultCode==-1){
                    alert("序号获取失败");
                }
                
            },
            error : function() {
                alert("异常！");
            }
        });
    $('#defaultForm').bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            bh: {
                group: '.col-sm-4',
                validators: {
                    notEmpty: {
                        message: '评价编号不能为空'
                    }
                }
            },

           evalute_type: {
                validators: {
                    notEmpty: {
                        message: '评价类型不能为空'
                    }
                }
            },
            pj_content: {
                validators: {
                    notEmpty: {
                        message: '评价内容不能为空'
                    }
                }
            }
        }
    });

    $('#resetBtn').click(function() {
        $('#defaultForm').data('bootstrapValidator').resetForm(true);
    });
    Date.prototype.format = function(fmt)
   { 
　　var o = {
　　　　"M+" : this.getMonth()+1, //月份
　　　　"d+" : this.getDate(), //日
　　　　"h+" : this.getHours()%12 == 0 ? 12 : this.getHours()%12, //小时
　　　　"H+" : this.getHours(), //小时
　　　　"m+" : this.getMinutes(), //分
　　　　"s+" : this.getSeconds(), //秒
　　　　"q+" : Math.floor((this.getMonth()+3)/3), //季度
　　　　"S" : this.getMilliseconds() //毫秒
　　   };
　　  if(/(y+)/.test(fmt))
　　　　   fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));
　　   for(var k in o)
　　　　   if(new RegExp("("+ k +")").test(fmt))
　　   fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));
　　   return fmt;
   } 
    var date1=new Date().format("yyyy-MM-dd");
    var date2 = new Date().format("yyyy-MM-dd HH:mm:ss");
    console.log(date2);
    //$('#ds_rq').val(date);
    $('#ds_rq').attr("value",date2);
    $('#ds_rq').attr("text",date2);
});