function textAreaAdjust(o) {
    o.style.height = "1px";
    o.style.height = (25+o.scrollHeight)+"px";
}

function doProcess(a) {
    debug = "";
    if (a == "text") {
        $('#result_' + a).html('<div class="title">Processing...</div>');
        if ($('#contentsbox').height() > 200) {
            $('#contentsbox').animate({height: '200px'});
        }
        $.post("/process", $('#form_' + a).serialize(), function(data) {
            $('#result_' + a).html('');
            inspected = "<div><div class='title'>* Categorize</div>" + "해당 글은 <span class='blue bold'>Class " + data.class + " : " + getClassName(data.class) + "</span>로 판단됩니다.</div>";
            $('#result_' + a).append(inspected);

            member = "<div class='title'>* Keyword Extraction</div>";
            $.each(data.keyword, function(idx, item) {
                member += "<tr><td>" + idx + "</td><td>" + item[0] + "</td><td>" + item[1] + "</td><td>" + item[2] + "</td></tr>"
            });
            $('#result_' + a).append("<table class='table table-condensed'><tr><th>Rank</th><th>Keyword</hd><th>Morpheme</th><th>Point</th></tr>"+ member +"</table>");
        }, "json");
    } else if (a == "image") {
        $('#result_' + a).html('<div class="title">Processing...</div>');
        $('#form_image').ajaxSubmit({
            dataType: 'json',
            url: '/process',
            success: function(data) {
                debug = data;
                $('#result_' + a).html('');
                html = "<img src='" + data.uploaded + "'>";
                $('#result_' + a).append(html);
            }
        });
    }
}

function getClassName(a) {
    switch(a) {
        case '1':
            return "정치";
            break;

        case '2':
            return "경제";
            break;

        case '3':
            return "2";
            break;

        case '4':
            return "음식";
            break;

        case '5':
            return "5";
            break;

        case '6':
            return "IT";
            break;

        case '7':
            return "스포츠";
            break;
    }
    return "None";
}