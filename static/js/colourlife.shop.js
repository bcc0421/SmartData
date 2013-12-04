// JavaScript Document

//获取当前URL 的主机部分
var url=window.location.host+"/site/";
var pId="";
var cId="";
var aId="";
//加载市级单位
function GetCity(obj,selectCid,selectAid) {
	$.get("http://"+url+"regions?parent_id="+$(obj).find("option:selected").val(), function (cityData) {
		var firstCityId=cityData[0].id;
		$("#"+selectCid).empty();
		$("#"+selectAid).empty();
		$("#shopCommunity2").empty();
		for (var i = 0; i < cityData.length; i++) {
			var cityname = cityData[i].name;
			var cityid = cityData[i].id;
			$("#"+selectCid).append("<option value=" + cityid + ">" + cityname + "</option>");
		}
		//加载第一个市级单位下的区级单位
		GetDefaultAreaS(firstCityId,selectAid); 
		//GetDefaultArea(firstCityId,'shopArea2'); 
	}, 'json');
};

//加载地区单位
function GetArea(obj,selectAid) {
	$.get("http://"+url+"regions?parent_id="+$(obj).find("option:selected").val(), function (areaData) {
			$("#"+selectAid).empty();
			$("#shopCommunity2").empty();
			for (var i = 0; i < areaData.length; i++) {
				var areaname = areaData[i].name;
				var areaid = areaData[i].id;
				$("#"+selectAid).append("<option value=" + areaid + ">" + areaname + "</option>");
			}
	}, 'json');
};
function GetArea2(obj,selectAid) {
	$.get("http://"+url+"regions?parent_id="+$(obj).find("option:selected").val(), function (areaData) {
			$("#"+selectAid).empty();
			$("#shopCommunity2").empty();
			for (var i = 0; i < areaData.length; i++) {
				var areaname = areaData[i].name;
				var areaid = areaData[i].id;
				$("#"+selectAid).append("<option value=" + areaid + ">" + areaname + "</option>");
			}
			//good 页面加载默认小区
			var shopDefaultId = areaData[0].id;
			shopGetDefaultCommunity(shopDefaultId);
	}, 'json');
};
//加载小区
function GetCommunity(obj) {
	$.get("http://"+url+"communities?region_id="+obj, function (communitiesData) {
			var getNewcommunities = "";
			$(".communitiesBox").find("li").eq(0).nextAll().remove();
			$(".communitiesBox").find("li").eq(0).addClass("c-right-fore1-content-li");
			//判断小区数据是否为空
			if(communitiesData.length > 0)
			{
				for (var i = 0; i < communitiesData.length; i++) {
					var communitiesName = communitiesData[i].name;
					var communitiesId = communitiesData[i].id;
                    var communitiesUrl = communitiesData[i].domain;
					getNewcommunities = '<li><a href="'+communitiesUrl+'" val="'+communitiesId+'">'+communitiesName+'</a></li>'
					$(getNewcommunities).appendTo($(".communitiesBox"));
				}
			}
			else
			{
				alert("对不起，您所选地区暂无数据！")
			}
			//小区显示区域高度控制
			controlHeight();
	}, 'json');
};

//获取默认市级单位
function GetDefaultCity(obj,selectCid){
  $.get("http://"+url+"regions?parent_id="+obj,function(defaultCityData){
	var defaultAreaId = defaultCityData[0].id;
	//构造对应的省级下面的市级单位
	for (var i = 0; i < defaultCityData.length; i++) {
		var defaultCityname = defaultCityData[i].name;
		var defaultCityid = defaultCityData[i].id;
		$("#"+selectCid).append("<option value=" + defaultCityid + ">" + defaultCityname + "</option>");
	}
	
	
	GetDefaultArea(cId,'shopArea'); 
	//GetDefaultArea(defaultAreaId,'shopArea2');
	$("#shopProvince").val(pId);
   }, 'json')
}

