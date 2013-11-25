/*
 * name		: $.cl_addBookmark(opt)
 * content	: 添加收藏（仅IE和FF有效）
 *
 * 参数说明
 * @title	: 提示文本
 * @url		: 提示框类型
 * @success	: 可以使用添加收藏功能的回调函数
 * @fail	: 不能使用添加收藏功能的回调函数
 */

(function($) {
	$.cl_addBookmark = function(opt) {
		var _opt = $.extend({}, $.cl_addBookmark.defaults, opt),
			_title = _opt.title,
			_url = _opt.url,
			_success = _opt.success,
			_fail = _opt.fail,
			_state = "";
		
		if (window.sidebar) { 
			window.sidebar.addPanel(_title, _url, "");
			_state = "success";
		} else if( document.all ) {
			window.external.AddFavorite(_url, _title);
			_state = "success";
		} else {
			_state = "fail";
		}
		
		switch(_state) {
			case "success" :
				if (!!_success) {
					_success();
				}
				break;
				
			case "fail" :
				if (!!_fail) {
					_fail();
				}
				break;
		}
	};
	
	$.cl_addBookmark.defaults = {
		"title"		: "",
		"url"		: "",
		"success"	: null,
		"fail"		: null
	};
})(jQuery);


/*
 * name				: $(node).cl_controlNum(opt)
 * content			: 数量加减条
 * 
 * 参数说明
 * @perNum			: 每次加减单位数量（标签中perNum的属性值最优先获取）
 * @startNum		: 开始值（标签中value的属性值最优先获取，starNum的属性值次之；当input的value不存在数值时才以此值为准；如果此值少于min，则以min为准；如果此值大于max，则以max为准）
 * @minNum			: 最小值（标签中minNum的属性值最优先获取）
 * @maxNum			: 最大值（标签中maxNum的属性值最优先获取）
 * @addCallback		: 增加后的执行回调函数（带一个参数，为文本框元素）
 * @reduceCallback	: 减少后的执行回调函数（带一个参数，为文本框元素）
 * @callback		: 增加或减少后的执行回调函数（带一个参数，为文本框元素）
 */

(function($) {
	$.fn.cl_controlNum = function(opt) {
		var _opt = $.extend({}, $.fn.cl_controlNum.defaults, opt);
		
		return this.each(function() {
			var	_this = $(this),
				_add = _this.find(".el_controlNum_add"),
				_reduce = _this.find(".el_controlNum_reduce"),
				_inText = _this.find(".el_controlNum_val"),
				_inText_val = _inText.val(),
				_inText_perNum = _inText.attr("perNum"),
				_inText_startNum = _inText.attr("startNum"),
				_inText_minNum = _inText.attr("minNum"),
				_inText_maxNum = _inText.attr("maxNum"),
				_perNum = (isNaN(_inText_perNum)) ? _opt.perNum : parseInt(_inText_perNum),
				_startNum = (isNaN(_inText_startNum)) ? _opt.startNum : parseInt(_inText_startNum),
				_minNum = (isNaN(_inText_minNum)) ? _opt.minNum : parseInt(_inText_minNum),
				_maxNum = (isNaN(_inText_maxNum)) ? _opt.maxNum : parseInt(_inText_maxNum),
				_addCallback = _opt.addCallback,
				_reduceCallback = _opt.reduceCallback,
				_callback = _opt.callback,
				_fn_init;
			
			function _fn_init() {
				var __num = 0,
					__val = parseInt(_inText.val());
				
				if (isNaN(__val)) {
					__num = _minNum;
				} else {
					if (__val > _minNum && __val < _maxNum) {
						__num = __val;
					} else if (__val <= _minNum) {
						__num = _minNum;
					} else if (__val >= _maxNum) {
						__num = _maxNum;
					}
				}
				
				_inText.val(__num);
			}
			
			// 初始化	
			(function() {
				
				if (isNaN(_inText_val)) {
					var __num = 0;
					
					if (_startNum > _minNum && _startNum < _maxNum) {
						__num = _startNum;
					} else if (_startNum <= _minNum) {
						__num = _minNum;
					} else if (_startNum >= _maxNum) {
						__num = _maxNum;
					}
				
					_inText.val(__num);
				}
			})();
			
			// 节点动作
			(function() {
				
				// 加值
				_add.live("click", function() {
					var __val = parseInt(_inText.val()) + _perNum,
						__set = (__val > _maxNum) ? _maxNum : __val;
					
					_inText.val(__set);
					
					if (typeof _addCallback === "function") {
						_addCallback(_inText);
					}
					
					if (typeof _callback === "function") {
						_callback(_inText);
					}
				});
				
				// 减值
				_reduce.live("click", function() {
					var __val = parseInt(_inText.val()) - _perNum,
						__set = (__val < _minNum) ? _minNum : __val;
					
					_inText.val(__set);
					
					if (typeof _reduceCallback === "function") {
						reduceCallback(_inText);
					}
					
					if (typeof _callback === "function") {
						_callback(_inText);
					}
				});
				
				// 文本框检查数值
				_inText.live("focusout", _fn_init);
			})();
		});
	};
	
	$.fn.cl_controlNum.defaults = {
		"perNum"		: 1,
		"startNum"		: 0,
		"minNum"		: 0,
		"maxNum"		: 99999999999,
		"addCallback"	: null,
		"reduceCallback": null,
		"callback"		: null
	};
})(jQuery);


