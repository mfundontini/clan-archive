$(document).ready(function(){
    $("#show-comments").click(function(){
        $("#comments-section").show();
        $("#show-comments").hide();
    });

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
// The code below is used to set markdown on the client side and not the server, markdown-deux does back-end markdown
//    var unmarked = $(".post-body").text();
//    var markedHTML = marked(unmarked);
//    $(".post-body").html(markedHTML);
//    $(".home-post-body").each(function(){
//        var homeUnmarked = $(this).text();
//        var homeMarked = marked(homeUnmarked);
//        $(this).html(homeMarked);
//    });
});
