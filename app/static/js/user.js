//tab标签页默认开启控制
$(function () {
    $('#myTab a').click(function (e) {
        e.preventDefault();
        $(this).tab('show');
    });
})

//在除首页的其他页面对于nav竖导航进行控制
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

//用户注册控制表单验证
$(function () {
    // 验证用户名
    $('#username').focus(function () {
    }).blur(function () {
        var username = $(this).val();
        var userurl = $("#userurl").val();
        var usernameok = username.replace(/[^\x00-\xff]/g, "rrr").length;
        if (usernameok >= 6 && usernameok <= 64) {
            $.ajax({
                type: "POST", //用POST方式传输
                dataType: "text", //数据格式:JSON
                url: userurl, //目标地址
                data: "username=" + username,
                error: function (data) {
                    $("#username").next().text('用户名已经被注册');
                },
                success: function (data) {
                    if (data == "false") {
                        $("#username").next().text('用户名已经被注册');
                    } else {
                        $("#username").next().text('');
                    }

                }
            });

        } else if (usernameok == 0) {
            $(this).next().text('用户名不能为空');
        } else {
            $(this).next().text('请输入正确长度的用户名');
        }

    });
    //验证手机号
    $('#cellphone').focus(function () {
    }).blur(function () {
        var isMobile = /^(?:13\d|14\d|15\d|18\d|17\d)\d{5}(\d{3}|\*{3})$/;
        var phonenum = $(this).val();
        var userurl = $("#userurl").val();
        if (isMobile.test(phonenum)) {
            $.ajax({
                type: "POST", //用POST方式传输
                dataType: "text", //数据格式:JSON
                url: userurl, //目标地址
                data: "mobile=" + phonenum,
                success: function (data) {
                    if (data == "false") {
                        $("#cellphone").next().text('手机号已存在');
                    } else {
                        $("#cellphone").next().text('');
                    }

                }
            });
        } else if (phonenum == "") {
            $(this).next().text('手机号码不能为空');
        } else {
            $(this).next().text('请输入正确的手机号');
        }


    });
    //前端校验验证码长度
    $('#inputVerCode').focus(function () {
        // $(this).next().text('密码应该为6-20位之间');
    }).blur(function () {
        var code = $(this).val();
        var iscode = /^\d{6}$/;
        if (iscode.test(code)) {
            $("#smsinfo").text("");
        } else {
            $("#smsinfo").text('请输入正确的验证码');
        }

    });

    //验证邮箱
    $('#inputemail').focus(function () {
        // $(this).next().text('请输入正确的EMAIL格式');
    }).blur(function () {
        var myreg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
        var email = $(this).val();
        if (myreg.test(email) || email == "") {
            $(this).next().text('');
        }
        else {
            $(this).next().text('请输入正确格式的邮箱');
        }

    });
    //验证密码
    $('#password').focus(function () {
        // $(this).next().text('密码应该为6-20位之间');
    }).blur(function () {
        var password = $(this).val();
        var passwordlength = password.length;
        if (passwordlength >= 6 && passwordlength <= 20) {
            $(this).next().text('');
        } else {
            $(this).next().text('请输入长度为6到20位的密码');
        }

    });
    //验证确认密码
    $('#password2').focus(function () {
    }).blur(function () {
        if ($(this).val() != '' && $(this).val() == $('#password').val()) {
            $(this).next().text('');
        } else {
            $(this).next().text('前后密码不一致');
        }
    });

    //提交按钮,所有验证通过方可提交

});
$('#userregbtn').click(function () {
    var ok1 = false;
    var ok2 = false;
    var ok3 = false;
    var ok4 = false;
    var ok5 = false;
    var ok6 = false;
    var username = $("#username").val();
    var usernameok = username.replace(/[^\x00-\xff]/g, "rrr").length;
    var userurl = $("#userurl").val();
    if (usernameok >= 6 && usernameok <= 64) {
        $.ajax({
            type: "POST", //用POST方式传输
            dataType: "text", //数据格式:JSON
            url: userurl, //目标地址
            async: false,
            data: "username=" + username,
            error: function (data) {
                $("#username").next().text('用户名已经被注册');
                $("#userstatus").val(0);
            },
            success: function (data) {
                if (data == "false") {
                    $("#username").next().text('用户名已经被注册');
                    $("#userstatus").val(0);
                } else {
                    $("#username").next().text('');
                    $("#userstatus").val(1);
                }
            }
        });
        var userstatus = $("#userstatus").val();
        if (userstatus == "1") {
            ok1 = true;
        }
        else {
            ok1 = false;
        }
    } else if (usernameok == 0) {
        $("#username").next().text('用户名不能为空');
    } else {
        $("#username").next().text('请输入正确长度的用户名');
    }

    var isMobile = /^(?:13\d|14\d|15\d|18\d|17\d)\d{5}(\d{3}|\*{3})$/;
    var phonenum = $('#cellphone').val();
    if (isMobile.test(phonenum)) {
        if (isMobile.test(phonenum)) {
            $.ajax({
                type: "POST", //用POST方式传输
                dataType: "text", //数据格式:JSON
                url: userurl, //目标地址
                async: false,
                data: "mobile=" + phonenum,
                error: function (data) {
                    ok2 = false;
                    $("#cellphone").next().text('手机号已存在');
                    $("#cellphonestatus").val(0);
                },
                success: function (data) {
                    if (data == "false") {
                        $("#cellphonestatus").val(0);
                        $("#cellphone").next().text('手机号已存在');
                    } else {
                        $("#cellphonestatus").val(1);
                        $("#cellphone").next().text('');
                    }
                }

            });
            var cellphonestatus = $("#cellphonestatus").val();
            if (cellphonestatus == "1") {
                ok2 = true;
            }
            else {
                ok2 = false;
            }

        }

    } else if (phonenum == "") {
        $('#cellphone').next().text('手机号码不能为空');
    } else {
        $('#cellphone').next().text('请输入正确的手机号');
    }

    var code = $('#inputVerCode').val();
    var iscode = /^\d{6}$/;
    if (iscode.test(code)) {
        $("#smsinfo").text("");
        ok3 = true;
    } else {
        $("#smsinfo").text('请输入正确的验证码');
    }
    var myreg = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
    var email = $('#inputemail').val();
    if (myreg.test(email) || email == "") {
        $('#inputemail').next().text('');
        ok4 = true;
    }
    else {
        $('#inputemail').next().text('请输入正确格式的邮箱');
    }
    var password = $('#password').val();
    var passwordlength = password.length;
    if (passwordlength >= 6 && passwordlength <= 20) {
        $('#password').next().text('');
        ok5 = true;
    } else {
        $('#password').next().text('请输入长度为6到20位的密码');
    }
    if ($('#password2').val() != '' && $('#password2').val() == $('#password').val()) {
        $('#password2').next().text('');
        ok6 = true;
    } else {
        $('#password2').next().text('前后密码不一致');
    }
    if (ok1 && ok2 && ok3 && ok4 && ok5 && ok6) {
        $('#userregbtn').submit();

    } else {
        return false;
    }
});
//显示全部
function show() {
    var box = document.getElementById("boxmore");
    var text = box.innerHTML;
    var newBox = document.createElement("div");
    var btn = document.createElement("a");
    btn.className = "amoremore";
    newBox.innerHTML = text.substring(0, 262);
    btn.innerHTML = text.length > 262 ? "...查看全部" : "";
    btn.href = "###";
    btn.onclick = function () {
        if (btn.innerHTML == "...查看全部") {
            btn.innerHTML = "收起";
            newBox.innerHTML = text;
        } else {
            btn.innerHTML = "...查看全部";
            newBox.innerHTML = text.substring(0, 262);
        }
    }
    box.innerHTML = "";
    box.appendChild(newBox);
    box.appendChild(btn);
}
var degree = ['', '很差', '差', '中', '良', '优', '未评分'];
//重新点评
function addComment2(e, inid, opt, id) {
    $.ajax({
        url: '/siteMessage/content',
        type: 'post',
        data: 'id=' + id,
        dataType: 'json',
        success: function (data) {
            if (data.status == 1) {
                var list = $('#Addnewskill_119');
                list.eq(0).html(data.talent + '(人才ID：' + data.talentId + ')');
                list.eq(1).html(data.job);
                list.eq(2).html(data.ms);

                var arr = [data.total, data.expAuth, data.killAuth, data.followTime, data.formality, data.appReact];
                var list2 = $('span.level', '#Addnewskill_119');
                $('input[name="InterviewCommentInfoSub[opt]"]').val(opt + 1);
                list2.each(function (i, v) {
                    var a = '';

                    if (i > 0) {
                        a = 'cjmark';
                        $(v).parents('li').find('input').val(arr[i]);
                    }
                    var str = '';
                    if (arr[i] == 6) {
                        for (var n = 0; n <= 4; n++) {
                            str += '<i ' + a + ' class="level_hollow"></i>';
                        }
                        $(v).parents('li').find('input').prop('disabled', true)
                    } else {
                        $(v).parents('li').find('input').prop('checked', true)
                        for (var n = 0; n < arr[i]; n++) {
                            str += '<i ' + a + ' class="level_solid"></i>';
                        }
                        for (var n = 0; n < (5 - arr[i]); n++) {
                            str += '<i ' + a + ' class="level_hollow"></i>';
                        }
                    }
                    $(v).html(str);
                    $(v).next().html(degree[arr[i]]);
                })
                create_show(119);
            } else {
                ui.error(data.msg, 2000);
            }
        }
    })
}