/*
 * name		: $(node).cl_inputDefaultTxt(opt)
 * content	: input标签添加默认文本，聚焦时，默认文本消失
 */

(function($) {
	$.fn.cl_inputDefaultTxt = function(opt) {
		var _opt = $.extend({}, $.fn.cl_inputDefaultTxt.defaults, opt);
		
		return this.each(function() {
			var _this = $(this),
				_val = _this.val(),
				_dTxt = _this.attr("defaultTxt");
				
			_this.focus(function() {
				var __this = $(this),
					__val = __this.val();
					
				if (__val === _dTxt) {
					__this.val("");
				}
			});
			
			_this.focusout(function() {
				var __this = $(this),
					__val = __this.val();
					
				if (__val === "") {
					__this.val(_dTxt);
				}
			});
		});
	};
	
	$.fn.cl_inputDefaultTxt.defaults = {};
})(jQuery);


/*
 * name				: $(node).cl_scoreLine(opt)
 * content			: 评分条
 * 
 * 参数说明
 * @callback		： 回调函数
 */

(function($) {
	$.fn.cl_scoreLine = function(opt) {
		var _opt = $.extend({}, $.fn.cl_scoreLine.defaults, opt);
		
		return this.each(function() {
			var	_this = $(this),
				_scoreLine_item = _this.find(">.scoreLine_item"),
				_scoreLine_scoreBall = _scoreLine_item.find(".scoreLine_scoreBall"),
				_scoreLine_getSet = _this.find(".scoreLine_getSet"),
				_scoreLine_getSet_val = _scoreLine_getSet.val();
			
			// 节点初始化	
			(function() {
				_scoreLine_item.filter(function() {
					return $(this).attr("value") === _scoreLine_getSet_val;
				}).addClass("setThis");
			})();
			
			// 节点动作
			(function() {
				_scoreLine_scoreBall.click(function() {
					var __parent = $(this).parents(".scoreLine_item"),
						__parent_val = __parent.attr("value");
					
					__parent.addClass("setThis").siblings(".setThis").removeClass("setThis");
					
					_scoreLine_getSet.val(__parent_val);
					
					if (typeof _opt.callback === "function") {
						_opt.callback();
					}
				});
			})();
		});
	};
	
	$.fn.cl_scoreLine.defaults = {
		"callback"	: null
	};
})(jQuery);


/*
 * name		: $(node).cl_scrollPicBox(opt)
 * content	: 点击切换图片滚动框
 *
 * 参数说明
 * @maxNum	: 可视区域最大缩放图数量
 */

