var form1;
var form2;
$(function(){
	$("#header").load("/header");
	form1 = document.getElementById("form1");
    form2 = document.getElementById("form2");
	form2.style.display = "none";
});

function check_username(){
		var username = $('input[name="username"]').val();
		if(username==''){
			alert("Username is mandatory");
		}
		else
		{
				
			var check_user_url = "is_user_registered?username="+username;
			$("#overlay").addClass('starting');
			$.ajax({
				type:'GET',
				beforeSend: function(){
				//$('.ajax-loader').css("visibility", "visible");
				},
				url:check_user_url,
				success:function(data){
					console.log(data);
					json = JSON.parse(data);
					console.log(json);
					$("#overlay").removeClass('starting');
					if(json.user ==true){
						document.getElementById("username1").value=username;
						//document.getElementById("user_label").innerHTML=username
						document.getElementById("user_label").value=username
						
						form1.style.display = "none";
						form2.style.display = "block";
						form2.style.top="50%";
					}else{
						alert("User not registered");
						console.warn("User not in records");
					}
				},
				complete: function(){
					//$('.ajax-loader').css("visibility", "hidden");
					
				}
				});				
								
				
		}
}
