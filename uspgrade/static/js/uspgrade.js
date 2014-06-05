$(document).ready(function(){

	/*
	 * Responder
	 */

	$("#ajax_submit_resposta").submit(function(){
		var data = $(this).serialize();
		var form = this;
		$.post("/api/responder", data)
		.done(function(response) {
			if (response.result == 'success') {

				// Get values for jQuery response
				
				var id = form.post.value;
				var name = form.name.value;
				var content = form.content.value;
				var rand_target = "scroll-" + (1 + Math.floor(Math.random() * 10000));
				var message = '<div class="comment-content pull-left" id="' + rand_target + '">';
				message += '<h4>' + name + ' <small>Alguns segundos atrás</small></h4>';
				message += '<p>' + content + '</p>';
        		message += '</div>';

				// Tell user everything is ok

				alert("Seu comentário foi enviado. Atualize a página para ver a resposta!");
			}
			else
				alert('Houve algum erro no preenchimento dos dados.');
		})
		.fail(function() {
			alert( "Houve alguma falha no sistema. Por favor, tente novamente. Se o erro persistir, por favor, entre em contato." );
		});
		return false;
	});

	/*
	 * Votar
	 */

	$(".botao-votar").click(function(){
		sugestao = $(this).attr('data-sugestao');
		voto     = $(this).attr('data-voto');
		data = {
			sugestao: sugestao,
			voto: voto
		}

		$.post("/api/votar", data)
		.done(function(response) {
			alert(response.message);
			if (response.result == 'success')
				location.reload();
		})
		.fail(function() {
			alert( "Houve alguma falha no sistema. Por favor, tente novamente. Se o erro persistir, por favor, entre em contato." );
		});
	});

});
