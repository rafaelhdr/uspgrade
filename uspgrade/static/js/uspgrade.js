$(document).ready(function(){

	/*
	 * Responder
	 */

	$("#ajax_submit_resposta").submit(function(){
		var data = $(this).serialize();
		var form = this;
		$.post("/api/responder", data)
		.done(function(response) {
			alert(response.message);
			if (response.result == 'success')
				location.reload();
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
