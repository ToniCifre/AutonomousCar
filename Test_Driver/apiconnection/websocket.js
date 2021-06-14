const express = require('express');

var server = require('http').Server(express);
var io = require('socket.io')(server);
global.cotxes = {};

server.listen(3003, function() {
    console.log('WebSocket corriendo en http://localhost:3003');
});


io.on('connection', function(socket) {
    console.log('Un cliente se ha conectado');
    socket.emit('message', "Benvingut al WebSocket");

    // missatge inicial on el cotche et comunica el seu id
    socket.on('id', (id) => {
        console.log('id del cotche: ' + id);
        socket.id = id;
        cotxes[id] = socket;
    });

    // missage que reps del posicionament individual de cada cotche
    socket.on('position', (lat,lon) => {
        console.log('position del cotxe '+socket.id+': ' + lat + " - " + lon);
    });

    // missage que reps del status individual de cada cotche
    socket.on('status', (msg) => {
        const status = Number(msg);
        if (status <= 3 && status >= 0 ) {
            console.log('status del cotxe '+socket.id+': ' + status);
        }else {
            console.log('Bad status');
            socket.emit('bad_status', "El status no es correcte");
        }
    });

    socket.on('notification', (msg) => {
        if (msg === 'llest' || msg === 'anant' || msg === 'error') {
            console.log('notificacio del cotxe '+socket.id+': ' + msg);
        }else {
            console.log('Bad notify');
            socket.emit('bad_notify', "La notificació no es correcte");
        }
    });
    // quan un cotxe es desconnecta s'elimina de la llista
    socket.on('disconnect', (reason) => {
        console.log('Cotxe '+socket.id+' desconnectat');
        delete cotxes[socket.id]
    });

});


// cotxes["12341"].emit('message', "Benvingut al WebSocket"); // ejemplo de mensaje normal, no sirve para nada
// cotxes["12341"].emit('notification', "Id_aturada_inicial:Id_aturada_final"); // ejemplo de notidicación a un solo coche