//获取默认区级单位
function GetDefaultArea(obj,selectAid)
{
	$.get("http://"+url+"regions?parent_id="+obj,function (defaultAreaData){
		for (var i = 0; i < defaultAreaData.length; i++) {
			var defaultAreaname = defaultAreaData[i].name;
			var defaultAreaid = defaultAreaData[i].id;
			$("#"+selectAid).append("<option value=" + defaultAreaid + ">" + defaultAreaname + "</option>");
		}
		//good 页面加载默认小区
		//var shopDefaultId = defaultAreaData[0].id;
		//shopGetDefaultCommunity(shopDefaultId);
		$("#shopCity").val(cId);
		$("#shopArea").val(aId);
	}, 'json')
}
function GetDefaultAreaS(obj,selectAid)
{
	$.get("http://"+url+"regions?parent_id="+obj,function (defaultAreaData){
		for (var i = 0; i < defaultAreaData.length; i++) {
			var defaultAreaname = defaultAreaData[i].name;
			var defaultAreaid = defaultAreaData[i].id;
			$("#"+selectAid).append("<option value=" + defaultAreaid + ">" + defaultAreaname + "</option>");
		}
	}, 'json')
}
//goods 页面 获取小区
function shopGetCommunity(obj,selectCommunityId) {
	$.get("http://"+url+"communities?region_id="+$(obj).find("option:selected").val(), function (communitiesData) {
			var getNewcommunities = "";
			$("#"+selectCommunityId).empty();
			//判断小区数据是否为空
			if(communitiesData.length > 0)
			{
				for (var i = 0; i < communitiesData.length; i++) {
					var communitiesName = communitiesData[i].name;
					var communitiesId = communitiesData[i].id;
					$("#"+selectCommunityId).append("<option value=" + communitiesId + ">" + communitiesName + "</option>");
				}
                $('#shopCommunity2').change();
			}
			else
			{
				//alert("对不起，您所选地区暂无数据！")
                $('#show_have_goods').show().children('td').html("<div style='margin:5px 20px;color:red;'>本商品在选择的小区暂不销售！</div>");
				$(".el_btn_orange_xxsl").css({"background-position":"0 -1840px","cursor":"default"})
				$(".el_btn_orange_xxsl .icon").css("background-position","-37px -1813px");
				$(".el_btn_orange_xxsl .txt").css("color","#808080");
			}
	}, 'json');
};
//goods 页面 获取默认小区
function shopGetDefaultCommunity(obj) {
	$.get("http://"+url+"communities?region_id="+obj, function (communitiesData) {
			var getNewcommunities = "";
			$("#shopCommunity2").empty();
			//判断小区数据是否为空
			if(communitiesData.length > 0)
			{
				for (var i = 0; i < communitiesData.length; i++) {
					var communitiesName = communitiesData[i].name;
					var communitiesId = communitiesData[i].id;
					$('#shopCommunity2').append("<option value=" + communitiesId + ">" + communitiesName + "</option>");
				}
                $('#shopCommunity2').change();
			}
			else
			{
				//alert("对不起，您所选地区暂无数据！")
                $('#show_have_goods').show().children('td').html("<div style='margin:5px 20px;color:red;'>本商品在选择的小区暂不销售！</div>");
				$(".el_btn_orange_xxsl").css({"background-position":"0 -1840px","cursor":"default"})
				$(".el_btn_orange_xxsl .icon").css("background-position","-37px -1813px");
				$(".el_btn_orange_xxsl .txt").css("color","#808080");
			}
	}, 'json');
};

function showHaveGoods(obj){
    $.get("http://"+url+"haveGoods?community_id="+$(obj).find("option:selected").val(), function (numData) {
        if(numData.count>0){
			$(".el_btn_orange_xxsl").css({"background-position":"0 -1889px","cursor":"pointer"});
			$(".el_btn_orange_xxsl .icon").css("background-position","0 -1813px");
			$(".el_btn_orange_xxsl .txt").css("color","#fff");
			$("#buy_goods").addClass("el_btn_buy_s1_1");
            $('#show_have_goods').show().children('td').html("<div style='margin:5px 20px;'>本商品在选择的小区可以购买！</div>");
        }else{
			$(".el_btn_orange_xxsl").css({"background-position":"0 -1840px","cursor":"default"});
			$(".el_btn_orange_xxsl .icon").css("background-position","-37px -1813px");
			$(".el_btn_orange_xxsl .txt").css("color","#808080");
            $('#show_have_goods').show().children('td').html("<div style='margin:5px 20px;color:red;'>本商品在选择的小区暂不销售！</div>");
        }
    }, 'json');
};

