module.exports = (socket) => {
	if (socket.data.profession == 'teacher') {
		socket.join('teacher');
	} else if (socket.data.profession == 'student') {
		socket.join('student');
	}
	if (socket.data.profession == 'teacher') {
		socket.on('update_option', (message) => {
			console.log('update_option', socket.data.username, message);
			io.to('student').emit('update_option', message);
		});
	} else if (socket.data.profession == 'student') {
		socket.on('wrong_counting', (message) => {
			console.log('wrong_counting', socket.data.username);
			io.to('teacher').emit('wrong_counting', {
				name: socket.data.username
			});
		});
		socket.on('distracted', (message) => {
			console.log('distracted', socket.data.username);
			io.to('teacher').emit('distracted', {
				name: socket.data.username
			});
		});
		socket.on('absent', (message) => {
			console.log('absent', socket.data.username);
			io.to('teacher').emit('absent', {
				name: socket.data.username
			});
		});
	}
}
