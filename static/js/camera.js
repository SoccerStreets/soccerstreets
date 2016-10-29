// Grab elements, create settings, etc.
var video = document.getElementById('video');

// Get access to the camera!
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        video.src = window.URL.createObjectURL(stream);
        video.play();
    });
}


var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var video = document.getElementById('video');


function draw() {
  var ctx = context;
  ctx.canvas.width  = window.innerWidth;
  ctx.canvas.height = window.innerHeight;
  //...drawing code...
}


// Trigger photo take
document.getElementById("snap").addEventListener("click", function() {
	context.drawImage(video, 0, 0, 640, 480);
	//draw()
});