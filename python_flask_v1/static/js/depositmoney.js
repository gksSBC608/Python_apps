				var acc_number;
				function do_initials(){
					
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
							 document.getElementById("acc_balance").innerHTML=balance;
							 $("#overlay").removeClass('starting');
						});
				}
				
				function deposit_money(){
					var flag = false;
					$("span[id='message']").html('');
					var username = document.getElementById('username').value;
					var amount = $("input[name='amount']").val();
					//alert(username+","+amount+","+acc_number);
					console.log(amount);
					if(amount===''){
						$("span[id='message']").html("<font color=red>Enter amount</font>");
						document.getElementById('amount').focus();
					}else{
						$("#overlay").addClass('starting');
						$.post("money.deposit",
						{
							acc_number: acc_number,
							amount:amount
						},
						function(data,status){
							//console.log("Data: " + data + "\nStatus: " + status);
							$("span[id='message']").html(data);
							$("input[name='amount']").val('');
							flag = true;
							//$("#overlay").removeClass('starting');
							$('#message').html( "<font color='green'>Money deposited</font>" );
							
							var accountbalance_url = "accountbalance?acc_number="+acc_number;
							$.get(accountbalance_url, function(data, status){
								console.log(data);
								json = JSON.parse(data);
								console.log("Data: " + json + "\nStatus: " + status);
								var balance = json.balance;
								document.getElementById("acc_balance").innerHTML=balance;
								$("#overlay").removeClass('starting');							
							});
							
						});			
						
					}				
					
				}