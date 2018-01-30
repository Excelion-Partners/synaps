const express = require('express');
const http = require('http');
var io = require('socket.io')(http);

const app = express()
var _deviceData;
var _adData = [];
var _lastAd = -1;

var firebase = require('firebase');
var fb = firebase.initializeApp({
    databaseURL: "https://synaps-demo.firebaseio.com/", // Realtime Database
});

//var adSetId = process.env.AD_SET_ID != null ? process.env.AD_SET_ID : 1;
var uuid = process.env.RESIN_DEVICE_UUID != null ? process.env.RESIN_DEVICE_UUID : 'local';
var device_name = process.env.RESIN_DEVICE_NAME_AT_INIT != null ? process.env.RESIN_DEVICE_NAME_AT_INIT : 'local';

// fb.database().ref('devices/' + uuid).on('value', function (dataSnapshot) {
//     _deviceData = dataSnapshot.val();

//     if (_deviceData == null)
//         _deviceData = {

//         };

//     _deviceData.name = device_name;

//     // console.log('new value: ' + JSON.stringify(dataSnapshot))

//     if (_deviceData['session-ct'] == null)
//         _deviceData['session-ct'] = 0;
//     if (_deviceData['session-len'] == null)
//         _deviceData['session-len'] = 0;
//     if (_deviceData['male-ct'] == null)
//         _deviceData['male-ct'] = 0;
//     if (_deviceData['female-ct'] == null)
//         _deviceData['female-ct'] = 0;
//     if (_deviceData['youth-ct'] == null)
//         _deviceData['youth-ct'] = 0;
//     if (_deviceData['young-ct'] == null)
//         _deviceData['young-ct'] = 0;
//     if (_deviceData['adult-ct'] == null)
//         _deviceData['adult-ct'] = 0;
//     if (_deviceData['senior-ct'] == null)
//         _deviceData['senior-ct'] = 0;

// });

// fb.database().ref('ads').on('value', function (dataSnapshot) {
//     var ads = dataSnapshot.val();

//     for (var x = 0; x < ads.length; x++) {
//         for (var y = 0; y < ads[x].set.length; y++) {
//             var nm = ads[x].set[y].image;
//             if (nm == null)
//                 nm = ads[x].set[y].video;

//             _adData[_adData.length] = {
//                 'name': nm,
//                 'slots': []
//             };
//         }
//     }

//     console.log("ADS:" + JSON.stringify(_adData));
// });

app.all('*', function (req, res, next) {
    res.header('Access-Control-Allow-Origin', '*')
    res.header('Access-Control-Allow-Headers', 'X-Requested-With')
    next()
})

var server = http.createServer(app)
var port = 3001 // app.get('port')
server.listen(port, function () {
    console.log('SOCKETIO server listening on port ' + port)
})

var io = require('socket.io')(server)
var _socket;
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

module.exports = app