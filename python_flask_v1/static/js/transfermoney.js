var threshold_balance = 1000;
var available_balance;
var submit_btn;
				
function do_initials(){
				
	submit_btn = $("input[type='submit']");
	submit_btn.prop('disabled', true);
	var payee_acc_name_field = $("input#payee_acc_name1");
	var payee_acc_bank_field = $("input#payee_acc_bank1");
	payee_acc_name_field.prop('disabled', true);
	payee_acc_bank_field.prop('disabled', true);
				
	var url = "accountdetail";
	$("#overlay").addClass('starting');
	$.get(url, function(data, status){
		//	console.log(data);
		json = JSON.parse(data);
		//console.log("Data: " + json + "\nStatus: " + status);
		acc_number = json.acc_number;
		document.getElementById("acc_number_label").innerHTML=acc_number;
		document.getElementById("acc_number").value=acc_number;
		var balance = json.acc_balance;
		available_balance = balance;
		document.getElementById("acc_balance").innerHTML="₹ "+balance;
		// "₹ "
	});
						/*
						document.getElementById("acc_number").value=acc_number;
						document.getElementById("user_id").value=username;
						document.getElementById("acc_number_label").innerHTML=acc_number;
						var url = "accountbalance?acc_number="+acc_number;
						$.get(url, function(data, status){
							//console.log(data);
							json = JSON.parse(data);
							//console.log("Data: " + json + "\nStatus: " + status);
							 var balance = json.balance;
							 available_balance = balance;
							 document.getElementById("acc_balance").innerHTML=json.balance;
							 if(balance<=threshold_balance){
							  $("input").prop('disabled', true);
							  alert("low balance, must be more than "+threshold_balance);
							 }
							
						});
						*/
				var beneficiaries_url = "getpayee_accounts";
					
				$.ajax({
							type:'GET',
							beforeSend: function(){
								//$('.ajax-loader').css("visibility", "visible");
								
							},
							url:beneficiaries_url,
							success:function(data){
								
								if(data.length<=6){
									alert("Payee not added");
									submit_btn.prop('disabled', true);
								}
								$("#overlay").removeClass('starting');
							json = JSON.parse(data);
							//console.log(json);
							var select_str = "<select name='payee_acc_number' id='payee_acc_number' style='width: 167px;'onchange='load_payee_info()'>";
							var options ="<option value='---'>--------select--------</option>";
							json.forEach(function(item){
							//console.log(item);
							var option = "<option value="+item+">"+item+"</option>";
							options += option;
							});
							//console.log(options);
							select_str += options+"</select>";
							//console.log(select_str);
							document.getElementById("acc_list").innerHTML=select_str;
							},
							complete: function(){
								//$('.ajax-loader').css("visibility", "hidden");
								
							}
					});
				}
				
				function load_payee_info(){
					
					var payee_acc_number = document.getElementById("payee_acc_number").value;
					//console.log(payee_acc_number);
					if("---"===payee_acc_number){
						document.getElementById("payee_acc_name").value= "";
							document.getElementById("payee_acc_name1").value= "";
							document.getElementById("payee_acc_bank1").value= "";
							document.getElementById("payee_acc_bank").value= "";
							document.getElementById("amount_to_transfer").value= "";
						submit_btn.prop('disabled', true);
					}else{
	
						var url = "getpayee_data?payee_acc_number="+payee_acc_number;
						$("#overlay").addClass('starting');
						$.get(url, function(data, status){
							
							json = JSON.parse(data);
							document.getElementById("payee_acc_name").value= json.ben_name;
							document.getElementById("payee_acc_name1").value= json.ben_name;
							document.getElementById("payee_acc_bank1").value= json.bank_name;
							document.getElementById("payee_acc_bank").value= json.bank_name;
							submit_btn.prop('disabled', false);
							$("#overlay").removeClass('starting');
						});
					}
					
				}
				
				
				
				function validate_transfer_amount(){
				 
				 var amount = parseInt($("input[name='amount_to_transfer']").val());
				 //alert(amount);
				 //console.log(amount);
				 //console.log(available_balance);
				 //console.log(threshold_balance);
				 //var submit_btn = $("input[type='submit']");
				 if(available_balance-amount <= threshold_balance){
					alert("amount entered is more than the permited, account balance will go below "+threshold_balance);
					submit_btn.prop('disabled', true);
					return false;
				 }else{
					submit_btn.prop('disabled', false);
					return true;
				 }
				
				}
				
				function validate_input(){
					var payee_acc_number = document.getElementById("payee_acc_number").value;
					//console.log(payee_acc_number);
					if("---"===payee_acc_number){
						alert("Select a payee account number");
						submit_btn.prop('disabled', true);
						return false;
					}else{
						submit_btn.prop('disabled', false);
						return true;
					}
					
				}
				
				function process_transferMoney(){
				
				var isPayeeAccValid =  validate_input()
				//alert(isPayeeAccValid);
				var flag = false;
				if(isPayeeAccValid){
					if(validate_transfer_amount()){
						flag = validate_transfer_amount();
					}
				}
				
				if(flag){
					
					var account_number = $("#acc_number").val();	
					var payee_acc_number = $("#payee_acc_number").val();
					var payee_acc_name = $("#payee_acc_name").val();	
					var payee_acc_bank = $("#payee_acc_bank").val();
					var	amount_to_transfer = $("#amount_to_transfer").val();		
					//alert(account_number+" "+payee_acc_number+" "+payee_acc_name+" "+payee_acc_bank );
					$("#overlay").addClass('starting');
					var arr = {account_number:account_number,
								payee_acc_number:payee_acc_number,
								payee_acc_name:payee_acc_name,
								payee_acc_bank:payee_acc_bank,
								amount_to_transfer:amount_to_transfer
								};
					console.log(arr);
					$.ajax({
					url: "money.transfer",
					type: 'POST',
					data: JSON.stringify(arr),
					contentType: 'application/json; charset=utf-8',
					dataType: 'json',
					//headers: { 'x-my-custom-header': 'some value' },
					async: false,
					success: function( data, status,xhr){
						//alert(data);
						console.log(data)
						$('#message').html( data.message );
					},
					error: function( jqXhr, textStatus, errorThrown ){
						console.log( errorThrown );
						console.log( jqXhr );
						$('#message').html( jqXhr );
					}
				});
				
					var url = "accountbalance?acc_number="+account_number;
				
					$.get(url, function(data, status){
						console.log(data);
						json = JSON.parse(data);
						console.log("Data: " + json + "\nStatus: " + status);
						var balance = json.balance;
						document.getElementById("acc_balance").innerHTML="₹ "+balance;
						$("#overlay").removeClass('starting');	 
							
					});
					
				}else{
				alert("No permit");
				}
				
				
				}