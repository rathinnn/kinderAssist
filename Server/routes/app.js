const controllers = require('./../controllers/app.js');
const middleware = require('./../middleware/app.js');
const express = require('express');
const router = express.Router();

router.get('/home', middleware, controllers.get_user_home);
router.get('/socket_token', middleware, controllers.socket_token);
router.post('/logout', middleware, controllers.logout);

module.exports = router;
