$(document).ready(function() {
    // $('.sidenav .about').on("click", function() {
    //
    // });

});

function openNav() {
    document.getElementById("mySidenav").style.width = "100%";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}


$(document).ready(function() {

    $("input").on('click', function() {
        if ($('#ParentRadio:checked').length > 0) {
            $('.signup-fields').css('display', 'flex');
            $('.breeze-card').css('display', 'none');
            $('.marta-station').css('display', 'none');
            $('.parent-code').css('display', 'none');
        } else if ($('#ChaperoneRadio:checked').length > 0) {
            $('.signup-fields').css('display', 'flex');
            $('.marta-station').css('display', 'none');
            $('.breeze-card').css('display', 'none');
            $('.parent-code').css('display', 'none');
        } else if ($('#KidRadio:checked').length > 0){
            $('.signup-fields').css('display', 'flex');
            $('.breeze-card').css('display', 'block');
            $('.marta-station').css('display', 'block');
            $('.parent-code').css('display', 'block');
        } else {
            $('.signup-fields').css('display', 'none');
        }

    });

    $('.toFade').fadeOut(3200, function() {
        console.log("fades");
    });

    $('.qr-button').on('click', function() {
        $('.qrcode-modal').css('display', 'flex');
    });

    $('.qr-close').on('click', function() {
        $('.qrcode-modal').css('display', 'none');
    });

});
