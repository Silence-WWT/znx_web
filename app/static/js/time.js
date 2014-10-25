var InterValObj; //timer变量，控制时间
var count = 60; //间隔函数，1秒执行
var curCount;//当前剩余秒数
function sendMessage() {
	curCount = count;
	var mobilephone=$("#inputPhone").val();//手机号码
    var messageurl=$("#mobileurl").val();
	if(mobilephone != ""){
		//设置button效果，开始计时
		$("#regmessage").attr("disabled", "true");
		$("#regmessage").val("请在" + curCount + "秒内输入验证码");
		InterValObj = window.setInterval(SetRemainTime, 1000); //启动计时器，1秒执行一次
	//向后台发送处理数据
		$.ajax({
			type: "POST", //用POST方式传输
			dataType: "text", //数据格式:JSON
			url: messageurl, //目标地址
			data: "mobile=" + mobilephone,
			error: function (data) {
           alert(data);
           },
		success: function (data){
            alert(data);
           }
		});
	}else{
		//alert("手机号码不能为空！");
	}
}
//timer处理函数
function SetRemainTime() {
	if (curCount == 0) {                
		window.clearInterval(InterValObj);//停止计时器
		$("#regmessage").removeAttr("disabled");//启用按钮
		$("#regmessage").val("重新发送验证码");
		code = ""; //清除验证码。如果不清除，过时间后，输入收到的验证码依然有效    
	}
	else {
		curCount--;
		$("#regmessage").val("请在" + curCount + "秒内输入验证码");
	}
}
