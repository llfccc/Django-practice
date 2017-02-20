function editCode(){

		var p = {};
		$("input[name='transfer_finance']").each(function(){
    		var o = new Object();

			id=$(this).attr("id").substring(16);
			value=$(this).val();
			if (value){
				o.transfer_finance=value;
			}else{
			o.transfer_finance="";
			}
			p[id]=o;
		})

	console.log(p);

		var data = JSON.stringify(p);

		$.ajax({
				  type: 'POST',
					url:'../updatePayment/',
				  data: data,
				  dataType: 'json'
        });
        alert("提交成功,将会自动刷新");
        window.location.reload();
	}
