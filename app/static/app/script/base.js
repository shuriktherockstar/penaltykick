$(document).ready(
    function() {
        $('button[type="submit"]').hover(
            function () {
                $(this).css('color', '#063367')
            },
            function () {
                $(this).css('color', '#000000')
            }
        )
    }
);

$(document).ready(
    function() {
        $('textarea, input[type="text"]').focus(
            function () {
                $(this).css('background-color', '#fdfdfd')
            }
        )
    }
);

$(document).ready(
    function() {
        $('textarea, input[type="text"]').blur(
            function () {
                $(this).css('background-color', '#ffffff')
            }
        )
    }
);