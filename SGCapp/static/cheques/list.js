$(function () {
     $('#data').DataTable({
         responsive: true,
         autoWidth: false,
         destroy: true,
         deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },

        columns: [
            {"data": "id"},
            {"data": "cheque_banco"},
            {"data": "fecha"},
            {"data": "monto"},
            {"data": "imagen"},
            {"data": "opciones"},
        ],
        columnDefs: [
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<img src="'+data+'" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                    // return '<img src="'+row.imagen+'" class="img-fluid mx-auto d-block" style="width: 20px; height: 20px;">';
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    // {% url 'SGCapp:ClienteUpdateView' c.id %}
                    var buttons = '<a href="/sgcapp/editcheque/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/sgcapp/deletecheque/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        // initComplete: function (settings, json) {
        //     alert('Tabla cargada');
        // }
    });
});