(function($) {
	$.fn.cl_scrollPicBox = function(opt) {
		var _opt = $.extend({}, $.fn.cl_scrollPicBox.defaults, opt);
		
		return this.each(function() {
			var	_maxNum = _opt.maxNum,
				_this = $(this),
				_picField = _this.find(".scrollPicBox_img"),
				_prev = _this.find(".scrollPicBox_optItem_pBtn"),
				_next = _this.find(".scrollPicBox_optItem_nBtn"),
				_container = _this.find(".scrollPicBox_optItem_picBox .container"),
				_pBox = _container.find(".pBox"),
				_pBox_len = _pBox.size(),
				_eachW = 0,
				_totalW = 0,
				_endPos = 0;
			
			// 数值初始化
			(function() {
				_eachW = _pBox.width() + parseInt(_pBox.css("margin-right")) + 2;
				
				_totalW = _eachW * _pBox_len;
				
				_container.css("width", _totalW + "px");
				
				_endPos = -(_totalW - _eachW * _maxNum);
			})();
			
			// 节点初始化初始化
			(function() {
				_pBox.eq(0).addClass("cur");
				
				_picField.attr("src", _pBox.eq(0).attr("imgSrc"));
			})();
			
			// 图片切换
			(function() {
				_pBox.click(function() {
					var __this = $(this),
						__cur = __this.siblings(".cur"),
						__src = __this.attr("imgSrc");
						
					__cur.removeClass("cur");
					
					__this.addClass("cur");
					
					_picField.attr("src", __src);
				});
			})();
			
			// 按钮点击滚动
			(function() {
				if (_pBox_len <= _maxNum) {return false;}
				
				_prev.click(function() {
					var __this = $(this),
						__cPos = parseInt(_container.css("margin-left"));
					
					if (!__this.hasClass("disbaled") && __cPos !== 0) {
						__this.addClass("disbaled");
						
						_container.animate({
							"margin-left" : "+=" + _eachW + "px"
						}, function() {
							__this.removeClass("disbaled");
						});
					}
				});
				
				_next.click(function() {
					var __this = $(this),
						__cPos = parseInt(_container.css("margin-left"));
						
					if (!__this.hasClass("disbaled") && __cPos !== _endPos) {
						__this.addClass("disbaled");
						
						_container.animate({
							"margin-left" : "-=" + _eachW + "px"
						}, function() {
							__this.removeClass("disbaled");
						});
					}
				});			
			})();
		});
	};
	
	$.fn.cl_scrollPicBox.defaults = {
		"maxNum"	: 4
	};
})(jQuery);


/*
 * name		: $(node).cl_selectbox(opt)
 * content	: select标签模拟
 *
 * 参数说明
 * @callback: 回调函数，带两个参数，第一个为下拉外框，第二个为选中的值
 */

(function($) {
	$.fn.cl_selectbox = function(opt) {
		var _opt = $.extend({}, $.fn.cl_selectbox.defaults, opt);
		
		return this.each(function() {
			var _this = $(this),
				_valBox = _this.find(".el_selectBox_valBox"),
				_val = _this.find(".el_selectBox_val"),
				_list = _this.find(".el_selectBox_list"),
				_item = _list.find(".el_selectBox_list_item");
				
			_item.click(function() {
				var __this = $(this),
					__val = __this.attr("value");
					
				_val.attr("value", __val);
				
				_list.css({
					"visibility"		: ""
				});
				
				if(typeof _opt.callback === "function") {
					_opt.callback(_this, __val);
				}
			});
			
			_valBox.click(function() {
				_val.blur();
				_list.css({
					"visibility"		: "visible"
				});
			});
			
			_this.mouseleave(function() {
				_list.css({
					"visibility"		: ""
				});
			});
		});
	};
	
	$.fn.cl_selectbox.defaults = {
		"callback"	: null
	};
})(jQuery);


/*
 * name		: $.cl_setCurItem(data)
 * content	: 设置相关当前栏目状态
 */