function controlHeight(){
	$(".c-right-foer1-footer").find("a").removeClass("arrow-up");
	if($(".communitiesBox").outerHeight() > 100)
	{
		$(".communitiesBox").css("height","100px");
		$(".c-right-foer1-footer").find("a").addClass("arrow-up");
	}
	else
	{
		$(".communitiesBox").css("height","auto");
	}
}





$(document).ready(function(e) {
	
	//评论查看全部
	$(".add-new-a").click(function() {
		$(".add-control").find(".currentEle").removeClass("currentEle");
		$(".add-control .headBox_itemBox").eq(1).addClass("currentEle");
		$(".add-control .containBox_inner").eq(1).addClass("currentEle");
	});
	
	
	
	//区域收起展开
	var add_other_all = $(".add-other-all"),
		  add_open_all = $(".add-open-all");
	
	$(".add-open-all").click(function() {
		if($(".c-right-foer1-footer").find("a").hasClass("arrow-up") == true)
		{
			$(".c-right-foer1-footer").find("a").removeClass("arrow-up");
			$(".communitiesBox").css({"height":"auto"});
		}
		else
		{
			$(".c-right-foer1-footer").find("a").addClass("arrow-up");
			$(".communitiesBox").css({"height":"100px"});
		}
	});
	

	
	//省市区三级联动
	$(".add-address-select").click(function(){
		var pId_0 = $(".add-address-select").attr("pId");
		var cId_0 = $(".add-address-select").attr("cId");
		var aId_0 = $(".add-address-select").attr("aId");
		if(pId_0 != "" && cId_0 != "" && aId_0 != "")
		{
			pId = pId_0;
			cId = cId_0;
			aId = aId_0;
		}
		else
		{
			pId = 19; //广东省
			cId = 233; //深圳市
			aId = 2149;//福田区
		}
		if($(".address-select").css("display") == "none")
		{
			//加载省级单位
			$.get("http://"+url+"regions?region_id=0", function(provinceData){
				for(var i=0;i<provinceData.length;i++)
				{
					var value=provinceData[i].id;
					var text=provinceData[i].name;
					//var defaultData = provinceData[0].id;
					if(i==0)
					{
						$('#shopProvince').append("<option value=" + value + ">" + text + "</option>");
					}
					else
					{
						$('#shopProvince').append("<option value=" + value + ">" + text + "</option>");
					}
				}
				//加载默认市级单位
				GetDefaultCity(pId,'shopCity'); 

			}, 'json');
			//选择框显示
			$(".address-select").show();
		}
		
		
	});
	//地址选择框“确定”按钮点击动作
	$("#shopAddressOk").click(function() {
		var selectProvinceId = $("#shopProvince option:selected").attr("value");
		var selectCityId = $("#shopCity option:selected").attr("value");
		var selectAreaId = $("#shopArea option:selected").attr("value");
		var selectProvinceName = $("#shopProvince option:selected").text();
		var selectCityName = $("#shopCity option:selected").text();
		var selectAreaName = $("#shopArea option:selected").text();
		$(".add-address-select").attr({"pId":selectProvinceId,"cId":selectCityId,"aId":selectAreaId})
		//当前位置
		$(".add-address-select").attr({"selectAreaId":selectAreaId}).text(selectProvinceName+","+selectCityName+","+selectAreaName);
		//加载小区动作
		GetCommunity(selectAreaId);
		//选择框消失
		$(".address-select").hide();
        var pageUrl = window.location.href;
        pageUrl = pageUrl.substr(0,pageUrl.indexOf('?'));
        window.location.href = pageUrl+"?community_id=&area_id="+selectAreaId;
	});
	
	//小区单击切换
	$(".communitiesBox").find("li").die("click").live("click",function() {
		$(".c-right-fore1-content-li").removeClass("c-right-fore1-content-li");
		$(this).addClass("c-right-fore1-content-li");
	})
	
	

	
	

	
	
	
	
});