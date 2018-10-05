			var flag = true;
			var key = "";
			function process_addpayee(){
			
				var payee_url = "payee.add";
				var data = { payee_acc_no: $("input[name=payee_acc_no]").val(), payee_acc_name : $("input[name=payee_acc_name]").val(), payee_acc_bank : $("input[name=payee_acc_bank]").val()}
				if(flag){
					/*
					$.post(payee_url,data, 
					function(returnedData,status){
						console.log(returnedData);
						console.log(status);
						$("span[id='message']").html(returnedData);
					}).fail(function(){
							console.log("error");
					});
					*/
					
					$.ajax({
					url: payee_url,
					type: 'POST',
					data: data,
					headers: { 'security-key': key },
					//async: false,
					success: function( data, status,xhr){
						console.log(data);
						console.log(status);
						$("span[id='message']").html(data);
					},
					error: function( jqXhr, textStatus, errorThrown ){
						console.log( errorThrown );
						console.log( jqXhr );
						$('#acc_no_error').html( jqXhr );
					}
					});
					
				}
						
			}
			
			function check_account_number(){
			
				var url = "check_benficiary";
				//var acc_no = $("input[name=payee_acc_no]").val();
				var arr = { payee_acc_no: $("input[name=payee_acc_no]").val()};
				 $.ajax({
					url: url,
					type: 'POST',
					data: JSON.stringify(arr),
					contentType: 'application/json; charset=utf-8',
					dataType: 'json',
					//headers: { 'x-my-custom-header': 'some value' },
					async: false,
					success: function( data, status,xhr){
						var httpResponseCode = (xhr.status);
						console.log('httpResponseCode: ' + httpResponseCode);
						if(data.acc_exists){							
							console.log( "Beneficiary already exists");
							$('#acc_no_error').html( "Beneficiary already exists" );
							$('#acc_no_error').focus();
							flag = false;
						}else{
							$('#acc_no_error').html( "" );
							//$('#acc_no_error').blur();
							key = xhr.getResponseHeader("security-key");
							console.log(key)
							flag = true;
						}
						// 1234567790
					},
					error: function( jqXhr, textStatus, errorThrown ){
						console.log( errorThrown );
						console.log( jqXhr );
						$('#acc_no_error').html( jqXhr );
					}
				});
			}