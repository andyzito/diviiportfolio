<!DOCTYPE HTML>
<html>
<body>
<?php include "header.php";
include "main.php";
$arrs=array(0,0,0,0);
?>
<div id="menu-container">
	<div id="menu-icon"></div>
	<ul id="menu">
	<a href="/files" target="_self"><li>See all files</li></a>
	<a href="#splash" target="_self"><li>Front Page</li></a>
	<a href="#simons-rock" target="_self"><li>Simon's Rock</li></a>
	<a href="#fall-main" target="_self"><li>Fall 2015</li></a>
	<a href="#spring-main" target="_self"><li>Spring 2016</li></a>
	<a href="#retrospective" target="_self"><li>Retrospective</li></a>
	</ul>
</div>
<div id="main">
<div class="up arrow show"></div>
<div class="left arrow"></div>
<div class="right arrow"></div>
<div class="down arrow show"></div>
<?php
$sem='intro';
include "section-template.php";
include "section-template.php";
include "section-template.php";
include "section-template.php";
$sem='fall';
include "section-template.php";
include "section-template.php";
include "section-template.php";
include "section-template.php";
include "section-template.php";
include "section-template.php";
$sem='spring';
// include "section-template.php";
include "section-template.php";
include "section-template.php";
include "section-template.php";
include "section-template.php";
include "section-template.php";
include "section-template.php";
include "section-template.php";
?>
</div>
<!DOCTYPE HTML>
</body>
</html>
