$(document).ready(function() {
	$('#loadData, #sortLikes').click(function() {
		$.blockUI({ css: {
			border: 'none',
			background: 'transparent',
			opacity: 1,
			color: '#fff'
		},
		message: '<div class="plus">Loading</div>',
		overlayCSS: { backgroundColor: '#eeeeee' }});
	});
});

$(document).ajaxStop($.unblockUI);

var dataGlobal = [];

function loadAjax(callBack, desc) {
	(function(){
		$.ajax({
			url: "/arr/",
			type: "GET",
			dataType: "JSON",
			success: function (data, status, jqXHR) {
				dataGlobal = data;
				callBack(data, desc);
				// execute if success response
			},
			error: function (jqXHR, status, err) {
				console.log(err);
				// execute if error response
			},
			complete: function (jqXHR, status) {
				// execute after success or error response
			}
		})
	})();
}

function sortData(data, key, desc) {
	data.sort(function(a,b) {
		return parseInt(a[key]) - parseInt(b[key])
	});
	return data;
}

function loadGraph() {
	loadAjax(plotGraph);
}

function sortByLikes(desc) {
	if(dataGlobal.length === 0) {
		loadAjax(plotSortedLike, desc);
	} else {
		plotSortedLike(dataGlobal, desc);
	}
}

function plotSortedLike(data, desc) {
	plotGraph(sortData(data, 'likes'), desc);
}

function plotGraph(data, desc) {
	setTimeout($.unblockUI, 500);

	if(desc === true) {
		data = data.reverse()
	}

	var likesLen = [], titleLen = [];
	for (var i=0;i<data.length;i++) {
		likesLen.push(Number(JSON.stringify(data[i]["likes"])))
		titleLen.push(JSON.stringify(data[i]["title"]))
		data[i].y = data[i].likes
		data[i].url = "http://scn.sap.com" + data[i].link
	}

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
				colorByPoint: true,
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
			data: data
		}],
		xAxis: {
			labels: {
					enabled: false
			},
			categories: titleLen
		},
	});
}
