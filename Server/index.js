require('dotenv').config();

const express = require('express');
global.path = require('path');
const cp = require('cookie-parser');
const bp = require('body-parser');
const favicon = require('serve-favicon');
const http = require('http');
global.mysql = require('mysql2');
const compression = require('compression');

const app = express();
const express_server = http.createServer(app);

global.io = require('socket.io')(express_server);

io.use(require('./middleware/socket-io/authenticator.js'));
io.on('connection', require('./controllers/socket-io/socket.js'));

app.disable('x-powered-by');

app.use(favicon(path.join(__dirname, 'public', 'favicon.ico')));

app.use(compression({
	filter: (request, response) => {
		if (request.headers['x-no-compresssion']) {
			return false;
		} else {
			return compression.filter(request, response);
		}
	},
	level: 1
}));

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.use(bp.urlencoded({
	extended : true
}));

app.use(bp.json());

app.use(cp());

app.use('/', express.static(path.join(__dirname, 'public')));

global.__basedir = __dirname;
global.__tempdir = path.join(__dirname, 'temp');
global.max_username_length = 50;
global.max_password_length = 50;
global.max_session_id_length = 50;
global.session_id_length = 20;
global.max_profession_length = 50;
global.profession_roles = ['student', 'teacher'];
global.delay_request = 2000;

require('./config/database.js');
require('./models/login_system.js');

app.use('/', require('./routes/root.js'));

app.all('*', (request, response) => {
	response.sendStatus(404);
});

express_server.listen(process.env.port_number, (error) => {
	if (error) {
		console.log('Port', process.env.port_number.toString(), 'not idle!');
		process.exit();
	} else {
		console.log('Listening at port:', process.env.port_number.toString());
	}
});

process.on('SIGINT', () => {
	console.log();
	console.log('SIGINT signal received. Closing the server.');
	express_server.close(() => {
		console.log("Server Closed");
		db_pool.end((error) => {
			if (error) {
				console.log(error);
				process.exit();
			} else {
				console.log('Closed connection to mysql.');
				process.exit();
			}
		});
	});
});
