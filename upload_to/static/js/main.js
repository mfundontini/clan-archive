$(document).ready(function(){
    $("#show-comments").click(function(){
        $("#comments-section").show();
        $("#show-comments").hide();
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
