const fastify = require('fastify')();
const path = require('path');
const argon2 = require('argon2');

const { User, Note } = require('./models');
const report = require('./report');

fastify.register(require('fastify-formbody'));

fastify.register(require('fastify-secure-session'), { 
	key: require('crypto').randomBytes(32)
});

fastify.register(require('fastify-csrf'), {
	sessionPlugin: 'fastify-secure-session'
});

fastify.register(require('point-of-view'), {
	engine: {
		ejs: require('ejs')
	},
	root: path.join(__dirname, 'views')
});

fastify.addHook('preHandler', async (req, res) => {
	if (req.session.get('user')) {
		req.user = await User.findOne({ where: { username: req.session.get('user') }, include: ['notes'] });
	}
});

function auth(handler) {
	return (req, res) => {
		if (!req.user) return res.redirect('/');

		return handler(req, res);
	}
}

let userSchema = {
	body: {
		type: 'object',
		properties: {
			username: { type: 'string', maxLength: 30 },
			password: { type: 'string', maxLength: 30 }
		},
		required: ['username', 'password']
	}
};

let reportSchema = {
	body: {
		type: 'object',
		properties: {
			url: { type: 'string', maxLength: 1000 },
		},
		required: ['url']
	}
}

let noteSchema = {
	body: {
		type: 'object',
		properties: {
			title: { type: 'string', maxLength: 30 },
			content: { type: 'string', maxLength: 1000 }
		},
		required: ['title', 'content']
	}
};

let deleteSchema = {
	body: {
		type: 'object',
		properties: {
			id: { type: 'integer' }
		},
		required: ['id']
	}
}

fastify.after(() => {
	fastify.get('/', (req, res) => {
		if (req.user) return res.redirect('/notes');
		return res.view('login');
	});

	fastify.post('/login', { schema: userSchema }, async (req, res) => {
		let { username, password } = req.body;
		username = username.toLowerCase();

		let user = await User.findOne({ where: { username }});
		if (user === null) {
			return res.status(400).send('User not found');
		}

		if (!(await argon2.verify(user.password, password))) {
			return res.status(400).send('Wrong password!');
		}

		req.session.set('user', user.username);

		return res.redirect('/notes');
	});

	fastify.get('/register', (req, res) => {
		return res.view('register');
	});

	fastify.post('/register', { schema: userSchema }, async (req, res) => {
		let { username, password } = req.body;
		username = username.toLowerCase();

		let user = await User.findOne({ where: { username }});
		if (user) {
			return res.status(400).send('User already exists!');
		}

		await User.create({
			username,
			password: await argon2.hash(password)
		});

		req.session.set('user', username);

		return res.redirect('/notes');
	});

	fastify.get('/notes', auth(async (req, res) => {
		return res.view('notes', {
			notes: req.user.notes, 
			csrf: await res.generateCsrf()
		});
	}));

	fastify.get('/new', auth(async (req, res) => {
		return res.view('new', { csrf: await res.generateCsrf() });	
	}));

	fastify.post('/new', {
		schema: noteSchema,
		preHandler: fastify.csrfProtection
	}, auth(async (req, res) => {
		let { title, content } = req.body;

		await Note.create({
			title,
			content,
			userId: req.user.id
		});

		return res.redirect('/notes');
	}));

	fastify.post('/delete', {
		schema: deleteSchema,
		preHandler: fastify.csrfProtection
	}, auth(async (req, res) => {
		let { id } = req.body;

		let deleted = false;

		for (let note of req.user.notes) {
			if (note.id === id) {
				await note.destroy();

				deleted = true;
			}
		}

		if (deleted) {
			return res.redirect('/notes');
		} else {
			res.status(400).send('Note not found!');
		}
	}));

	fastify.get('/report', auth(async (req, res) => {
		return res.view('report', { csrf: await res.generateCsrf() });
	}));

	fastify.post('/report', {
		schema: reportSchema,
		preHandler: fastify.csrfProtection
	}, auth((req, res) => {
		let { url } = req.body;

		if (report.open) {
			return res.send('Only one browser can be open at a time!');
		} else {
			report.run(url);
		}

		return res.send('URL has been reported.');
	}));
}) 

fastify.listen(8080, '0.0.0.0');