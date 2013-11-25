// JavaScript Document

$(document).ready(function(e) {
	var _el_btn_orange_xsl = $(".reserve_btn_by_from");
	var _form = $("form");
	var dataValid=false;
	
	//点击“预约”
	_el_btn_orange_xsl.each(function(index, element) {
		$(this).click(function() {
			
			//check方法
			function checkForm(){
				var nameValue =$.trim( _form.eq(index).find("input[name = 'name']").attr("value")),
				      nameDefaulttxt = $.trim(_form.eq(index).find("input[name = 'name']").attr("defaulttxt")),
				      telValue = $.trim(_form.eq(index).find("input[name = 'tel']").attr("value")),
				      telDefaulttxt = $.trim(_form.eq(index).find("input[name = 'tel']").attr("defaulttxt")),
				      reserveTimeValue = $.trim(_form.eq(index).find("select[name = 'reserve_time'] option:selected").attr("value")),
                      reserveValue = $.trim(_form.eq(index).find("input[id = 'reserve_value']").attr("value")),
                      addressValue = $.trim(_form.eq(index).find("input[name = 'address']").attr("value")),
                      addressDefaulttxt = $.trim(_form.eq(index).find("input[name = 'address']").attr("defaulttxt")),
				      descValue = $.trim(_form.eq(index).find("textarea[name = 'desc']").attr("value")),
				      descDefaulttxt = $.trim(_form.eq(index).find("textarea[name = 'desc']").attr("defaulttxt"));

				if(_form.eq(index).find("input[name = 'name']").length>0 && ( nameValue == nameDefaulttxt || nameValue == "" || nameValue == null ))
				{
				    alertBox('姓名不能为空！','style3');
					dataValid = false;
					return false;
				}
				else
				{
					dataValid=true;
				}
				if(_form.eq(index).find("input[name = 'tel']").length>0 && (telValue ==telDefaulttxt || telValue == "" || telValue == null ))
				{
					alertBox('联系电话不能为空','style3');
					dataValid = false;
					return false;
				}
				else
				{
				    var pattern=/(^[0-9]{3,4}\-[0-9]{3,8}$)|(^[0-9]{3,8}$)|(^\([0-9]{3,4}\)[0-9]{3,8}$)|(^1[3|4|5|8][0-9]{5,9}$)/; 
                    if(!pattern.test(telValue) && _form.eq(index).find("input[name = 'tel']").length>0) 
                    { 
                        alertBox('联系电话格式错误','style3');
					    dataValid = false;
                        return false;
                    } 
                    else 
                    { 
                         dataValid=true;
                    } 
                    					
				}
                
				if(_form.eq(index).find("select[name = 'reserve_time']").length>0 && (reserveTimeValue == "请选择" || reserveTimeValue == "" || reserveTimeValue == null))
				{
				    var message = "服务时间/服务内容不能为空！";
				    if(reserveValue==0){
				        message = "请选择取衣时间！";
				    }else if(reserveValue==1){
				        message = "请选择上门时间！";
				    }else{
				        message = "请选择服务内容！";
				    }
					alertBox(message,'style3');
					dataValid = false;
					return false;
				}
				else
				{
					dataValid = true;
				}
                
                if(_form.eq(index).find("input[name = 'address']").length>0 && (addressValue ==addressDefaulttxt || addressValue == "" || addressValue == null ))
				{
					alertBox('详细地址不能为空！','style3');
					dataValid = false;
					return false;
				}
				else
				{
					dataValid=true;
				}
                
				if(descValue == descDefaulttxt || descValue == "" || descValue == null)
				{
					alertBox("请填写备注说明！",'style3')
					dataValid = false;
					return false;
				}
				else
				{
					dataValid = true;
				}
			}
			//调用check
			checkForm();
			
			//check完成
			if(dataValid == true)
			{
				_form.eq(index).submit();
			}
			
		});
	});
	
	//弹出层
	function alertBox(boxInfo,style)
	{
		var successBox ='<div class="alertBoxWrap">\
								<div class="alertBoxBg"></div>\
								<div class="alertBoxMain '+style+'">\
									<div class="alertBoxMainInfo">'+boxInfo+'</div>\
									<input type="button" value="确定" class="alertBoxSureBn"/>\
								</div></div>'
															 
		$(successBox).appendTo("body");
		$(".alertBoxSureBn").die("click").live("click",function() {
			$(".alertBoxWrap").remove();
		})
	}
	
});


                            