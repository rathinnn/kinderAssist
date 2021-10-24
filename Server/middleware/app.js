module.exports = async (request, response, next) => {
	if (request.cookies.username && request.cookies.session_id) {
		if (request.cookies.session_id != 'nill') {
			const results = await db_query('SELECT * FROM users WHERE username = ? AND session_id = ?', [request.cookies.username, request.cookies.session_id]);
			if (results.length == 1) {
				next();
			} else {
				response.clearCookie('username');
				response.clearCookie('session_id');
				response.sendStatus(401);
			}
		} else {
			response.clearCookie('username');
			response.clearCookie('session_id');
			response.sendStatus(401);
		}
	} else {
		response.clearCookie('username');
		response.clearCookie('session_id');
		response.sendStatus(401);
	}
}