$(function () {
    //点星星
    $(document).on('mouseover', 'i[cjmark]', function () {
        var num = $(this).index();
        var pmark = $(this).parents('.revinp');
        var mark = pmark.prevAll('input');

        if (mark.prop('checked')) return false;

        var list = $(this).parent().find('i');
        for (var i = 0; i <= num; i++) {
            list.eq(i).attr('class', 'level_solid');
        }
        for (var i = num + 1, len = list.length - 1; i <= len; i++) {
            list.eq(i).attr('class', 'level_hollow');
        }
        $(this).parent().next().html(degree[num + 1]);
        $("#scorenum").val(num + 1);

    })
    //点击星星
    $(document).on('click', 'i[cjmark]', function () {
        var num = $(this).index();
        var pmark = $(this).parents('.revinp');
        var mark = pmark.prevAll('input');

        if (mark.prop('checked')) {
            mark.val('');
            mark.prop('checked', false);
            mark.prop('disabled', true);
        } else {
            mark.val(num);
            $("#scorenum").val(num + 1);
            mark.prop('checked', true);
            mark.prop('disabled', false);
        }
    })
    //选框
    $('#Addnewskill_119 input[type="checkbox"]').change(function () {
        if ($(this).not(':checked')) {//!($(this).prop('checked'))
            $(this).prop('checked', false);
            $(this).prop('disabled', true)
            var smark = $(this).nextAll('.revinp');
            smark.find('span.revgrade').html('未评分');
            smark.find('i').attr('class', 'level_hollow');
            smark.val(6);
            $("#scorenum").val(num + 1);
        }
    })


})

