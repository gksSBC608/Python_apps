/*	function do_initials(){
		var x = document.getElementById("pwd_reset_form");
		x.style.display = "none";
	}
*/

$(function(){
  $("#header").load("/header"); 
});
			
	function forgotpassword(){
		var username = document.querySelectorAll('input[name="username"]')[0].value;
		if(username==''){
			alert("Username is mandatory");
		}else{				
			var check_user_url = "is_user_registered?username="+username;
			$.ajax({
				type:'GET',
				beforeSend: function(){
				$('.ajax-loader').css("visibility", "visible");
				},
				url:check_user_url,
				success:function(data){
					console.log(data);
					json = JSON.parse(data);
					console.log(json);
					if(json.user ==true){
						document.getElementById("username1").value=username;
						document.getElementById("user_label").innerHTML=username
						var x = document.getElementById("login_form");
						x.style.display = "none";
				
						var x = document.getElementById("pwd_reset_form");
						x.style.display = "block";
					}else{
						alert("User not registered");
						console.warn("User not in records");
					}
				},
				complete: function(){
					$('.ajax-loader').css("visibility", "hidden");
				}
				});				
				
			}
			
		}