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
            {"data": "planilla_caja"},
            {"data": "planilla_cobrador"},
            {"data": "fecha_emision"},
            {"data": "fecha_cierre"},
            {"data": "monto_total"},
            {"data": "estado"},
            {"data": "opciones"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/sgcapp/editPlanilla/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="/sgcapp/deletePlanilla/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
    });
});
