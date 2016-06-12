$(document).ready(function() {
	$('.down.arrow').click(function() {
		$('html, body').animate({
			scrollTop: $(".fall.section-template").offset().top
		}, 1000);
	});
	$('.up.arrow').click(function() {
		alert('up arrow is click');
	});
});