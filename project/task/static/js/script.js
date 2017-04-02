$(document).ready(function() {
	function isValidDate(dateString) {
		var regEx = /^\d{2}.\d{2}.\d{4}$/;
		return dateString.match(regEx) != null;
	}

	$('.datepicker').pikaday();

	$('#add_task_form').on('submit', function(event) {
		event.preventDefault();
		
		if (!isValidDate($('#id_estimate').val())) {
			alert('Дата должна быть в виде: `dd.mm.yyyy`!');
			return;
		}

		form = $(this);
		$.ajax({
			url: '/add_task/',
			type: 'POST',
			data: form.serialize(),
			success: function(template) {
				$("#id_title").val('');
				$("#id_estimate").val('');
				$(".add_task_item").before(template);
			},
			error: function(xhr, errmsg, err) {
				alert("Возникла ошибка при добавлении задачи!");
			}
		});
	})

	$('.done').on('click', function(event) {
		elem = $(this);
		$.ajax({
			url: '/task_complete/',
			type: 'POST',
			data: {
				'id': elem.parent().attr('task-id'),
				'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
			},
			success: function(data) {
				if (data.code == 200) {
					var parent = elem.parent();
					parent.fadeOut(300, function(){
						parent.remove();
					})
				}
				else {
					alert("Упс! Возникла ошибка...");
				}
			},
			error: function(xhr, errmsg, err) {
				alert("Упс! Возникла ошибка...");
			}
		});
	})

	$('.task').on('dblclick', function(event) {
		elem = $(this);
		$.ajax({
			url: '/task_detail/',
			type: 'GET',
			data: {
				'id': elem.attr('task-id'),
			},
			success: function(template) {
				$("#task_detail").html(template);
			},
			error: function(xhr, errmsg, err) {
				alert("Упс! Возникла ошибка...");
			}
		});
	})
});