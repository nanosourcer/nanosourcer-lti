$(document).ready(function() {

	$('#user-sort').on('click', function() {

		if ($(this).attr('class') == 'glyphicon glyphicon-sort-by-alphabet') {

			$(this).attr('class', 'glyphicon glyphicon-sort-by-alphabet-alt')

			var sorted = $(".analytics-row").sort(function(a,b) { 

				if ($($(a).children()[0]).text() < $($(b).children()[0]).text()) {

					return -1;

				} else { 

					return 1;

				} 

			});

			$('#sortable-table').empty();
			$('#sortable-table').append(sorted);

		} else {

			$(this).attr('class', 'glyphicon glyphicon-sort-by-alphabet')

			var sorted = $(".analytics-row").sort(function(a,b) { 

				if ($($(a).children()[0]).text() < $($(b).children()[0]).text()) {

					return 1;

				} else { 

					return -1;

				} 

			});

			$('#sortable-table').empty();
			$('#sortable-table').append(sorted);

		}

	})

	$('#image-sort').on('click', function() {

		if ($(this).attr('class') == 'glyphicon glyphicon-sort-by-alphabet') {

			$(this).attr('class', 'glyphicon glyphicon-sort-by-alphabet-alt')

			var sorted = $(".analytics-row").sort(function(a,b) { 

				if ($($(a).children()[1]).text() < $($(b).children()[1]).text()) {

					return -1;

				} else { 

					return 1;

				} 

			});

			$('#sortable-table').empty();
			$('#sortable-table').append(sorted);

		} else {

			$(this).attr('class', 'glyphicon glyphicon-sort-by-alphabet')

			var sorted = $(".analytics-row").sort(function(a,b) { 

				if ($($(a).children()[1]).text() < $($(b).children()[1]).text()) {

					return 1;

				} else { 

					return -1;

				} 

			});

			$('#sortable-table').empty();
			$('#sortable-table').append(sorted);

		}

	})

	$('#uri-sort').on('click', function() {

		if ($(this).attr('class') == 'glyphicon glyphicon-sort-by-alphabet') {

			$(this).attr('class', 'glyphicon glyphicon-sort-by-alphabet-alt')

			var sorted = $(".analytics-row").sort(function(a,b) { 

				if ($($(a).children()[2]).text() < $($(b).children()[2]).text()) {

					return -1;

				} else { 

					return 1;

				} 

			});

			$('#sortable-table').empty();
			$('#sortable-table').append(sorted);

		} else {

			$(this).attr('class', 'glyphicon glyphicon-sort-by-alphabet')

			var sorted = $(".analytics-row").sort(function(a,b) { 

				if ($($(a).children()[2]).text() < $($(b).children()[2]).text()) {

					return 1;

				} else { 

					return -1;

				} 

			});

			$('#sortable-table').empty();
			$('#sortable-table').append(sorted);

		}

	})

	$('#label-sort').on('click', function() {

		if ($(this).attr('class') == 'glyphicon glyphicon-sort-by-alphabet') {

			$(this).attr('class', 'glyphicon glyphicon-sort-by-alphabet-alt')

			var sorted = $(".analytics-row").sort(function(a,b) { 

				if ($($(a).children()[3]).text() < $($(b).children()[3]).text()) {

					return -1;

				} else { 

					return 1;

				} 

			});

			$('#sortable-table').empty();
			$('#sortable-table').append(sorted);

		} else {

			$(this).attr('class', 'glyphicon glyphicon-sort-by-alphabet')

			var sorted = $(".analytics-row").sort(function(a,b) { 

				if ($($(a).children()[3]).text() < $($(b).children()[3]).text()) {

					return 1;

				} else { 

					return -1;

				} 

			});

			$('#sortable-table').empty();
			$('#sortable-table').append(sorted);

		}

	})


});