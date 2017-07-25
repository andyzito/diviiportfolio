<?php
$sectionnames = array_keys($sections);
$prev_section=$sectionnames[$current_section-1];
$this_section=$sectionnames[$current_section];
$content=$sections[$this_section];
$current_section=$current_section+1;
$next_section=$sectionnames[$current_section];
?>

<section id="<?php echo $this_section ?>" class="<?php echo $sem ?> v">
	<?php
		if ($arrs[0]) {
			echo '<div class="up arrow" href="#'.$prev_section.'"></div>';
		};
		if ($arrs[1]) {
			echo '<div class="left arrow"></div>';
		};
		
		foreach ($content as $section => $value) {
			echo "<section class='".$section." h'>";
			foreach ($value as $piece => $stuff) {
				echo "<p class='".$piece."'>".$stuff."</p>";
			}
			echo "</section>";
		}
		
		if ($arrs[2]) {
			echo '<div class="right arrow"></div>';
		}
		if ($arrs[3]) {
			echo '<div class="down arrow" href="#'.$next_section.'"></div>';
		}
		?>
</section>