var markone = {}
markone['main'] = function(){
    var host='localhost:5000'
    var socket = io.connect(host);
    socket.on('connect', function() {
        console.log('connected to ' + host)
        socket.on('messages', function (data) {
            console.log('data:', data);
        })
    });
}

window.onload = markone.main
