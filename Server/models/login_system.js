db_query('CREATE TABLE IF NOT EXISTS users (username VARCHAR(?) NOT NULL, password VARCHAR(?) NOT NULL, session_id VARCHAR(?) NOT NULL, profession VARCHAR(?) NOT NULL)', [max_username_length, max_password_length, max_session_id_length, max_profession_length]).then((results) => {
	console.log('Created table if not exists users.');
}).catch((error) => {
	console.log(error);
	process.exit();
});
