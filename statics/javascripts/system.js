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
            url: '/system',         //请求后台的URL（*）
            method: 'post',                      //请求方式（*）
            toolbar: '#toolbar',                //工具按钮用哪个容器
            striped: true,                      //是否显示行间隔色
            cache: false,                       //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
            pagination: false,                   //是否显示分页（*）
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
                    title: '字段名称',
                    field: '列名',
                }, {
                    title: '字段注释',
                    field: '注释',

                }, {
                    title: '字段类型',
                    field: '数据类型',

                },  ]
        });
    };
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
                        url: '/index/queryd?cxlx='+cxlx.val()+'&cxnr='+cxnr.val(),
                        //url: "/deleteUser",
                        traditional:true,
                        dataType: "json",
                        type: "get",
                        success: function(data) {
                            console.log(data.code)
                            if(data.code!=-1) {
                               console.log('到这儿1')
                                var url='/index/queryd?cxlx='+cxlx.val()+'&cxnr='+cxnr.val()
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
                
                    var url='/system'
                    var opt = {
                        url: url
                    };
                    // 带参数，刷新（加载新请求数据）
                    $("#tb_departments").bootstrapTable('refresh', opt);
                    // 不带参数，只刷新（重新加载数据）
                    // $("#table").bootstrapTable('refresh');
                
            })
    
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