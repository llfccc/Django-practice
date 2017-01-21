// 获取点击的供应商的所有数据
function updateInfo(id, url) {
    data = {};
    data.id = id;

    $.ajax({
        url: url,
        type: "post",
        dataType: 'json',
        data: data,
        success: function (res) {
            // result = res[0];
            result=res;
            $("#supplier_id").val(result.id);

            for (res in result) {
                res2 = "#" + res;
                $(res2).val(result[res]);
            }

        }
    });
}

// 更新所有数据
function updateAll(url) {
    var p = {};

    $(":text").each(function () {
        var o = {};
        id = $(this).attr("id");
        value = $(this).val();
        if (id) {
            p[id] = value;
        }
    });
    var data = JSON.stringify(p);
    console.log(p);
    $.ajax({
        type: 'POST',
        url: url,
        dataType: 'json',
        data: data,
        success: function (res) {
            console.log(res);            
            if (res.result == 'ok') {
                alert("更新成功");
            } else {
                alert("更新失败，您可能没有权限或者没有更改内容");
            }
        },
        error: function (res) {
            console.log(res);
            alert('没有得到响应');
        }
    });

     window.location.reload();
}

// 更新备选供应商所有数据
function updateOptionalAll(url) {
    var p = {};

    $(":text").each(function () {
        var o = {};
        id = $(this).attr("id");
        value = $(this).val();
        if (id) {
            p[id] = value;
        }
    });
    var data = JSON.stringify(p);
    $.ajax({
        type: 'POST',
        url: url,
        data: data,
        dataType: 'json',
        success: function (res) {
            console.log(res);
            if (res.result == 'ok') {
                alert("更新成功");
            } else {
                alert("更新失败，您可能没有权限或者没有更改内容");
            }
        },
        error: function (res) {
            console.log(res);
            alert('没有得到响应');
        }
    });


    window.location.reload();
}
// 新增一个供应商
function addNew(url) {
    $.get(url, function (text) {
        if (text == 'ok') {
            alert("新增成功");
             window.location.reload();
        } else {
            alert("新增失败，您可能没有权限");
        }
    });


}
// 新增一个备选供应商

function addOptionalNew(url) {
    $.get(url, function (text,res) {
        if (text='ok') {
            console.log(text);
            alert("新增成功");
             window.location.reload();
        } else {
          alert(text.status);
            alert("新增失败，您可能没有权限");
        }
    });
}

function updateContact(url) {
    var p = {};

    $(":text").each(function () {
        var o = {};
        id = $(this).attr("id");
        value = $(this).val();
        if (id) {
            p[id] = value;
        }
    });


    $.ajax({
        type: 'POST',
        url: url,
        data: p,
        dataType: 'json',
        success: function (text, res) {
            if (text.status == 1) {
                alert("更新联系人成功");
            } else {
                alert("更新失败，您可能没有权限或者没有更改内容");
            }
        },
        error: function (res) {
            alert('没有得到响应');
        }
    });

    window.location.reload();
}

function infoOptional(id, url) {
    data = {};
    data.id = id;

    $.ajax({
        url: url,
        type: "post",
        dataType: 'json',
        data: data,
        success: function (res) {
            result = res;
            $("#supplier_id").val(result['id']);

            for (res in result) {
                res2 = "#" + res;
                $(res2).val(result[res]);
            }

        }
    });
}
