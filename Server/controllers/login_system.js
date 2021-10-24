const helpers = require('./../helpers/functions.js');
const controllers = {};

controllers.get_home = async (request, response) => {
	response.render('homepage.ejs');
}

controllers.get_login = async (request, response) => {
	response.render('loginpage.ejs', {
		max_username_length: max_username_length,
		max_password_length: max_password_length,
		error: false
	});
}

controllers.get_signup = async (request, response) => {
	response.render('signuppage.ejs', {
		max_username_length: max_username_length,
		max_password_length: max_password_length,
		profession_roles: profession_roles,
		error: 0
	});
}

controllers.login = async (request, response) => {
	if (request.body.username && request.body.password) {
		const results = await db_query('SELECT * FROM users WHERE username = ? and password = ?', [request.body.username, request.body.password]);
		if (results.length == 1) {
			const temp = helpers.random_string_generator(session_id_length);
			response.cookie('username', request.body.username, {
				httpOnly: true,
				sameSite: true
			});
			response.cookie('session_id', temp, {
				httpOnly: true,
				sameSite: true
			});
			await db_query('UPDATE users SET session_id = ? WHERE username = ?', [temp, request.body.username]);
			response.redirect('/home');
		} else {
			response.render('loginpage.ejs', {
				max_username_length: max_username_length,
				max_password_length: max_password_length,
				profession_roles: profession_roles,
				error: true
			});
		}
	} else {
		response.sendStatus(400);
	}
}

controllers.signup = async (request, response) => {
	if (request.body.username && request.body.password && request.body.check_password && request.body.profession) {
		if (request.body.username.length < max_username_length && request.body.password.length < max_password_length && request.body.profession.length < max_profession_length) {
			if (profession_roles.includes(request.body.profession)) {
				const results = await db_query('SELECT * FROM users WHERE username = ?', [request.body.username]);
				if (results.length == 1) {
					response.render('signuppage.ejs', {
						max_username_length: max_username_length,
						max_password_length: max_password_length,
						profession_roles: profession_roles,
						error: 1
					});
				} else {
					await db_query('INSERT INTO users (username, password, session_id, profession) VALUES (?, ?, ?, ?)', [request.body.username, request.body.password, 'null', request.body.profession]);
					response.redirect('/login');
				}
			} else {
				response.sendStatus(401);
			}
		} else {
			response.sendStatus(401);
		}
	} else {
		response.sendStatus(400);
	}
}

module.exports = controllers;
