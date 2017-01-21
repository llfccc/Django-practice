

function selectAll(){
	$(":checkbox").each(function(){
	if($(this).prop("checked")){
	$(this).prop("checked",false);
	}else{
	$(this).prop("checked",true);
	}
	});
}

function editCode() {

    var p = {};
    $("input[name='checked']").each(function() {
        var o = new Object()
        id = $(this).attr("id").substring(7);
        value=$(this).prop("checked");
        if (value) {
            o.checked = true;
        } else {
            o.checked = false;
        }
        p[id] = o
    })

    console.log(p);

    var data = JSON.stringify(p);

    $.ajax({
        type: 'POST',
        //url: 'http://127.0.0.1:8000/stockCode/varifyApplication/',
        url: '../varifyApplication/',
        data: data,
        dataType: 'json'
    });
    alert("提交成功,将会自动刷新");
    window.location.reload();
}
