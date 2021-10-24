module.exports = async (request, response, next) => {
	if (request.cookies.username && request.cookies.session_id) {
		if (request.cookies.session_id != 'null') {
			const results = await db_query('SELECT * FROM users WHERE username = ? AND session_id = ?', [request.cookies.username, request.cookies.session_id]);
			if (results.length == 1) {
				response.redirect('/home');
			} else {
				response.clearCookie('username');
				response.clearCookie('session_id');
				next();
			}
		} else {
			response.clearCookie('username');
			response.clearCookie('session_id');
			next();
		}
	} else {
		response.clearCookie('username');
		response.clearCookie('session_id');
		next();
	}
}
