$(document).ready(function(){
	$("#queryForm").hide();
	$("#id_radio_0").click(function(){
    		$("#queryForm").show();
});
	$("#id_radio_1").click(function(){
    		$("#queryForm").hide();
});
});

$(function() {
	$("#id_dateStart").datepicker({ dateFormat: 'dd-mm-yy' });
	$("#id_dateEnd").datepicker({ dateFormat: 'dd-mm-yy' });
	$("#id_timeStart").timepicker({template:false, minuteStep: 1,showSeconds: true,showMeridian: false});
	$("#id_timeEnd").timepicker({template:false,minuteStep: 1,showSeconds: true,showMeridian: false});
});




