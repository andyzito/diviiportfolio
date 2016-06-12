<html>
<body>
<?php include "header.php";
$sections=array('fall-main','artificial-intelligence','chinese-1','cs-issues','performatives','programming-science','spring-main','comp-ling','chinese-2','phonology','syntax','semantics');
$current_section=0;
$sem='fall';
$contents=array('fall-main' => 'Fall 2015', 'artificial-intelligence' => 'Artificial Intelligence', 'chinese-1' => 'Intermediate Chinese I', 'cs-issues' => 'Current Issues in Cognitive Science', 'performatives' => 'Performative Utterances', 'programming-science' => 'Programming for Science', 'spring-main' => 'Spring 2016', 'comp-ling' => 'Computational Linguistics', 'chinese-2' => 'Intermediate Chinese II', 'phonology' => 'Speech Sounds and Structure', 'syntax' => 'Introduction to Syntax', 'semantics' => 'A Theory of Meaning');?>
<div id="main">
<?php include "sidenav.php" ?>
<?php include "section-template.php" ?>
<?php include "section-template.php" ?>
<?php include "section-template.php" ?>
<?php include "section-template.php" ?>
<?php include "section-template.php" ?>
<?php include "section-template.php" ?>
<?php $sem='spring'; include "section-template.php"; ?>
<?php include "section-template.php" ?>
<?php include "section-template.php" ?>
<?php include "section-template.php" ?>
<?php include "section-template.php" ?>
<?php include "section-template.php" ?>
</div>
</body>
</html>