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
            {"data": "comprobante_cliente"},
            {"data": "fecha_comprobante"},
            {"data": "monto"},
            // {"data": "monto_cancelado"},
            {"data": "opciones"},
        ],

        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    // {% url 'SGCapp:ClienteUpdateView' c.id %}
                    var buttons = '<a href="/sgcapp/editcomprobante/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/sgcapp/deletecomprobante/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        // initComplete: function (settings, json) {
        //     alert('Tabla cargada');
        // }
    });
});
