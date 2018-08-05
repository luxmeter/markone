var markone = function(){
    var host='localhost:5000'
    var socket = io.connect(host);
    socket.on('connect', function() {
        console.log('connected to ' + host)
        socket.on('update_index', function (data) {
            $('#container').jstree(true).settings.core.data = data;
            $('#container').jstree(true).refresh();
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
            window.open(parent_path+'/'+name, '_self')
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

    makeTablesPrettyAgain = function () {
        document.querySelectorAll('table').forEach(table => table.className = 'table table-striped')
    }
    makeTablesPrettyAgain();
}

window.onload = markone
