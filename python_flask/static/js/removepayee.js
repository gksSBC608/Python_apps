				var submit_btn;
				var key = "";
				var flag = false;
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
					//$("input[name='username']").val(username);
					//var home_link_el = $("[href='home']");
					//var home_url = "server/controller_action.py/render_dashboard?username="+username;
					//home_link_el.attr('href', home_url);
					//console.log(username+', '+acc_number)
						
						$("#overlay").addClass('starting');
						var beneficiaries_url = "getpayee_accounts_0";
						$.get(beneficiaries_url, function(data, status,xhr){
							
							console.log(data);
							console.log(data.length);
						
							if(data.length<=6){
								alert("Payee not added");
								submit_btn.prop('disabled', true);
							}
							key = xhr.getResponseHeader("security-key");
							console.log(key);
							flag = true;
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
						if(flag){
							$("#overlay").addClass('starting');
							var url = "getpayee_data_0?payee_acc_number="+payee_acc_number;
							/*
							$.get(url, function(data, status,xhr){
								//console.log(data);
								json = JSON.parse(data);
								//key = xhr.getResponseHeader("security-key");
								//console.log(key)
								document.getElementById("payee_acc_name").value= json.ben_name;
								document.getElementById("payee_acc_name1").value= json.ben_name;
								document.getElementById("payee_acc_bank1").value= json.bank_name;
								document.getElementById("payee_acc_bank").value= json.bank_name;
								$("#overlay").removeClass('starting');
							});
							*/
							$.ajax({
								url: "getpayee_data_0",
								data: { payee_acc_number: payee_acc_number },
							type: "GET", 
							beforeSend: function(xhr){
								xhr.setRequestHeader('security-key', key);
							},
							success: function(data, status,xhr) {
								var key1 = xhr.getResponseHeader("security-key");
								console.log(key1);
								document.getElementById("sec_key").value= key1;
								var httpResponseCode = (xhr.status);
								console.log('httpResponseCode: ' + httpResponseCode);
								console.log(data);
								json = JSON.parse(data);
								//key = xhr.getResponseHeader("security-key");
								//console.log(key)
								document.getElementById("payee_acc_name").value= json.ben_name;
								document.getElementById("payee_acc_name1").value= json.ben_name;
								document.getElementById("payee_acc_bank1").value= json.bank_name;
								document.getElementById("payee_acc_bank").value= json.bank_name;
								$("#overlay").removeClass('starting');
							},
							error: function( jqXhr, textStatus, errorThrown ){
								console.log( errorThrown );
								console.log( jqXhr );
								flag = false;
								//$('#acc_no_error').html( jqXhr );
								$("#overlay").removeClass('starting');
							}
							});
						}
						
					}
					
				}