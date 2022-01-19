
$('#nav li').each(function() { //4、移除ul下所有li
	$(this).remove();
});
var table = document.getElementById("nav");
//var classArr = ['n1', 'n2', 'n3', 'n4', 'n7', 'n7 more', 'n8'];
var classArr = ['n1', 'n2', 'n3', 'n4', 'n7', 'n8'];
//var titleArr = ["首页", "公司简介", "新闻资讯", "服务业务类型", "服务案例", "业务区域", "联系我们"]
var titleArr = ["首页", "公司简介", "新闻资讯", "服务业务类型", "服务案例", "联系我们"]
//var hrefArr = ["index.html", "about/index.html", "news/index.html", "business/property.aspx.html", "anli/property.aspx.html", "area/index.html", "contact/index.html"]
var hrefArr = ["http://gaojingwuye.gz01.bdysite.com/index.html", "http://gaojingwuye.gz01.bdysite.com/about/index.html", "http://gaojingwuye.gz01.bdysite.com/news/index.html", "http://gaojingwuye.gz01.bdysite.com/business/property.aspx.html", "http://gaojingwuye.gz01.bdysite.com/anli/property.aspx.html", "http://gaojingwuye.gz01.bdysite.com/contact/index.html"]
var temp = ""
for(var i = 0; i < classArr.length; i++) {
	var li = document.createElement('li');
	li.className = classArr[i];
	li.innerHTML = '<a href="' + hrefArr[i] + '"><span>' + titleArr[i] + '</span><span class="bkg"></span></a>';
	//				temp = temp + '<li class="' + classArr[i] + '"><a href="' + hrefArr[i] + '"><span>' + titleArr[i] + '</span><span class="bkg"></span></a></li>';
	//				alert(temp)
	//下拉刷新，新纪录插到最前面；
	table.insertBefore(li, table.lastChild);
}