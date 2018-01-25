const project = require('../config/project.config')
const server = require('../server/main')
const debug = require('debug')('app:bin:dev-server')

server.listen(project.server_port)

if (project.env === 'cloud9') {
	debug(`Server is now running at http://boilerplate-cloud-jansselt.c9users.io`)
} else {
	debug(`Server is now running at http://localhost:${project.server_port}`)
}
