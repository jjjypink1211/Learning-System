$(function () {

    //1.初始化Table
    var oTable = new TableInit();
    oTable.Init();

    //2.初始化Button的点击事件
    var oButtonInit = new ButtonInit();
    oButtonInit.Init();

});


var TableInit = function () {
    var oTableInit = new Object();
    //初始化Table
    oTableInit.Init = function () {
        $('#tb_departments').bootstrapTable({
            url: '/pj/',         //请求后台的URL（*）
            method: 'get',                      //请求方式（*）
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: true,                   //是否显示分页（*）
            sortable: false,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            queryParams: oTableInit.queryParams,//传递参数（*）
            sidePagination: "server",           //分页方式：client客户端分页，server服务端分页（*）
            pageNumber:1,                       //初始化加载第一页，默认第一页
            pageSize: 10,                       //每页的记录行数（*）
            pageList: [10, 25, 50, 100],        //可供选择的每页的行数（*）
            search: false,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: true,                  //是否显示所有的列
            showRefresh: true,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            height: 500,                        //行高，如果没有设置height属性，表格自动根据记录条数觉得表格高度
            uniqueId: "ID",                     //每一行的唯一标识，一般为主键列
            showToggle:true,                    //是否显示详细视图和列表视图的切换按钮
            cardView: false,                    //是否显示详细视图
            detailView: false,                   //是否显示父子表
            columns: [{
                checkbox: true
            }, {
                    title: '序号',
                    field: 'id',

                }, {
                    title: '评价编号',
                    field: 'evaluate_id',

                }, {
                    title: '评价类型',
                    field: 'evaluate_type',

                }, {
                    title: '评价内容',
                    field: 'evaluate_item',
                    //formatter: formatSex
                }, {
                    title: '评价权重',
                    cellStyle: formatTableUnit,
                    formatter: paramsMatter,
                    field: 'evaluate_weight'
                },  ]
        });
    };
	// 定义删除、更新按钮
            function option(value, row, index) {
                var htm = "";
                htm += '<button id="dupdevice" deviceId="' + value +
                    '" onclick="updDevice(' + value + ')">编辑</button>'
                return htm;
            }

            //表格超出宽度鼠标悬停显示td内容
            function paramsMatter(value, row, index) {
                var span = document.createElement("span");
                span.setAttribute("title", value);
                span.innerHTML = value;
                return span.outerHTML;
            }
            //td宽度以及内容超过宽度隐藏
            function formatTableUnit(value, row, index) {
                return {
                    css: {
                        "white-space": "nowrap",
                        "text-overflow": "ellipsis",
                        "overflow": "hidden",
                        "max-width": "60px"
                    }
                }
            }

            // 格式化性别"sex": 0,是女  "sex": 1,是男
            function formatSex(value, row, index) {
                return value == 1 ? "男" : "女";
            }
            // 格式化在离厂//"isLeave": 0,是离场，"isLeave": 1,是在场
            function formatIsLeave(value, row, index) {
                return value == 1 ? "离厂" : "在厂";
            }

            // 格式化时间
            function formatTime(value, row, index) {
                var date = new Date();
                date.setTime(value);
                var month = date.getMonth() + 1;
                var hours = date.getHours();
                if(hours < 10)
                    hours = "0" + hours;
                var minutes = date.getMinutes();
                if(minutes < 10)
                    minutes = "0" + minutes;
                var time = date.getFullYear() + "-" + month + "-" + date.getDate() +
                    " " + hours + ":" + minutes;
                return time;
            }

            // 格式化访问理由 "viewReason": 1是面试,2是开会，3是拜访客户，4是项目实施
            function formatReason(value, row, index) {
                var str;
                switch(value) {
                    case 1:
                        str = "面试";
                        break;
                    case 2:
                        str = "开会";
                        break;
                    case 3:
                        str = "拜访客户";
                        break;
                    case 4:
                        str = "项目实施";
                        break;
                    default:
                        str = "其他";
                }
                return str;
            }
            // 删除按钮事件
            $("#btn_delete").on("click", function() {

                if(!confirm("是否确认删除？"))
                    return;
                var rows = $("#tb_departments").bootstrapTable('getSelections'); // 获得要删除的数据
                if(rows.length == 0) { // rows 主要是为了判断是否选中，下面的else内容才是主要
                    alert("请先选择要删除的记录!");
                    return;
                } else {
                    var ids = new Array(); // 声明一个数组
                    $(rows).each(function() { // 通过获得别选中的来进行遍历
                        ids.push(this.BookID); // cid为获得到的整条数据中的一列
                    });
                    //后端删除的方法
                    deleteMs(ids)
                }

            })
            // 删除访客,删除数据库内容，刷新表格即可删除
            function deleteMs(ids) {
                var arr=ids;
                $.ajax({
                    url: "/deleteUser",
                    //url: "/deleteUser",
                    data:JSON.stringify(ids),
                    traditional:true,
                    dataType: "json",
                    type: "post",
                    success: function(data) {
                        if(data > 0) {
                            msg(6, "操作成功")
                            $('tb_departments').bootstrapTable('refresh', {
                                url: basePath + '/caller/list'
                            });
                        }
                    }
                });
            }
             // 查询按钮事件
             $("#btn_query").on("click", function() {
                var cxlx=$('select[id=colSearch]')
                var cxnr=$('input[id=txt_search_statu]')
                var searchdata={cxlx:cxlx.val(),cxnr:cxnr.val()}
                if(cxlx.val().length==0 || cxnr.val().length==0){
                   alert("查询内容不能为空！！");
                   return;
                }else{
                    $.ajax({
                        url: '/pjquery?cxlx='+cxlx.val()+'&cxnr='+cxnr.val(),
                        traditional:true,
                        dataType: "json",
                        type: "get",
                        success: function(data) {
                            console.log(data.code)
                            if(data.code!=-1) {
                               console.log('到这儿')
                                var url='/pjquery?cxlx='+cxlx.val()+'&cxnr='+cxnr.val()
                                var opt = {
                                    url: url
                                };
                                console.log(opt.url)
                                $('#tb_departments').bootstrapTable('refresh', opt);
                            }else
                            {
                                alert("未查找到此记录!");
                                //$('tb_departments').bootstrapTable('refresh', {url:'/'});

                            }
                        }
                    });
                    // var url='/queryd?cxlx='+cxlx.val()+'&cxnr='+cxnr.val()
                    // var opt = {
                    //     url: url
                    // };
                    // // 带参数，刷新（加载新请求数据）
                    // $("#tb_departments").bootstrapTable('refresh', opt);
                    // // 不带参数，只刷新（重新加载数据）
                    // // $("#table").bootstrapTable('refresh');
                }
                
            })
             // 重置按钮事件
             $("#btn_refresh").on("click", function() {
                
                    var url='/pj/'
                    var opt = {
                        url: url
                    };
                    // 带参数，刷新（加载新请求数据）
                    $("#tb_departments").bootstrapTable('refresh', opt);
                    // 不带参数，只刷新（重新加载数据）
                    // $("#table").bootstrapTable('refresh');
                
            })
            // 编辑访客
            function updDevice(id) {
                alert("编辑")
            }
    
    return oTableInit;
};


var ButtonInit = function () {
    var oInit = new Object();
    var postdata = {};

    oInit.Init = function () {
        //初始化页面上面的按钮事件
    };
    return oInit;
};