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
    $('#container')
    .on('click', '.jstree-anchor', function (e) {
        $(this).jstree(true).toggle_node(e.target);
        node = $(this).jstree(true).get_node(e.target)
        name = node.original.text
        type = node.original.node_type
        if (type === 'leaf') {
            parent_path = node.parents.map(n => $(this).jstree(true).get_node(n).text).reverse().join('/')
            window.open('/watch'+parent_path+'/'+name, '_self')
        }
    })
    .jstree({
        'plugins': [ 'changed' ],
        'core' : {
            'data' : function (obj, callback) {
                var self = this
                $.getJSON('/tree', function(data, status) {
                    if (status === 'success') {
                        console.log(data)
                        callback.call(self, data);
                    }
                })
            }
        }
    });
}

window.onload = markone.main
