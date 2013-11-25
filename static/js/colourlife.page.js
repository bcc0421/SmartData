//获取当前URL 的主机部分
var url=window.location.host+"/site/";
var pathname = window.location.pathname;
var newPathname = pathname.replace(/\//,"");
var set_province_id = "";
var set_city_id = "";
var set_area_id = "";

//获取默认市级单位
function GetDefaultCity2(obj){
	
  $.get("http://"+url+"regions?parent_id="+obj,function(defaultCityData2){
	var defaultAreaId2 = defaultCityData2[0].id;
	//构造对应的省级下面的市级单位 并将第一个设置为选中默认
	for (var i = 0; i < defaultCityData2.length; i++) {
		var defaultCityname2 = defaultCityData2[i].name;
		var defaultCityid2 = defaultCityData2[i].id;
		$('#cmbCity2').append("<option value=" + defaultCityid2 + ">" + defaultCityname2 + "</option>");
	}
	GetDefaultArea2(set_city_id);
	$('#cmbCity2').val(set_city_id);
   }, 'json')
}
//获取默认市级单位下的地区
function GetDefaultArea2(obj)
{
	$.get("http://"+url+"regions?parent_id="+obj,function (defaultAreaData2){
		//构造对应地区的 下拉框
		for (var i = 0; i < defaultAreaData2.length; i++) {
			var defaultAreaname2 = defaultAreaData2[i].name;
			var defaultAreaid2 = defaultAreaData2[i].id;
			$('#cmbArea2').append("<option value=" + defaultAreaid2 + ">" + defaultAreaname2 + "</option>");
		}
		
		$('#cmbArea2').val(set_area_id);
	}, 'json')
}
//加载市级单位
function GetCity2(obj) {
	$.get("http://"+url+"regions?parent_id="+$(obj).find("option:selected").val(), function (cityData2) {
			var firstCityId2=cityData2[0].id;
			$('#cmbCity2').empty();
			$('#cmbArea2').empty();
			for (var i = 0; i < cityData2.length; i++) {
				var cityname2 = cityData2[i].name;
				var cityid2 = cityData2[i].id;
				$('#cmbCity2').append("<option value=" + cityid2 + ">" + cityname2 + "</option>");
			}
			//加载默认地区
			GetDefaultArea2(firstCityId2); 
	}, 'json');
};
//加载地区单位
function GetArea2(obj) {
	$.get("http://"+url+"regions?parent_id="+$(obj).find("option:selected").val(), function (areaData2) {
			$('#cmbArea2').empty();
			for (var i = 0; i < areaData2.length; i++) {
				var areaname2 = areaData2[i].name;
				var areaid2 = areaData2[i].id;
				$('#cmbArea2').append("<option value=" + areaid2 + ">" + areaname2 + "</option>");
			}
	}, 'json');
};

//加载小区
function GetCommunity2(obj) {
	$.get("http://"+url+"communities?region_id="+obj, function (communitiesData2) {
			var getNewcommunities = "";
			var getNewcommunitiesBox="";
			$('.lstBox').find("p").remove();
			$('.lstBox').find(".lstBox_item").remove();
			//判断小区数据是否为空
			if(communitiesData2.length > 0)
			{
				for (var i = 0; i < communitiesData2.length; i++) {
					var communitiesAlpha2 = communitiesData2[i].alpha;
					var communitiesName2 = communitiesData2[i].name;
					var communitiesId2 = communitiesData2[i].id;
					var communitiesUrl = communitiesData2[i].domain+newPathname;
					if($("div[id="+"mark_"+communitiesAlpha2+"]").length > 0) //判断字母Box是否存在
					{
						getNewcommunities = '<a class="address_item" href="'+communitiesUrl+'" val="'+communitiesId2+'">'+communitiesName2+'</a>';
						$(getNewcommunities).appendTo($("div[id="+"mark_"+communitiesAlpha2+"]").find(".address"));
					}
					else
					{
						getNewcommunitiesBox = '<div class="lstBox_item" id="'+'mark_'+communitiesAlpha2+'"><span class="tit" val="'+communitiesAlpha2+'">'+communitiesAlpha2+'</span><p class="address"><a class="address_item" href="'+communitiesUrl+'" val="'+communitiesId2+'">'+communitiesName2+'</a></p></div>'

						$(".lstBox .emptyMark").before(getNewcommunitiesBox);
					}
				}
			}
			else
			{
				$("<p style='padding:20px 0;'>对不起，您所选地区暂无数据！</p>").appendTo(".lstBox");
			}
	}, 'json');
};

			
//点击确定获取地区id
$("#addressOk2").die("click").live("click",function() {
	//$(".innerBox").eq(0).siblings().hide();
	//$(".innerBox").eq(0).show();
	var getAddressData2 = $("#cmbArea2 option:selected").val();
	GetCommunity2(getAddressData2);
})			

			
			
			
$(function() {
	
	// 搜索栏的tab
	$(".searchBox_tab").click(function() {
		var _this = $(this),
			_val = _this.attr("val"),
			_cur = _this.siblings(".searchBox_tab_cur"),
			_input = _this.siblings(".searchBox_tab_val");
			
		_this.addClass("searchBox_tab_cur");
		_cur.removeClass("searchBox_tab_cur");
		_input.val(_val);
	});
	
	// 搜索栏的下拉模拟
	$(".search_by_el_selectBox").cl_selectbox();
	
	// 主导航的下拉模拟
	// $(".addressBox .el_selectBox").cl_selectbox();
	
	// 默认的下拉模拟
	$(".default_by_el_selectBox").cl_selectbox();
	
	// 添加收藏
	$(".toolbar .favorite").click(function() {
		$.cl_addBookmark({
			"title"		: "彩生活",
			"url"		: "http://www.colourlife.com"
		});
	});
	
	// 工具栏中分享图标弹出二维码框
	$(".toolbar .shareBox").cl_showChild({
		"child"	: ".shareBox_box"
	});
	
	// 工具栏中帮助弹出下拉
	$(".toolbar .optMore").cl_showChild({
		"child"	: ".optMore_box"
	});
	
	// 工具栏中登录
	$(".toolbar .optLink[title='登录']").click(function() {
		$.cl_tipPop({
			"$this"		: $(this),
			"title"		: "登录",
			"type"		: "default",
			"addClass"	: "logTipPop",
			"temp"		: function() {
				var __temp = '\
					<div class="item">\
						<label class="el_lab">用户名：</label>\
						<input class="el_inText" type="text">\
					</div>\
					<div class="item">\
						<label class="el_lab">密码：</label>\
						<input class="el_inText" type="password">\
					</div>\
					<div class="item">\
						<label class="el_lab">验证码：</label>\
						<input class="el_inText el_inText_sx" type="text">\
						<img class="codeImg" src="../images/pic_demo_banner.png">\
					</div>\
					<div class="btns">\
						<a href="../logResFpw/Fpw_phone.html" class="fpwLink">找回密码</a>\
						<button class="el_btn_sumbit el_btn_orange_sl el_btn"><span class="txt">登录</span></button>\
					</div>\
				';
				
				return __temp;
			},
			"needBg"	: true,
			"onlyOne"	: true,
			"callback"	: null
		});
		
		return false;
	});
	
	
	
	
	
	// 切换小区
	$(".mainNav .addressBox").click(function() {
		var pId_1 = "";
		var cId_1 = "";
		var aId_1 = "";
		if(pId_1 != "" && cId_1 != "" && aId_1 != "")
		{
			set_province_id = pId_1;
			set_city_id = cId_1;
			set_area_id = aId_1;
		}
		else
		{
			set_province_id = 19;
			set_city_id = 233;
			set_area_id = 2149;
		}
		if($(".addressChoseBox").css("display") != "block")
		{
			var titleHtml="<select id='cmbProvince2'  onchange='GetCity2(this)'>"
			/*首先加载所有的省级单位*/
			$.get("http://"+url+"regions?region_id=0", function(provinceData){
				for(var i=0;i<provinceData.length;i++)
				{
					var value=provinceData[i].id;
					var text=provinceData[i].name;
					//var defaultData2 = provinceData[0].id;
					if(i==0)
					{
						titleHtml+="<option value="+value+" selected='true'>"+text+"</option>";
					}
					else
					{
						titleHtml+="<option value="+value+">"+text+"</option>";
					}
				}
				 
				titleHtml+="</select><select id='cmbCity2'onchange='GetArea2(this)'></select><select id='cmbArea2'></select><input type='button' value='确定'id='addressOk2'/>";
			
				$(".addNewAddressChose").find(".title").after(titleHtml);
				//加载默认城市
				GetDefaultCity2(set_province_id);
				$("#cmbProvince2").val(set_province_id);
				GetCommunity2(set_area_id);
			}, 'json');
		}
		

		var __temp = '\
					<div class="addressChoseBox_item addNewAddressChose">\
						<span class="title">快速导航：</span>\
					</div>\
					<div class="addressChoseBox_item">\
						<span class="title title_s1">按首字母筛选小区：</span>\
						<p class="enCon">\
							<a href="###" class="enCon_item" val="A">A</a>\
							<a href="###" class="enCon_item" val="B">B</a>\
							<a href="###" class="enCon_item" val="C">C</a>\
							<a href="###" class="enCon_item" val="D">D</a>\
							<a href="###" class="enCon_item" val="E">E</a>\
							<a href="###" class="enCon_item" val="F">F</a>\
							<a href="###" class="enCon_item" val="G">G</a>\
							<a href="###" class="enCon_item" val="H">H</a>\
							<a href="###" class="enCon_item" val="I">I</a>\
							<a href="###" class="enCon_item" val="J">J</a>\
							<a href="###" class="enCon_item" val="K">K</a>\
							<a href="###" class="enCon_item" val="L">L</a>\
							<a href="###" class="enCon_item" val="M">M</a>\
							<a href="###" class="enCon_item" val="N">N</a>\
							<a href="###" class="enCon_item" val="O">O</a>\
							<a href="###" class="enCon_item" val="P">P</a>\
							<a href="###" class="enCon_item" val="Q">Q</a>\
							<a href="###" class="enCon_item" val="R">R</a>\
							<a href="###" class="enCon_item" val="S">S</a>\
							<a href="###" class="enCon_item" val="T">T</a>\
							<a href="###" class="enCon_item" val="U">U</a>\
							<a href="###" class="enCon_item" val="V">V</a>\
							<a href="###" class="enCon_item" val="W">W</a>\
							<a href="###" class="enCon_item" val="X">X</a>\
							<a href="###" class="enCon_item" val="Y">Y</a>\
							<a href="###" class="enCon_item" val="Z">Z</a>\
						</p>\
					</div>\
					<div class="sepLine"></div>\
					<div class="lstBox">\
						<div class="lstBox_item">\
							<span class="tit" val="B">B</span>\
							<p class="address">\
								<a class="address_item" href="#">碧水龙庭</a>\
							</p>\
						</div>\
						<div class="fn_clear emptyMark"></div>\
					</div>\
				';
				
		$.cl_tipPop({
			"$this"		: $(this),
			"title"		: "切换小区",
			"type"		: "before",
			"addClass"	: "addressChoseBox",
			"temp"		: __temp
		});
		
		//控制按首字母筛选
		$(".enCon").find("a").die("click").live("click",function() {
			var alphaNum = $(this).attr("val");
			var needMoveAlpha = $("#mark_"+alphaNum);
			var moveHeight = 0;
			if(needMoveAlpha.length > 0)
			{
				for(var i = 0;i < $(needMoveAlpha).prevAll().length;i++)
				{
					moveHeight += parseInt($(".lstBox_item").eq(i).outerHeight());
				}
				$(".lstBox").scrollTop(moveHeight);
			}
		});
		
		
		
	});
	

	
	// （测试）工具栏中我的订单
//	$(".toolbar .optLink[title='我的订单']").click(function() {
//		$.cl_tipPop({
//			"$this"		: $(this),
//			"title"		: "信息",
//			"type"		: "default",
//			"addClass"	: "infoTipPop",
//			"temp"		: function() {
//				var __temp = '\
//					<div class="item">\
//						<strong class="infoTxt">我的订单信息</strong>\
//					</div>\
//					<div class="btns">\
//						<button class="el_btn_orange_sl el_btn"><span class="txt">确定</span></button>\
//					</div>\
//				';
//				
//				return __temp;
//			},
//			"needBg"	: true,
//			"onlyOne"	: true,
//			"callback"	: null
//		});
//		
//		return false;
//	});

	
	// 设置相关当前栏目状态
	$.cl_setCurItem(pageConfig);
	
	// input标签添加默认文本，聚焦时，默认文本消失
	$(".el_inText[defaultTxt]").cl_inputDefaultTxt();
	
	
	
	
	
});