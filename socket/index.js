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

fb.database().ref('devices/' + uuid).on('value', function (dataSnapshot) {
    _deviceData = dataSnapshot.val();

    if (_deviceData == null)
        _deviceData = {

        };

    _deviceData.name = device_name;

    // console.log('new value: ' + JSON.stringify(dataSnapshot))

    if (_deviceData['session-ct'] == null)
        _deviceData['session-ct'] = 0;
    if (_deviceData['session-len'] == null)
        _deviceData['session-len'] = 0;
    if (_deviceData['male-ct'] == null)
        _deviceData['male-ct'] = 0;
    if (_deviceData['female-ct'] == null)
        _deviceData['female-ct'] = 0;
    if (_deviceData['youth-ct'] == null)
        _deviceData['youth-ct'] = 0;
    if (_deviceData['young-ct'] == null)
        _deviceData['young-ct'] = 0;
    if (_deviceData['adult-ct'] == null)
        _deviceData['adult-ct'] = 0;
    if (_deviceData['senior-ct'] == null)
        _deviceData['senior-ct'] = 0;

});

fb.database().ref('ads').on('value', function (dataSnapshot) {
    var ads = dataSnapshot.val();

    for (var x = 0; x < ads.length; x++) {
        for (var y = 0; y < ads[x].set.length; y++) {
            var nm = ads[x].set[y].image;
            if (nm == null)
                nm = ads[x].set[y].video;

            _adData[_adData.length] = {
                'name': nm,
                'slots': []
            };
        }
    }

    console.log("ADS:" + JSON.stringify(_adData));
});

app.all('*', function (req, res, next) {
    res.header('Access-Control-Allow-Origin', '*')
    res.header('Access-Control-Allow-Headers', 'X-Requested-With')
    next()
})

var server = http.createServer(app)
var port = 3003 // app.get('port')
server.listen(port, function () {
    console.log('SOCKETIO server listening on port ' + port)
})

var io = require('socket.io')(server)
var _socket;
console.log('starting socket')
io.on('connection', function (socket) {
    _socket = socket;
    _socket.on('media-change', function (frame) {
        _socket.broadcast.emit('media-change', frame);

        fb.database().ref('devices/' + uuid).update({
            'frame': frame
        });
    })
    _socket.on('config', function (n, fn) {
        console.log('config-response')
        fn({
            'device-name': device_name,
            'device-id': uuid,
            // 'ad-set-id': adSetId
        });
    })
    _socket.on('frame', function (frame) {
        _socket.broadcast.emit('frame', frame);
    });
    _socket.on('ad-change', function (frame) {
        console.log('ad change')
        var ad = frame;
        for (var x = 0; x < _adData.length; x++) {
            if (_adData[x].name == ad.url) {
                _adData[x].slots[_adData[x].slots.length] = {
                    start: new Date(),
                    views: 0,
                    males: 0,
                    age: 0
                }

                if (_lastAd != -1) {
                    var lastAd = _adData[_lastAd].slots[_adData[_lastAd].slots.length - 1];
                    lastAd.end = new Date();
                    console.log(lastAd.end - lastAd.start)
                }

                _lastAd = x;
                break;
            }
        }
    })
    _socket.on('session', function (frame) {
        console.log('new session! ' + JSON.stringify(frame))
        _deviceData['session-ct']++;
        _deviceData['session-len'] += frame.duration;
        _deviceData['latest-session'] = frame;

        if (frame.gender.toLowerCase() == 'male')
            _deviceData['male-ct']++;
        else
            _deviceData['female-ct']++;

        if (frame.age < 18)
            _deviceData['youth-ct']++;
        else {
            if (frame.age < 28)
                _deviceData['young-ct']++;
            else {
                if (frame.age < 55)
                    _deviceData['adult-ct']++;
                else
                    _deviceData['senior-ct']++;
            }
        }

        var winStart = new Date(frame.started * 1000);
        var winEnd = new Date((frame.started * 1000) + (frame.duration * 1000));

        var adData = [];
        for (var x = 0; x < _adData.length; x++) {
            adData[x] = {
                name: _adData[x].name,
                males: 0,
                age: 0,
                views: 0,
                viewLength: 0
            }
            for (var y = 0; y < _adData[x].slots.length; y++) {
                var slot = _adData[x].slots[y];

                var endedIn = (slot.start < winEnd && slot.end > winEnd) || (slot.start < winEnd && slot.end == null);
                var startedIn = slot.start < winStart && slot.end > winStart;
                var watchedAll = winStart < slot.start && winEnd > slot.end;
                if (endedIn || startedIn || watchedAll) {
                    slot.views++;
                    if (frame.gender.toLowerCase() == 'male') {
                        slot.males++;
                    }
                    slot.age += frame.age;
                }
                adData[x].views += slot.views;
                adData[x].age += slot.age;
                adData[x].males += slot.males;
                adData[x].viewLength += 0; //slot.end - slot.start;
            }
        }

        _deviceData.adData = adData;
        fb.database().ref('devices/' + uuid).set(_deviceData);
    })
})

module.exports = app