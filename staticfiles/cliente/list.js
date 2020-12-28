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
            {"data": "nombre"},
            {"data": "apellido"},
            {"data": "dni"},
            {"data": "telefono"},
            {"data": "email"},
            {"data": "direccion"},
            {"data": "opciones"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    // {% url 'SGCapp:ClienteUpdateView' c.id %}
                    var buttons = '<a href="/sgcapp/edit/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/sgcapp/delete/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        // initComplete: function (settings, json) {
        //     alert('Tabla cargada');
        // }
    });
});