(function($) {
	$.cl_setCurItem = function(data) {
		var _data = data,
			_pageItemType = _data["pageItemType"],
			_mainNavCurIndex = _data["mainNavCurIndex"],
			_subNavCurIndex = _data["subNavCurIndex"],
			_root = $("html");
				
		switch(_pageItemType){
			case 1 :
				if (_mainNavCurIndex > 0) {
					_root.find(".mainNav_box .mainNav_item").eq(_mainNavCurIndex - 1).addClass("mainNav_item_cur");
				}
				break;
			case 3 :
				if (_mainNavCurIndex > 0) {
					_root.find(".hcMainNav .item").eq(_mainNavCurIndex - 1).addClass("item_cur");
				}
				
				if (_mainNavCurIndex > 1) {
					_root.find("body").addClass("hc_bg");
				}
				
				// 二级栏目及其子栏初始化
				if (!!_subNavCurIndex && _subNavCurIndex.length>0) {
					$(".hcSideBar").cl_sidebarMore({
						"initParm"	: _subNavCurIndex
					});
				}
				break;
		};
	};
})(jQuery);


/*
 * name		: $(node).cl_showChild(opt)
 * content	: 鼠标滑过显示指定后代
 *
 * 参数说明
 * @child	: 子代元素
 */

(function($) {
	$.fn.cl_showChild = function(opt) {
		var _opt = $.extend({}, $.fn.cl_showChild.defaults, opt);
		
		if (!_opt.child) {return false;}
		
		return this.each(function() {
			var _this = $(this),
				_child = _this.find(_opt.child);
							
			_this.mouseenter(function() {
				_child.css("visibility", "visible");
			});
			
			_this.mouseleave(function() {
				_child.css("visibility", "");
			});
		});
	};
	
	$.fn.cl_showChild.defaults = {
		"child"	: null
	};
})(jQuery);


/*
 * name				: $(node).cl_skyScrollPicBox(opt)
 * content			: 全幅滚动
 * 
 * 参数说明
 * @delay			: 自动滚动时，每隔多少ms滚动一次
 */

(function($) {
	$.fn.cl_skyScrollPicBox = function(opt) {
		var _opt = $.extend({}, $.fn.cl_skyScrollPicBox.defaults, opt);
		
		return this.each(function() {
			var	_this = $(this),
				_btn = _this.find(".skyScrollPicBox_btn"),
				_picBox = _this.find(".skyScrollPicBox_pics"),
				_pic = _picBox.find(".skyScrollPicBox_pic"),
				_pic_w = _pic.width(),
				_pic_h = _pic.height(),
				_pic_len = _pic.size(),
				_fn_go,
				_fn_run,
				_curIndex = 0,
				_id,
				_delay = _opt.delay;
			
			function _fn_go(tarIndex) {
				if (_curIndex === _pic_len - 1) {
					_curIndex = 0;
				} else {
					_curIndex++;
				}
				
				if (!isNaN(tarIndex)) {
					_curIndex = tarIndex;
				}
				
				_btn.eq(_curIndex).addClass("current").siblings(".current").removeClass("current");
				
				_picBox.stop().animate({
					"margin-left"	: "-" + (_curIndex * _pic_w) + "px"
				});
			};
			
			function _fn_run() {
				_fn_go();
				
				_id = setTimeout(_fn_run, _delay);
			};
			
			// 初始化	
			(function() {
				_picBox.css("width", _pic_w * _pic_len + "px");
				
				_btn.eq(0).addClass("current");
			})();
			
			// 节点动作
			(function() {
				
				// 切换
				_btn.click(function() {
					var __this = $(this),
						__index = __this.index();
						
					_fn_go(__index);
				});
				
				// 鼠标移入，定时滚动消失
				_this.mouseenter(function() {
					clearTimeout(_id);
				});
				
				// 鼠标移出，定时滚动开启
				_this.mouseleave(function() {
					_id = setTimeout(_fn_run, _delay);
				});
			})();
			
			// 函数执行
			(function() {
				
				_id = setTimeout(_fn_run, _delay);
			})();
		});
	};
	
	$.fn.cl_skyScrollPicBox.defaults = {
		"delay"		: 3000
	};
})(jQuery);


