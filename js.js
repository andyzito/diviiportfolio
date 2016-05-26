$('#dropdown').click(
	function() {
		$('.navbar.n1 li:not(#dropdown)').slideToggle(110)
		$('#dropdown').toggleClass('expanded')
		// $('.navbar.fall').slideToggle(110)
		// $('#dropdown').hide()
	})