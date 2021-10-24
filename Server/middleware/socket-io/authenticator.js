module.exports = async (socket, next) => {
	const credentials = socket.handshake.auth;
	if (credentials.username && credentials.session_id && credentials.profession) {
		const results = await db_query('SELECT * FROM users WHERE username = ? AND session_id = ?', [credentials.username, credentials.session_id]);
		if (results.length == 1) {
			console.log(credentials.username, credentials.profession, 'has joined.');
			socket.data = credentials;
			next();
		} else {
			const error = new Error('Not authorized');
			next(error);
		}
	} else {
		const error = new Error('Not authorized');
		next(error);
	}
}
