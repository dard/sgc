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
            {"data": "direccion"},
            {"data": "email"},
            {"data": "telefono"},
            {"data": "id"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: true,
                render: function (data, type, row) {
                    var buttons = '<a href="/sgcapp/editcobrador/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/sgcapp/deletecobrador/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        // initComplete: function (settings, json) {
        //     alert('Tabla cargada');
        // }
    });
});
