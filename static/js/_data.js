function editCode(){

		var p = {};
		$("input[name='code']").each(function(){
    		var o = new Object()
			id=$(this).attr("id").substring(4);
			value=$(this).val();
			if (value){
				o.code=value;
			}else{
			o.code="";
			}
			p[id]=o
		})

	console.log(p);

		var data = JSON.stringify(p);

		$.ajax({
				  type: 'POST',
					url:'../receiveCode/',
				  //url: 'http://127.0.0.1:8000/stockCode/receiveCode/',
					//url: 'http://192.168.8.179:1000/stockCode/receiveCode/',
				  data: data,
				  dataType: 'json'
        });
        alert("提交成功,将会自动刷新");
        window.location.reload();
	}
