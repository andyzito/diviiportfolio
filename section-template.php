<?php
$prev_section=$sections[$current_section-1];
$this_section=$sections[$current_section];
$content=$contents[$this_section];
$current_section=$current_section+1;
$next_section=$sections[$current_section];
?>

<div id="<?php echo $this_section ?>" class="<?php echo $sem ?> section">
	<div class="up arrow" href="#<?php echo $prev_section ?>"></div>
	<div class="left arrow"></div>
	<p><?php echo $content ?></p>
	<div class="right arrow"></div>
	<div class="down arrow" href="#<?php echo $next_section ?>"></div>
</div>