/*
 * name				: $(node).cl_switchBox(opt)
 * content			: 点击头部栏目切换内容
 * 
 * 参数说明
 * @startTarIndex	: .headBox_itemBox对应的tarIndex值，默认第一个.headBox_itemBox为当前，设置后，则对应元素设置当前
 * @switchAction	： "hover" / "click" ，通过何种事件进行切换
 * @fixedContainer	： false / true ，是否固定第一个.containBox_inner进行数据装在
 * @callback		： 回调函数
 */

(function($) {
	$.fn.cl_switchBox = function(opt) {
		var _opt = $.extend({}, $.fn.cl_switchBox.defaults, opt);
		
		return this.each(function() {
			var	_startTarIndex = _opt.startTarIndex,
				_switchAction = _opt.switchAction,
				_fixedContainer = _opt.fixedContainer,
				_callback = _opt.callback,
				_this = $(this),
				_headBox = _this.find(">.headBox"),
				_headBox_item = _headBox.find(">.headBox_itemBox"),
				_containBox = _this.find(">.containBox"),
				_containBox_inner = _containBox.find(">.containBox_inner"),
				_fn_switch;
			
			// 节点初始化	
			(function() {
				
				// 头部节点
				if (_startTarIndex === "") {
					_headBox_item.eq(0).addClass("currentEle");
				} else {
					_headBox_item.filter(function() {
						return $(this).attr("tarIndex") === _startTarIndex;
					}).addClass("currentEle");
				}
				
				// 内容区节点
				if (_startTarIndex === "") {
					_containBox_inner.eq(0).addClass("currentEle");
				} else {
					_containBox_inner.filter(function() {
						return $(this).attr("srcIndex") === _startTarIndex;
					}).addClass("currentEle");
				}
			})();
			
			// 切换动作
			(function() {
				
				// 切换函数
				function _fn_switch($this) {
					var __this = $this,
						__tarIndex = __this.attr("tarIndex");
					
					if (!_fixedContainer) {
						_containBox_inner.filter(function() {
							return $(this).hasClass("currentEle");
						}).removeClass("currentEle").end().filter(function() {
							return $(this).attr("srcIndex") === __tarIndex;
						}).addClass("currentEle");
					}
					
					__this.addClass("currentEle").siblings(".currentEle").removeClass("currentEle");
					
					if (typeof _opt.callback === "function") {
						_callback();
					}
				};
				
				// 通过不同动作绑定函数
				switch(_switchAction) {
					case "hover" :
						_headBox_item.mouseenter(function() {
							_fn_switch($(this));
						});
						break;
						
					case "click" :
						_headBox_item.click(function() {
							_fn_switch($(this));
						});
						break;
				}
			})();
		});
	};
	
	$.fn.cl_switchBox.defaults = {
		"startTarIndex"	: "",
		"switchAction"	: "hover",
		"fixedContainer": false,
		"callback"		: null
	};
})(jQuery);


/*
 * name		: $.cl_tipPop(opt)
 * content	: 提示信息
 *
 * 参数说明
 * @$this	: 提示文本
 * @title	: 提示框标题
 * @type	: default / before / none ， 提示框类型
 * @addClass: 给弹出框外框加入额外的class（仅加一个）
 * @temp	: function / string ， 接受函数（带return string）或者字符串
 * @needBg	: true / false ， 是否需要大半透明背景
 * @onlyOne	: true / false ， 是否只需要一个当前同类弹出框（通过addClass判断）
 * @callback: 回调函数（带两个参数，第一个为弹出框外框根元素，第二个为触发弹出框事件的元素）
 */

