$(function(){
	$("#refreshimg").click(function(){
		$.post('newsession.php');
		$("#captchaimage").load('image_req.php');
		return false;
	});
        });