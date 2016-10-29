 $(document).ready(function(){

 var kidsID;

 $('#confirm').on('click', function(){
 	kidsID = document.getElementById('ID').value
 	$('.checkin').text("Confirmed Check in for " + kidsID)
 })

 $('.toFade').fadeOut(3200, function(){
   console.log("fades");
 });

})
