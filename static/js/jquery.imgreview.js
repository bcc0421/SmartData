/*!
 * jQuery 图片上传预览
 * @version: v1.0
 * @author kili huang (haoxiaopengyou@gmail.com)
 */
(function ($) {
    /**
     *  图片上传预览
     *  使用方法：$('input[type="file"]').uploadPreview();
     *  
     *  settings: 参数设置
     * ---------------------------------------
     *  ext:        // 支持的图片类型 默认：.jpg|.jpeg|.png|.bmp|.gif
     *  className:  // 预览图片应用的样式
     *  target:     // 预览图片显示的目标容器id, 也可以通过在元素中添加 target 属性来指定显示的容器，如：<input type="file" target="#reviewContent" />
     *  width:      // 预览图片宽度
     *  height:     // 预览图片高度
     *  template:   // 预览图片模板，预览区的元素添加 tag="reviewContent" 如：<div id="template"><div tag="reviewContent"></div></div>
     *  onChange:   // 选择改变时的处理 参数：file：当前 file 的 jquery 对象 如：function(file){}
     */
    $.fn.uploadReview = function (options) {
        options = $.extend({}, $.fn.uploadReview.settings, options);

        this.bind("change", function (e) {
            var file = $(this);
            var fileName = file.val();
            var key = file.attr('key');

            var target = file.attr("target");
            if (target != null && target.length > 1) {
                options.target = target;
            }

            if (checkExtension(fileName, options.ext)) {
                var img = createImg(key, options, file);

                if (typeof FileReader != 'undefined') {
                    var reader = new FileReader();
                    reader.onload = function (result) {
                        img.attr("src", this.result);
                    };
                    reader.readAsDataURL(this.files[0]);
                } else {
                    try {
                        img = img.find('div')[0];
                        img.style.width = options.width + "px";
                        img.style.height = options.height + "px";
                        img.style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(sizingMethod = scale)";
                        img.filters.item("DXImageTransform.Microsoft.AlphaImageLoader").src = fileName;
                    } catch (e) { $('#' + key).remove(); }
                }
            } else {
                $('#' + key).remove();
            }

            if ($.isFunction(options.onChange)) {
                options.onChange(file);
            }

        }).each(function () {
            $(this).attr('key', NewGuid());
        });

        return this;
    };

    $.fn.uploadReview.settings = {
        ext: '.jpg|.jpeg|.png|.bmp|.gif',
        className: '',
        target: '',
        width: 120,
        height: 120,
        template: '',
        onChange: null
    };

    function checkExtension(fileName, extension) {
        if (fileName != null && fileName.length > 0) {
            var strRegex = "(" + extension + ")$";
            var re = new RegExp(strRegex);
            return re.test(fileName.toLowerCase());
        }
        return false;
    };

    function createImg(key, options, file) {
        var img = $('#' + key).eq(0);
        if (img.size() == 0) {
            var tag = (typeof FileReader != 'undefined') ? "<img />" : "<div><div /></div>";

            img = $(tag);
            img.attr({
                "class": options.className
            }).css({
                display: "inline-block",
                width: options.width,
                height: options.height


            });

            var template = img;
            if (options.template != null && options.template.length > 0) {
                template = $(options.template);
                template.find('[tag="reviewContent"]').empty().append(img);
            }

            template.attr("id", key);

            if (options.target == null || options.target.length < 2) {
                template.insertBefore(file);
            } else {
                $(options.target).append(template);
            }
        }
        return img;
    }
    function S4() {
        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    }
    function NewGuid() {
        return (S4() + S4() + S4() + S4() + S4() + S4() + S4() + S4());
    }

})(jQuery);

$(function () {
    $('#pepair-form input[type="file"]').uploadReview();
});
