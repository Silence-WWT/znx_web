var wait=60;
$("#regmessage").attr('disabled',false);
$("#regmessage").val("免费获取验证码");  
function time(o) {
        if (wait == 0) {
            o.removeAttribute("disabled");           
            o.value="免费获取验证码";
            wait = 60;
        } else {

            o.setAttribute("disabled", true);
            o.value="重新发送(" + wait + ")";
            wait--;
            setTimeout(function() {
                time(o)
            },
            1000)
        }
    }
	
	$(function(){
		$("#regmessage").click(function(){
			time(this);
			var mobile=$("#inputPhone").val();
			var isMobile=/^(?:13\d|15\d|18\d)\d{5}(\d{3}|\*{3})$/; //手机号码验证规则
			var moblieurl=$("#mobileurl").val();
			alert(moblieurl);
			if(isMobile.test(mobile)){
			   $.ajax({
                    type: "POST", //用POST方式传输
                    dataType: "text", //数据格式:JSON
                    url: moblieurl, //目标地址
                    data: "mobile=" + mobile,
                    error: function (XMLHttpRequest, textStatus, errorThrown) { },
                    success: function (msg){ }

                });		
			}
		
			})
		})
