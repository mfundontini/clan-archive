$(document).ready(function(){
    $("#show-comments").click(function(){
        var threadUrl = $(this).attr("data-url");
        function handleSuccess(data, textStatus, jqXHR){
            $("#comments-section").html(data.html);
        };
        function handleErrors(jqXHR, textStatus, errorThrown){
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        };
        $.ajax({
            method: "GET",
            url: threadUrl,
            success: handleSuccess,
            error: handleErrors,
        });
        $("#show-comments").hide();
    });

    $('#comments-section').on("click", "#post-comment", function(event) {
        event.preventDefault();
        var form = $(this).parent();
        var formData = form.serialize()
        var postUrl = $(this).attr("post-url")
        function handlePostSuccess(data, textStatus, jqXHR){
            $("#comments-section").html(data.html);
        };
        function handlePostErrors(jqXHR, textStatus, errorThrown){
            console.log(jqXHR);
            console.log(textStatus);
            console.log(errorThrown);
        };
        $.ajax({
            method: "POST",
            url: postUrl,
            data: formData,
            success: handlePostSuccess,
            error: handlePostErrors,
        });
    });

    $("#id_comment_body").val("");

    $("#show-preview").click(function(){
        $("#edit-container").addClass("pull-right");
        $("#show-preview").attr("disabled", "disabled");
        $("#preview-container").addClass("pull-left").show();
        var previewTitle = $("#id_title").val();
        var previewBody = marked($("#id_body").val());
        $("#title-preview").text(previewTitle);
        $("#content-preview").html(previewBody);
        $("#id_title").focus(function(){
            $(this).keyup(function(){
                previewTitle = $(this).val();
                $("#title-preview").text(previewTitle);
            });
        });
        $("#id_body").focus(function(){
            $(this).keyup(function(){
                previewBody = marked($(this).val());
                $("#content-preview").html(previewBody);
            });
        });

    });
    $("#hide-preview").click(function(){
        $("#edit-container").removeClass("pull-right");
        $("#preview-container").removeClass("pull-left").hide();
        $("#show-preview").removeAttr("disabled");
    });
//  This is the normal click event for the add reply buttons, however, we need to cater for dynamically added buttons so we use on("click")
//    $(".reply-textarea-button").click(function(){
//        $(this).next().show();
//        $(this).hide();
//    });

    $('#comments-section').on("click", ".reply-textarea-button", function() {
        $(this).next().show();
        $(this).hide();

    });

//    The code below is used to set markdown on the client side and not the server, markdown-deux does back-end markdown
//    var unmarked = $(".post-body").text();
//    var markedHTML = marked(unmarked);
//    $(".post-body").html(markedHTML);
//    $(".home-post-body").each(function(){
//        var homeUnmarked = $(this).text();
//        var homeMarked = marked(homeUnmarked);
//        $(this).html(homeMarked);
//    });
});
