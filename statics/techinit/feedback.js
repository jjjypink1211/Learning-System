$(function () {
   var fbfileList = [];
   var feedback_files = document.getElementById("feedback_file");
   var fileListDisplay = document.getElementById('file-list-display');
    ValidatorUserInfo();
    feedback_files.addEventListener("change", function (event) {
            var fbfileList = [];
            console.log(feedback_files.files.length);
            for (var i = 0; i < feedback_files.files.length; i++) {
                fbfileList.push(feedback_files.files[i]);
            }
            renderFileList(fbfileList);
        });
        renderFileList = function (fbfileList) {
            fileListDisplay.innerHTML='';
            fbfileList.forEach(function (file, index) {
                var fileDisplayEl = document.createElement("p");
                fileDisplayEl.innerHTML = (index + 1) + ":" + file.name;
                fileListDisplay.appendChild(fileDisplayEl);
            })
        };
});
function ValidatorUserInfo(){
   $('#add_feedback').bootstrapValidator({
        message: 'This value is not valid',
        //提供输入验证图标提示
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        fields: {
            feedback_title: {
                message: '内容不能为空',
                validators: {
                    notEmpty: {
                        message: '内容不能为空'
                    },
                     stringLength: {
                         min: 2,
                         max: 255,
                         message: '内容长度必须在2到255之间'
                     },

                }
            },
            feedback_content: {
                message: '内容不能为空',
                validators: {
                    notEmpty: {
                        message: '反馈内容不能为空'
                    },

                }
            },
            feedback_type: {
                message: '选择无效',
                validators: {
                    notEmpty: {
                        message: '选择不能为空'
                    },
                       callback:{
                        message:'必须选择一个反馈类型',
                        callback:function(value,validator)
                        {
                          if(value == 0)
                          {
                             return false;
                          }else
                          {
                             return true;
                          }
                        }
                       }

                }
            },


        }
    })
}
function send_feedback()
{
  //验证销毁
     $("#add_feedback").data('bootstrapValidator').destroy();
     $('#add_feedback').data('bootstrapValidator', null);

     ValidatorUserInfo();

    $("#add_feedback").bootstrapValidator('validate');//提交验证
    if (!$("#add_feedback").data('bootstrapValidator').isValid()) {
        return
    }
     var fileList=[];
     var file_flag="有";
     var feedback_title=$('#feedback_title').val();
     var feedback_content=$('#feedback_content').val();
     var obj = document.getElementById("feedback_type"); //定位id
     var index = obj.selectedIndex; // 选中索引
     var feedback_type = obj.options[index].value; // 选中值
     var files=$('#feedback_file')[0].files;
     var formdata=new FormData();
     var csrf = $('input[name="csrfmiddlewaretoken"]').val();
     if(files.length == 0)
     {
        file_flag="无";
        formdata.append('csrfmiddlewaretoken',csrf);
        formdata.append('feedback_content',feedback_content);
        formdata.append('feedback_title',feedback_title);
        formdata.append('feedback_type',feedback_type);
        formdata.append('file_flag',file_flag);
        formdata.append('file_count',0);

     }
     else
     {

         for (var i = 0; i < files.length; i++) {
                fileList.push(files[i]);
            }
        formdata.append('csrfmiddlewaretoken',csrf);
        formdata.append('feedback_content',feedback_content);
        formdata.append('feedback_title',feedback_title);
        formdata.append('feedback_type',feedback_type);
        formdata.append('file_flag',file_flag);
        formdata.append('file_count',files.length);
        //formdata.append('feedback_file',files);
        fileList.forEach(function (file) {
                formdata.append('feedback_file', file, file.name);
            });

     }
          $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/addfeedbackmsg/" ,//url
            data: formdata,
            processData:false,
            contentType:false,
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                    alert(result.msg);
                    location.reload();

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
function reply_feedback()
{
  //验证销毁
     $("#add_feedback").data('bootstrapValidator').destroy();
     $('#add_feedback').data('bootstrapValidator', null);

     ValidatorUserInfo();

    $("#add_feedback").bootstrapValidator('validate');//提交验证
    if (!$("#add_feedback").data('bootstrapValidator').isValid()) {
        return
    }
     var fileList=[];
     var file_flag="有";
     var feedback_title=$('#feedback_title').val();
     var feedback_content=$('#feedback_content').val();
     var obj = document.getElementById("feedback_type"); //定位id
     var index = obj.selectedIndex; // 选中索引
     var feedback_type = obj.options[index].value; // 选中值
     var files=$('#feedback_file')[0].files;
     var num=document.getElementById('author_groupid').innerHTML;
     var formdata=new FormData();
     var csrf = $('input[name="csrfmiddlewaretoken"]').val();
     if(files.length == 0)
     {
        file_flag="无";
        formdata.append('csrfmiddlewaretoken',csrf);
        formdata.append('feedback_content',feedback_content);
        formdata.append('feedback_title',feedback_title);
        formdata.append('feedback_type',feedback_type);
        formdata.append('num',num);
        formdata.append('file_flag',file_flag);
        formdata.append('file_count',0);

     }
     else
     {

         for (var i = 0; i < files.length; i++) {
                fileList.push(files[i]);
            }
        formdata.append('csrfmiddlewaretoken',csrf);
        formdata.append('feedback_content',feedback_content);
        formdata.append('feedback_title',feedback_title);
        formdata.append('feedback_type',feedback_type);
        formdata.append('num',num);
        formdata.append('file_flag',file_flag);
        formdata.append('file_count',files.length);
        //formdata.append('feedback_file',files);
        fileList.forEach(function (file) {
                formdata.append('feedback_file', file, file.name);
            });

     }
          $.ajax({
        //几个参数需要注意一下
            type: "POST",//方法类型
            url: "/addreplyfeedbackmsg/" ,//url
            data: formdata,
            processData:false,
            contentType:false,
            success: function (result) {
                console.log(result)
                if (result.resultCode == 200) {
                    alert(result.msg);
                    $('#add_feedback')[0].reset();
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
Date.prototype.Format = function (fmt) { // author: meizz
  var o = {
    "M+": this.getMonth() + 1, // 月份
    "d+": this.getDate(), // 日
    "h+": this.getHours(), // 小时
    "m+": this.getMinutes(), // 分
    "s+": this.getSeconds(), // 秒
    "q+": Math.floor((this.getMonth() + 3) / 3), // 季度
    "S": this.getMilliseconds() // 毫秒
  };
  if (/(y+)/.test(fmt))
    fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
  for (var k in o)
    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
      return fmt;
}
