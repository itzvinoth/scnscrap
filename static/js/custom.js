$(document).ready(function() {
	$('#loadData').click(function() {
		$.blockUI({ css: {
			border: 'none',
			background: 'transparent',
			opacity: 1,
			color: '#fff'
		},
		message: '<div class="three-quarters">Loading</div>',
		overlayCSS: { backgroundColor: '#eeeeee' }});
	});
});

$(document).ajaxStop($.unblockUI);

function loadAjax() {
	console.log("Loading")
	var likesLen = [], titleLen = [];
	function checkData(test) {

			for (var i=0;i<test.length;i++) {
				likesLen.push(Number(JSON.stringify(test[i]["likes"])))
				titleLen.push(JSON.stringify(test[i]["title"]))
				test[i].y = test[i].likes
				test[i].url = "http://scn.sap.com" + test[i].link
				delete test[i].likes
				delete test[i].link
			}
			console.log(JSON.stringify(likesLen))
			console.log(JSON.stringify(titleLen))
			console.log(JSON.stringify(test))
			$('#container').highcharts({
				chart: {
					type: 'column'
				},
						title: {
								text: 'Blog',
								x: -20 //center
						},
						subtitle: {
								text: 'Number of likes per blog ',
								x: -20
						},
				plotOptions: {
								series: {
										cursor: 'pointer',
										point: {
												events: {
														click: function () {
																//location.href = this.options.url;
																window.open(this.options.url,'_blank')
														}
												}
										}
								}
						},
						series: [{
								name: 'Likes',
								data: test
						}],
						xAxis: {
								labels: {
										enabled: false
								},
								categories: titleLen
						},

				});
		};
	(function(){
		$.ajax({
			url: "/arr/",
			type: "GET",
			dataType: "JSON",
			success: function (data, status, jqXHR) {
				checkData(data);
				// execute if success response
			},
			error: function (jqXHR, status, err) {
				console.log(error);
				// execute if error response
			},
			complete: function (jqXHR, status) {
				// execute after success or error response
			}
		})
	})();
}
