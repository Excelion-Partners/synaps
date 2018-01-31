// const express = require('express');
// const http = require('http');
// var io = require('socket.io')(http);

// const app = express()
var uuid = process.env.RESIN_DEVICE_UUID != null ? process.env.RESIN_DEVICE_UUID : 'local';
var device_name = process.env.RESIN_DEVICE_NAME_AT_INIT != null ? process.env.RESIN_DEVICE_NAME_AT_INIT : 'local';

// app.all('*', function (req, res, next) {
//     res.header('Access-Control-Allow-Origin', '*')
//     res.header('Access-Control-Allow-Headers', 'X-Requested-With')
//     next()
// })

// var server = http.createServer(app)
// var port = 3001 // app.get('port')
// server.listen(port, function () {
//     console.log('SOCKETIO server listening on port ' + port)
// });

// var io = require('socket.io')(server)

const server = require('http').createServer();
const io = require('socket.io')(3001, {
    path: '/socket.io'
});

// var _socket;
console.log('starting socket')
io.on('connection', function (socket) {
    // _socket = socket;

    console.log('connection')

    socket.emit('config', {
        device_id: uuid,
        customer_id: process.env.CUSTOMER_ID != null ? process.env.CUSTOMER_ID : 1,
        flip: process.env.FLIP != null ? process.env.FLIP : false,
    });

    socket.on('frame', function (frame) {
        socket.broadcast.emit('frame', frame);
        //  console.log('new frame')
    });
})

//module.exports = app