document.getElementById("Commenttext").focus();
var chackTextarea = function (obj, num, objTip) {
    obj.onkeyup = obj.onfocus = function () {
        if (obj.value.length >= 1) {
            if (obj.value.length > num) {
                objTip.innerHTML = "已超出";
                objTip.style.color = "#F00";
                document.getElementById("button").disabled = "disabled";
            } else {
                objTip.innerHTML = "已输入" + (obj.value.length) + "/" + num + "个字!";
                objTip.style.color = "#000";
                document.getElementById("button").disabled = "";
            }
        } else {
            document.getElementById("button").disabled = "disabled";
        }
    }
}

chackTextarea(document.getElementById("Commenttext"), 500, document.getElementById("commentnum"));
function shake(o) {
    var $panel = $("#" + o);
    box_left = ($(window).width() - $panel.width()) / 2;
    $panel.css({'left': box_left, 'position': 'absolute'});
    for (var i = 1; 4 >= i; i++) {
        $panel.animate({left: box_left + (40 - 10 * i) - 360}, 10);
        $panel.animate({left: box_left + 1.1 * (40 - 10 * i) - 360}, 10);
    }
}
//评论时候必须评分
$(function () {
    $("#scorebtn").click(function () {
        var scorenum = $("#scorenum").val();
        if (scorenum == 0) {
            shake('scoreno');
            return false;
        }
    })
})