(function($) {
	$.cl_tipPop = function(opt) {
		var _opt = $.extend({}, $.cl_tipPop.defaults, opt),
			_$this = _opt.$this,
			_title = _opt.title,
			_text = _opt.text,
			_type = _opt.type,
			_needBg = _opt.needBg,
			_addClass = _opt.addClass,
			_onlyOne = _opt.onlyOne,
			_temp = _opt.temp,
			_callback = _opt.callback,
			_tpid = "tipPop" + parseInt(Math.random() * 10000),
			_root = $("html"),
			_body = _root.find("body"),
			_bgNode = '<div class="el_tipPop_bg" tpid="' + _tpid + '"></div>',
			_tip,
			_bg,
			_fn_temp,
			_fn_close;
		
		if (_onlyOne && _body.find("." + _addClass).size() !== 0) {
			return false;
		}
		
		// 数据初始化		
		(function() {
			
			_addClass = (!!_addClass) ? ' ' + _addClass : '';
		})();
		
		// 定义函数
		(function() {
			
			// 模板加载函数
			_fn_temp = function(temp) {
				var __temp = '';
				
				__temp += (_needBg) ? '' : '';
				
				__temp += '\
					<div class="el_tipPop' + _addClass + '" tpid="' + _tpid + '">\
						<div class="el_tipPop_h">\
							<div class="el_tipPop_h_i">\
								<span class="title">' + _title + '</span>\
								<i class="el_btn close"></i>\
							</div>\
						</div>\
						<div class="el_tipPop_m">\
							<div class="el_tipPop_m_i">\
								<div class="el_tipPop_m_i_b">\
				';
				
				__temp += (typeof _temp === "function") ? _temp() : _temp;
				
				__temp += '     </div>\
							</div>\
						</div>\
						<div class="el_tipPop_b">\
							<div class="el_tipPop_b_i"></div>\
						</div>\
					</div>\
				';
				
				return __temp;
			};
			
			// 关闭弹出窗
			_fn_close = function() {
				_tip.fadeOut(function() {
					_bg.remove();
					_tip.remove();
				});
			};
		})();
		
		// 加载模板
		(function() {
			switch(_type){
				
				case "info" :
					if (_needBg) {
						_body.append(_bgNode);
					}
					_body.append(_fn_temp(_temp));
					break;
				
				case "default" :
					if (_needBg) {
						_body.append(_bgNode);
					}
					_body.append(_fn_temp(_temp));
					break;
				
				case "before" :
					_$this.before(_fn_temp(_temp));
					break;
					
				case "none" :
					alert(_text);
					break;
			};
			
			_tip = _body.find(".el_tipPop[tpid='" + _tpid + "']");
			
			_bg = _body.find(".el_tipPop_bg[tpid='" + _tpid + "']");
			
			_tip.fadeIn();
			
			_bg.show();
		})();
		
		// 函数绑定与调用
		(function() {
			// 关闭按钮
			_tip.find(".close").click(_fn_close);
			
			// 回调函数
			if (typeof _opt.callback === "function") {
				_callback(_tip, _$this);
			}
		})();
	};
	
	$.cl_tipPop.defaults = {
		"$this"		: null,
		"title"		: "",
		"type"		: "none",
		"addClass"	: "",
		"temp"		: null,
		"needBg"	: true,
		"onlyOne"	: true,
		"callback"	: null
	};
})(jQuery);


/*
 * name				: $(node).cl_countdown(opt)
 * content			: 倒计时
 * 
 * 参数说明
 * @goingTemp		: 进行时模板，{hour}、{min}、{sec}分别代表结束时间的时、分、秒
 * @endTemp			: 结束时模板
 * @endTime			: 结束时间数组，六个数字分别代表结束时间的年、月、日、时、分、秒
 * @goingCallback	: 执行时执行回调函数
 * @endCallback		: 结束时执行回调函数
 */

