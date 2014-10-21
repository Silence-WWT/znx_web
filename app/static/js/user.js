$(function(){$('#myTab a').click(function (e) {
    e.preventDefault();
    $(this).tab('show');
});})

	 
	  $(function () {
		  
    $("#navorgan").click(function () {
	
      $("#allnav").toggle();
        if ($("#allnav").is(":hidden")) {
 
            $("#iconcheck").removeClass('icon-chevron-up').addClass('icon-chevron-down');
        } else {
            $("#iconcheck").removeClass('icon-chevron-down').addClass('icon-chevron-up');
        }
    })
 
})

$(function () {
    var ok1 = false;
    var ok2 = false;
    var ok3 = false;
    var ok4 = false;
    // 验证用户名
    $('input[name="username"]').focus(function () {
        // $(this).next().text('');
    }).blur(function () {
        if ($(this).val() != '') {
            $(this).next().text('');
            //$(this).next().css('color','#00B98D');
            ok1 = true;
        } else {
            $(this).next().text('用户名不能为空');
            //   $(this).next().css('color','#FF2424');
        }
 
    });
    //验证手机
    $('input[name="phoneNumber"]').focus(function () {
        // $(this).next().text('');
    }).blur(function () {
        if ($(this).val().length == 11) {
            $(this).next().text('');
            //$(this).next().css('color','#00B98D');
            ok1 = true;
        } else {
            $(this).next().text('手机号码输入格式错误哦!');
            //$(this).next().css('color','#FF2424');
        }
 
    });
 
    //验证密码
    $('input[name="password"]').focus(function () {
        // $(this).next().text('密码应该为6-20位之间');
    }).blur(function () {
        if ($(this).val() != '') {
            $(this).next().text('');
            ok2 = true;
        } else {
            $(this).next().text('密码不能为空');
            //$(this).next().css('color','#FF2424');
        }
 
    });
 
    //验证确认密码
    $('input[name="confirmPassword"]').focus(function () {
        // $(this).next().text('输入的确认密码要和上面的密码一致,规则也要相同');
    }).blur(function () {
        if ($(this).val() != '' && $(this).val() == $('input[name="password"]').val()) {
            $(this).next().text('');
            ok3 = true;
        } else {
            $(this).next().text('前后密码不一致哦！');
            //$(this).next().css('color','#FF2424');
        }
 
    });
 //验证邮箱
    $('input[name="email"]').focus(function () {
        // $(this).next().text('请输入正确的EMAIL格式');
    }).blur(function () {
        if ($(this).val().search(/\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/) == -1) {
            $(this).next().text('请输入正确的EMAIL格式');
            //$(this).next().css('color','#FF2424');
        } else {
            //$(this).next().text('输入成功');
            ok4 = true;
        }
 
    });
 
    //提交按钮,所有验证通过方可提交
    $('#userRegSubmit').click(function () {
        if (ok1 && ok2 && ok3 && ok4) {
            $('form').submit();
        } else {
            return false;
        }
    });
 
});

function show(){ 
var box = document.getElementById("boxmore"); 
var text = box.innerHTML; 
var newBox = document.createElement("div"); 
var btn = document.createElement("a");
btn.className="amoremore"; 
newBox.innerHTML = text.substring(0,262); 
btn.innerHTML = text.length > 262 ? "...查看全部" : ""; 
btn.href = "###"; 
btn.onclick = function(){ 
if (btn.innerHTML == "...查看全部"){ 
btn.innerHTML = "收起"; 
newBox.innerHTML = text; 
}else{ 
btn.innerHTML = "...查看全部"; 
newBox.innerHTML = text.substring(0,262); 
} 
} 
box.innerHTML = ""; 
box.appendChild(newBox); 
box.appendChild(btn); 
} 
show();


var degree = ['','很差','差','中','良','优','未评分'];
//重新点评
function addComment2(e,inid,opt,id){
	$.ajax({
		url:'/siteMessage/content',
		type:'post',
		data:'id='+id,
		dataType:'json',
		success:function(data){
			if(data.status==1){
				var list = $('#Addnewskill_119');
				list.eq(0).html(data.talent+'(人才ID：'+data.talentId+')');
				list.eq(1).html(data.job);
				list.eq(2).html(data.ms);
				
				var arr = [data.total,data.expAuth,data.killAuth,data.followTime,data.formality,data.appReact];
				var list2 = $('span.level','#Addnewskill_119');
				$('input[name="InterviewCommentInfoSub[opt]"]').val(opt+1);
				list2.each(function(i,v){
						var a = '';
						
						if(i>0){
							a = 'cjmark';
							$(v).parents('li').find('input').val(arr[i]);
						}
						var str = '';
						if(arr[i]==6){
							for(var n=0;n<=4;n++){
								str += '<i '+a+' class="level_hollow"></i>';
							}
							$(v).parents('li').find('input').prop('disabled',true)
						}else{
							$(v).parents('li').find('input').prop('checked',true)
							for(var n=0;n<arr[i];n++){
								str += '<i '+a+' class="level_solid"></i>';
							}
							for(var n=0;n<(5-arr[i]);n++){
								str += '<i '+a+' class="level_hollow"></i>';
							}
						}
						$(v).html(str);
						$(v).next().html(degree[arr[i]]);
					
				})
				
				
				create_show(119);
			}else{
				ui.error(data.msg,2000);
			}
		}
	})	
}

$(function(){
	//点星星
	$(document).on('mouseover','i[cjmark]',function(){
		var num = $(this).index();
		var pmark = $(this).parents('.revinp');
		var mark = pmark.prevAll('input');
	
		if(mark.prop('checked')) return false;
		
		var list = $(this).parent().find('i');
		for(var i=0;i<=num;i++){
			list.eq(i).attr('class','level_solid');
		}
		for(var i=num+1,len=list.length-1;i<=len;i++){
			list.eq(i).attr('class','level_hollow');
		}
		$(this).parent().next().html(degree[num+1]);

	})
	//点击星星
	$(document).on('click','i[cjmark]',function(){
		var num = $(this).index();
		var pmark = $(this).parents('.revinp');
		var mark = pmark.prevAll('input');
		
		if(mark.prop('checked')){
			mark.val('');
			mark.prop('checked',false);mark.prop('disabled',true);	
		}else{
			mark.val(num);
			mark.prop('checked',true);mark.prop('disabled',false);	
		}
	})
	//选框
	$('#Addnewskill_119 input[type="checkbox"]').change(function(){
		if($(this).not(':checked')){//!($(this).prop('checked'))
			$(this).prop('checked',false);$(this).prop('disabled',true)
			var smark = $(this).nextAll('.revinp');
			smark.find('span.revgrade').html('未评分');
			smark.find('i').attr('class','level_hollow');
			smark.val(6);
		}
	})
	

})
  //alert("");
document.getElementById("Commenttext").focus();
 var chackTextarea = function(obj,num,objTip){
  obj.onkeyup=obj.onfocus=function(){
    if(obj.value.length>=1){
     if (obj.value.length > num) {
       objTip.innerHTML="已超出";
       objTip.style.color="#F00";
       document.getElementById("button").disabled="disabled";
     }else{
        objTip.innerHTML="已输入"+(obj.value.length) +"/"+num+"个字!";
       objTip.style.color="#000";
       document.getElementById("button").disabled="";
     }
    }else{
      document.getElementById("button").disabled="disabled";
    }
  }
 }
 
 chackTextarea(document.getElementById("Commenttext"),500,document.getElementById("commentnum"));

