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
 
 
 
 $('#myTab a').click(function (e) {
    e.preventDefault();
    $(this).tab('show');
});