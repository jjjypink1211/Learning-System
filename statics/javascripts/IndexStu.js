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
            url: '/index/Stu',         //请求后台的URL（*）
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
                    title: '学生学号',
                    field: 'StuID',
                    visible: false
                }, {
                    title: '姓名',
                    field: 'stuName',

                }, {
                    title: '性别',
                    field: 'Sex',

                }, {
                    title: '证件号码',
                    field: 'ZJH',
                    //formatter: formatSex
                }, {
                    title: '联系电话',
                    cellStyle: formatTableUnit,
                    formatter: paramsMatter,
                    field: 'LXDH'
                }, {
                    title: '登记日期',
                    field: 'DJRQ',
                    formatter: formatTime,
                }, {
                    title: '有效期至',
                    field: 'YXQZ',
                    formatter: formatTime,
                }, {
                    title: '已借书数',
                    field: 'YJSS',
                    //formatter: formatReason
                }, ]
        });
    };
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
            // 格式化时间
            function formatTime(value, row, index) {
                var dateee = new Date(value).toJSON();
                var date = new Date(+new Date(dateee)+8*3600*1000).toISOString().replace(/T/g,' ').replace(/\.[\d]{3}Z/,'') ;
                return date;
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
                        url: '/index/querys?cxlx='+cxlx.val()+'&cxnr='+cxnr.val(),
                        //url: "/deleteUser",
                        traditional:true,
                        dataType: "json",
                        type: "get",
                        success: function(data) {
                            console.log(data.code)
                            if(data.code!=-1) {
                               console.log('到这儿1')
                               alert('查询成功！');
                                var url='/index/querys?cxlx='+cxlx.val()+'&cxnr='+cxnr.val()
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
                }
                
            })
             // 重置按钮事件
             $("#btn_refresh").on("click", function() {
                
                    var url='/index/Stu'
                    var opt = {
                        url: url
                    };
                    // 带参数，刷新（加载新请求数据）
                    $("#tb_departments").bootstrapTable('refresh', opt);
                    // 不带参数，只刷新（重新加载数据）
                    // $("#table").bootstrapTable('refresh');
                
            })
            // 查询登记日期按钮事件
            $("#btn_qurq").on("click", function() {
                var cxlx="DJRQ"
                var cxnr=$('input[id=txt_riqi]')
                var time=cxnr.val()+'.000000';
                var searchdata={cxnr:cxnr.val()}
                console.log(time)
                if(cxnr.val().length==0){
                   alert("查询日期未选择！！");
                   return;
                }else{
                    $.ajax({
                        url: '/index/querys?cxlx='+cxlx+'&cxnr='+cxnr.val(),
                        //url: "/deleteUser",
                        traditional:true,
                        dataType: "json",
                        type: "get",
                        success: function(data) {
                            console.log(data.code)
                            if(data.code!=-1) {
                               console.log('到这儿1')
                               alert('查询成功！');
                                var url='/index/querys?cxlx='+cxlx+'&cxnr='+cxnr.val()
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
                }
                
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