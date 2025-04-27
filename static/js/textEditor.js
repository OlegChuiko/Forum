$(document).ready(function () {
    $("#txtEditor").Editor();

    $("form").on("submit", function () {
        const content = $(".Editor-editor").html();  
        $("#txtEditor").val(content);  
    });
});