$(document).ready(function(){
    $("#show-comments").click(function(){
        $("#comments-section").show();
        $("#show-comments").hide();
    });
    var unmarked = $(".post-body").text();
    var markedHTML = marked(unmarked);
    $(".post-body").html(markedHTML);
    $(".home-post-body").each(function(){
        var homeUnmarked = $(this).text();
        var homeMarked = marked(homeUnmarked);
        $(this).html(homeMarked);
    });
});
