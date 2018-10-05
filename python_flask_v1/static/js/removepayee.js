				var submit_btn;
				function do_initials(){
					submit_btn = $("input[type='submit']");
					submit_btn.prop('disabled', false);
					var payee_acc_name_field = $("input#payee_acc_name1");
					var payee_acc_bank_field = $("input#payee_acc_bank1");
					payee_acc_name_field.prop('disabled', true);
					payee_acc_bank_field.prop('disabled', true);
					//var curr_url = new URL(window.location.href);
					//console.log(curr_url);
					//var username = curr_url.searchParams.get("username");
					//var acc_number = curr_url.searchParams.get("acc_number");
					$("input[name='username']").val(username);
					//var home_link_el = $("[href='home']");
					//var home_url = "server/controller_action.py/render_dashboard?username="+username;
					//home_link_el.attr('href', home_url);
					//console.log(username+', '+acc_number)
						
						$("#overlay").addClass('starting');
						var beneficiaries_url = "getpayee_accounts";
						$.get(beneficiaries_url, function(data, status){
							
							console.log(data);
							console.log(data.length);
				
							if(data.length<=6){
								alert("Payee not added");
								submit_btn.prop('disabled', true);
							}
							json = JSON.parse(data);
							console.log("json is "+json);
							var select_str = "<select id='payee_acc_number' style='width: 167px;' onchange='load_payee_info()'>";
							var options ="<option value='---'>---select---</option>";
							json.forEach(function(item){
							//console.log(item);
							var option = "<option value="+item+">"+item+"</option>";
							options += option;
							});
							//console.log(options);
							select_str += options+"</select>";
							//console.log(select_str);
							document.getElementById("acc_list").innerHTML=select_str;
							$("#overlay").removeClass('starting');
						});
					
				}
				
				function validate_input(){
					var payee_acc_number = document.getElementById("payee_acc_number").value;
					//console.log(payee_acc_number);
					if("---"===payee_acc_number){
						alert("Select a payee account number");
						return false;
					}else{
						return true;
					}
					
				}
				
				function load_payee_info(){
					
					var payee_acc_number = document.getElementById("payee_acc_number").value;
					console.log(payee_acc_number);
					if("---"===payee_acc_number){
						document.getElementById("payee_acc_name").value= '';
						document.getElementById("payee_acc_bank").value= '';
						document.getElementById("payee_acc_name1").value= '';
						document.getElementById("payee_acc_bank1").value= '';
						document.getElementById("payee_acc_number_text").value ='';
					}else{
						document.getElementById("payee_acc_number_text").value = payee_acc_number;
						$("#overlay").addClass('starting');
						var url = "getpayee_data?payee_acc_number="+payee_acc_number;
						$.get(url, function(data, status){
							//console.log(data);
							json = JSON.parse(data);
							//console.log(json);
							document.getElementById("payee_acc_name").value= json.ben_name;
							document.getElementById("payee_acc_name1").value= json.ben_name;
							document.getElementById("payee_acc_bank1").value= json.bank_name;
							document.getElementById("payee_acc_bank").value= json.bank_name;
							$("#overlay").removeClass('starting');
						});
					}
					
				}