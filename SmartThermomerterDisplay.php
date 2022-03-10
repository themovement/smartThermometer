<?php 
$temp_sensor1 = '/sys/bus/w1/devices/28-01144bf8a9aa/w1_slave';
$temp_sensor2 = '/sys/bus/w1/devices/28-01144d0516aa/w1_slave';
$temp_sensor3 = '/sys/bus/w1/devices/28-01144d5718aa/w1_slave';

$line1 = file($temp_sensor1);
$line2 = file($temp_sensor2);
$line3 = file($temp_sensor3);

$tmp1 = explode('=', $line1[1]);
$tmp2 = explode('=', $line2[1]);
$tmp3 = explode('=', $line3[1]);

$tmp1 = number_format($tmp[1] /1000, 1, "");
$tmp1 = $tmp1 * 9.0 / 5.0 + 32.0;

$tmp2 = number_format($tmp2[1] /1000, 1, "");
$tmp2 = $tmp2 * 9.0 / 5.0 + 32.0;

$tmp3 = number_format($tmp3[1] /1000, 1, "");
$tmp3 = $tmp3 * 9.0 / 5.0 + 32.0;

echo $tmp1;

?>
