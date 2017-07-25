$(document).ready(function() {
	var arrindexs = {};
    var arrhides = ["splash", "introduction", "interlude", "fall-main", "spring-main", "interlude-2"];
    var currentsection = getCurrentSection();
    var sectionids = $("section.v").map(function(){return this.id; }).get()
	
	function update() {
		console.log('called');
		var arrclasses = "";
		if (arrhides.indexOf(currentsection) != -1) {
			arrclasses += "left-hide right-hide ";
        } else if (arrindexs[currentsection][0] == arrindexs[currentsection][1]-1) {
			arrclasses += "right-hide ";
        } else if (arrindexs[currentsection][0] == 0) {
			arrclasses += "left-hide ";
		}
		if (currentsection == "splash") {
			arrclasses += "up-hide ";
		} else if (currentsection == "retrospective") {
			arrclasses += "down-hide ";
		}
		$("body").attr('class',arrclasses + currentsection);
	}
	
	function getCurrentSection() {
		var current = "splash"
		var sectionids = $("section.v").map(function(){return this.id; }).get()
		sectionids.forEach(function(sectionid) {
			if(($(window).scrollTop() + 100) >= $("#" + sectionid).position().top){
				current = sectionid
			};
		});
		return current;
	};
	
	function up() {
		 if (sectionids.indexOf(currentsection) != 0) {
            var next = sectionids[sectionids.indexOf(currentsection) - 1];
        } else {
            var next = currentsection;
        }
        if (next != undefined && next != currentsection) {
            $("html, body").animate({
                scrollTop: $("#"+next).offset().top
            }, 300);
        }
		return next;
    };
	
	function down() {
		if (sectionids.indexOf(currentsection) != sectionids.length-1) {
            var next = sectionids[sectionids.indexOf(currentsection) + 1];
        } else {
            var next = currentsection;
        }
        if (next != undefined && next != currentsection) {
            $("html, body").animate({
                scrollTop: $("#"+next).offset().top
            }, 300);
        }
		return next;
	}
		
	$("section.v").each(function() {
        var id = $(this).attr("id");
        arrindexs[id] = [0];
        arrindexs[id].push($(this).children("section.h").length);
        var margin = 50;
        $(this).children("section.h").each(function() {
            $(this).css("margin-left",margin+"%");
            margin=margin+100;
        });
    });
	
	update();
    
	$(document).keydown(function(e){
		var code = e.keyCode || e.which;
		if(code == 38) {
			currentsection=up();
		} else if (code == 40) {
			currentsection=down();
		} else if (code == 39 && !(arrindexs[currentsection][0] == arrindexs[currentsection][1]-1)) {
			$("#"+currentsection).children("section.h").animate({left:"-=100%"},300);
			arrindexs[currentsection][0] += 1;
		} else if (code == 37 && !(arrindexs[currentsection][0] == 0)) {
			$("#"+currentsection).children("section.h").animate({left:"+=100%"},300);
			arrindexs[currentsection][0] -= 1;
		}
		update();
		if (code == 37 || code == 39) {
			return false;
		}
	});

    $(".up.arrow").click(function(){currentsection=up();update();});
    $(".down.arrow").click(function(){currentsection=down();update();});
	$("#menu a").click(function(){
		targetsection = $(this).attr('href').substring(1);
		currentsection=targetsection;
		update();
	});
	
    $(".right.arrow").on("click",function() {
        $("#"+currentsection).children("section.h").animate({left:"-=100%"},300);
        arrindexs[currentsection][0] += 1;
		update();
    });
	    
    $(".left.arrow").on("click",function() {
        $("#"+currentsection).children("section.h").animate({left:"+=100%"},300);
        arrindexs[currentsection][0] -= 1;
		update();
    });
	
	$("#menu-icon").on("click",function(){
		$("#menu").toggle('slide',{direction:'left'},100);
	})
	
	// $(document).on("scroll",function() {
		// var arrclasses = "";
		// if (arrhides.indexOf(currentsection) != -1) {
			// arrclasses += "left-hide right-hide ";
        // } else if (arrindexs[currentsection][0] == arrindexs[currentsection][1]-1) {
			// arrclasses += "right-hide ";
        // } else if (arrindexs[currentsection][0] == 0) {
			// arrclasses += "left-hide ";
		// }
		// if (currentsection == "splash") {
			// arrclasses += "up-hide ";
		// } else if (currentsection == "retrospective") {
			// arrclasses += "down-hide ";
		// }
		// $("body").attr('class',arrclasses + currentsection);
	// });
});