const controllers = {};

controllers.get_user_home = async (request, response) => {
	response.render('test.ejs');
}

controllers.socket_token = async (request, response) => {
	if (request.cookies.username && request.cookies.session_id) {
		const results = await db_query('SELECT * FROM users WHERE username = ? AND session_id = ?', [request.cookies.username, request.cookies.session_id]);
		response.json({
			username: request.cookies.username,
			session_id: request.cookies.session_id,
			profession: results[0].profession
		});
	}
}

controllers.logout = async (request, response) => {
	if (request.cookies.username && request.cookies.session_id) {
		const results = await db_query('SELECT * FROM users WHERE username = ? AND session_id = ?', [request.cookies.username, request.cookies.session_id]);
		if (results.length == 1) {
			await db_query('UPDATE users SET session_id = ? WHERE username = ?', ['null', request.cookies.username]);
			response.clearCookie('username');
			response.clearCookie('session_id');
			response.redirect('/');
		} else {
			response.sendStatus(401);
		}
	} else {
		response.sendStatus(400);
	}
}

module.exports = controllers;
