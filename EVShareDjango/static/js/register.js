$(function () {
    function bindCaptchaBtnClick() {
        $("#captcha-btn").click(function (event) {
            let $this = $(this);
            let email = $("input[name='email']").val();
            if (!email) {
                alert("Please enter your email address");
                return;
            }
            $this.off("click");

            $.ajax('/login/captcha?email=' + email, {
                method: "GET",
                success: function (result) {
                    if (result['code']===200) {
                        alert(result['message']);
                    }else{
                        alert(result['message']);
                    }
                },
                fail: function (error) {
                    console.log(error);
                }
            })

            let countdown = 60;
            let timer = setInterval(function () {
                if (countdown <= 0) {
                    $this.text('Get code again');
                    clearInterval(timer);
                    bindCaptchaBtnClick();
                } else {
                    countdown--;
                    $this.text('Resend code in ' + countdown + ' seconds');
                }
            }, 1000)
        })
    }

    bindCaptchaBtnClick()

})