(function($) {
	$.fn.cl_countdown = function(opt) {
		var _opt = $.extend({}, $.fn.cl_countdown.defaults, opt);
		
		return this.each(function() {
			var	_this = $(this),
				_endTime = (_this.attr("endtime")) ? _this.attr("endtime").split(",") : _opt.endTime,
				_endTemp = _opt.endTemp,
				_goingTemp = _opt.goingTemp,
				_goingCallback = _opt.goingCallback,
				_endCallback = _opt.endCallback,
				_year = _endTime[0] || 2013,
				_month = _endTime[1] - 1 || 0,
				_day = _endTime[2] || 1,
				_hour = _endTime[3] || 0,
				_min = _endTime[4] || 0,
				_sec = _endTime[5] || 0,
				_today = new Date(),
				_times = _today.getTime(),
				_eTime = new Date(_year, _month, _day, _hour, _min, _sec).getTime(),
				_leftTime = _eTime - _times,
				_leftTime_hour,
				_leftTime_min,
				_leftTime_sec,
				_setTemp,
				_fn_checkTime,
				_id;
			
			function _fn_checkTime() {
				
				if (_leftTime <= 0) {
					_this.html(_endTemp);
					
					if (typeof _endCallback === "function") {
						_endCallback();
					}
					
					return false;
				}
					
				_today = new Date();
				
				_times = _today.getTime();
				
				_leftTime = _eTime - _times;
				
				_leftTime_hour = parseInt(_leftTime/3600000);
				
				_leftTime_min = parseInt(_leftTime%3600000/60000);
				
				_leftTime_sec = parseInt(_leftTime%3600000%60000/1000);
				
				_leftTime_hour = (_leftTime_hour<10) ? "0" + _leftTime_hour : String(_leftTime_hour);
				
				_leftTime_min = (_leftTime_min<10) ? "0" + _leftTime_min : String(_leftTime_min);
				
				_leftTime_sec = (_leftTime_sec<10) ? "0" + _leftTime_sec : String(_leftTime_sec);
				
				_setTemp = _goingTemp.replace("{hour}", _leftTime_hour).replace("{min}", _leftTime_min).replace("{sec}", _leftTime_sec);
				
				_this.html(_setTemp);
				
				if (typeof _goingCallback === "function") {
					_goingCallback();
				}
				
				_id = setTimeout(_fn_checkTime, 1000);
			};
			
			_fn_checkTime();
		});
	};
	
	$.fn.cl_countdown.defaults = {
		"goingTemp"		: "",
		"endTemp"		: "",
		"endTime"		: [2013, 8, 8, 8, 0, 0],
		"goinCallback"	: null,
		"endCallback"	: null
	};
})(jQuery);


/*
 * name				: $(node).cl_sidebarMore(opt)
 * content			: 侧栏更多下拉栏
 * 
 * 参数说明
 * @initParm		: 初始化数组，子级当前栏目索引值，从1开始，0表示没有当前效果；数组中第1至n个分别代表2级中第？个中的...的第n级的第？个的当前栏目索引值
 */

(function($) {
	$.fn.cl_sidebarMore = function(opt) {
		var _opt = $.extend({}, $.fn.cl_sidebarMore.defaults, opt);
		
		return this.each(function() {
			var	_this = $(this),
				_subTit = _this.find(".subTit"),
				_parentNode = _this,
				_childNode,
				_initParm = _opt.initParm,
				_initParm_len = _initParm.length,
				_fn_init;
			
			// 初始化
			_fn_init = function() {
				$.each(_initParm, function(i, val) {
					_childNode = _parentNode.find(">.itemBox").eq(val - 1);
					
					if (i === _initParm_len - 1) {
						_parentNode
							.find(">.itemBox").find(">.linkBox").eq(val - 1).addClass("current");
					} else {
						_childNode
							.find(">.subTit").addClass("current").end()
								.find(">.itemBox").addClass("curItem");
					}
					
					_parentNode = _childNode;
				});
			}();
			
			// 展开关闭
			_subTit.click(function() {
				var __this = $(this);
				
				if (__this.hasClass("current")) {
					__this.removeClass("current")
						.siblings(".itemBox").removeClass("curItem")
							.find(".curItem").removeClass("curItem").end()
								.find(".current").removeClass("current");
				} else {
					__this.addClass("current")
						.siblings(".itemBox").addClass("curItem").end()
							.parent().siblings().find(".curItem").removeClass("curItem").end()
								.find(".current").removeClass("current");
				}
			});
		});
	};
	
	$.fn.cl_sidebarMore.defaults = {
		"initParm"	: []
	};
})(jQuery);
