$(document).ready(function(){

  $("input").on('click', function(){
    if($('#ParentRadio:checked').length > 0) {
      $('.Breeze').css('display','none')
      $('.Station').css('display','none')
      $('.parentid').css('display','none')}

    else if ($('#ChaperoneRadio:checked').length > 0) {
      $('.Station').css('display','none')
      $('.Breeze').css('display','none')
      $('.parentid').css('display','none')}

    else
    {
      $('.Breeze').css('display','block')
      $('.Station').css('display','block')
      $('.parentid').css('display','block')
    }

  });

  $('.toFade').fadeOut(3200, function(){
    console.log("fades");
  });

});
