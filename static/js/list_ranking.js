var list;
$.ajax({
	url:'/static/js/stock_info.json',
	dataType:'json',
	async:false,
	success:data=>{list=data}
});//将异步操作中的async改为false，实现同步操作，读取json数据，data是默认参数，需要把它赋给别的值
$('#id1').removeClass('active')
$('#id2').removeClass('active')
if(window.localStorage.flag == undefined)window.localStorage.flag = 1
if(window.localStorage.flag == 1) {
	$('#id1').addClass('active')
	$('#id1').css('color','#007aff')
	$('#id2').css('color','black')
} else {
	$('#id2').addClass('active')
	$('#id2').css('color','#007aff')
	$('#id1').css('color','black')
}
var alist = []
getdata(0)

function getdata(i){
	$.ajax({
		type: "get",
		url: "http://127.0.0.1:9997/getSome?a=" + list[i]['code'] + '&b=' + list[i]['name'],
		async: true,
		dataType: 'jsonp', //JSONP即JSON Padding，是一种解决了传输JSON数据时出现的跨域问题的JSON传输机制
		jsonp: "callback",
		jsonpCallback: "successCallback", //回调方法				
		success: function(data) {
			var dic = data
			alist.push(dic)
			$('ul').html('')
			var blist = []
			for(var i in alist) {
				var dic = alist[i];
				var cha = parseFloat(dic["price"].toFixed(2)) - parseFloat(dic["oldPrice"])
				dic.change = cha / parseFloat(dic["oldPrice"]) * 100
				blist.push(dic)
			}
			var examplearr = blist;

			if(window.localStorage.flag == 1) {
				alist.sort(
					function(x,y){
						return y.change-x.change
					}
				);
				for(var i in alist) {
					var dic = alist[i];
					var aint = parseInt(i) + 1
					if($("#temp").html!="")$("#temp").remove();
					$('ul').append('<li class="mui-table-view-cell">' +
						'<a">【' + aint + '】' + dic["code"] + '-' + dic["name"] + '<span style="float: right;">预测涨幅：' + dic["change"].toFixed(2) + '%</span><p><span style="float: left;">现价：' + dic["oldPrice"] + '</span><span style="float: right;">预测：' + dic["price"].toFixed(2) + '</span></p></a>' +
						'</li>')
				}
			} else {
				alist.sort(
					function(x,y){
						return y.volatility-x.volatility
					}
				);
				for(var i in alist) {
					var dic = alist[i];
					var aint = parseInt(i) + 1
					if($("#temp").html!="")$("#temp").remove();
					$('ul').append('<li class="mui-table-view-cell">' +
						'<a">【' + aint + '】' + dic["code"] + '-' + dic["name"] + '<span style="float: right;">平稳性：' + dic["volatility"].toFixed(2) + '</span><p><span style="float: left;">现价：' + dic["oldPrice"] + '</span><span style="float: right;">预测：' + dic["price"].toFixed(2) + '</span></p></a>' +
						'</li>')
				}
			}

			i = parseInt(i) + 1;
			if(i < 40) {//在这里控制显示的数量
				getdata(i)
			}
		}
	});
}
alist = []

function successCallback(data) {}

$('.item').click(function() {
	$('.item').each(function(i, o) {
		$(o).removeClass('active')
	})
	$(this).addClass('active')
	if($(this).attr('id') == 'id1') {
		window.localStorage.flag = 1
	} else {
		window.localStorage.flag = 2
	}
	location.reload()
})
