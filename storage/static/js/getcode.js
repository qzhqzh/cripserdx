var code = document.getElementById('code');
var myEmail = document.querySelector('#myEmail');
var checkCode = document.getElementById('check-code');
code.onclick = function () {
    var values = myEmail.value;
    $.ajax(
        {
            type:'get',
            // dataType:'json',
            url:('http://127.0.0.1:8000/myuser/findpwd2/'),
            data:{username:values},
            success: function (result) {
                // console.log(result)
                code.style.display="none"
                checkCode.innerHTML = '验证码已发送邮箱，请输入验证码:<input type="text" name="check-code">'
                var mySubmit = document.createElement('input');
                mySubmit.type = 'submit';
                checkCode.appendChild(mySubmit)
                mySubmit.value = '提交'
                // console.log(result.msg)
                if (result.msg == '邮箱存在'){
                    code.style.display="none"
                    checkCode.innerHTML = '验证码已发送邮箱，请输入验证码:<input type="text">'
                    var mySubmit = document.createElement('input');
                    mySubmit.type = 'submit';
                    checkCode.appendChild(mySubmit)
                    mySubmit.value = '提交';
                }else {
                    checkCode.innerHTML = '邮箱不存在，<a href="/">请联系管理员</a>'
                }
            },
            error:function (xhr,status,error) {
                console.log(error);

            }
        }
    )

}