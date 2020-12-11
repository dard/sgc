let tblRecibos

$(function () {
    tblRecibos= $('#data').DataTable({
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
            {"data": "recibo_cliente"},
            {"data": "recibo_planilla"},
            {"data": "recibo_caja"},
            {"data": "fecha"},
            {"data": "estado"},
            // {"data": "comprobantes"},
            // {"data": "cheque"},
            {"data": "efectivo"},
            {"data": "subtotalComp"},
            {"data": "subtotalCheq"},
            {"data": "total"},
            {"data": "opciones"},
        ],

        columnDefs: [
            {
                targets: [-2, -3, -4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    // var buttons = '<a rel="details" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
                    var buttons ='<a href="/sgcapp/deleteReciboFactura/' + row.id + '/" type="button" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
        ],
        initComplete: function (settings, json) {
            // alert('Tabla cargada');
        }
    });

        $('#data tbody')
            .on('click', 'a[rel="details"]', function () {
                var tr = tblRecibos.cell($(this).closest('td, li')).index();
                var data = tblRecibos.row(tr.row).data();
                console.log(data);

                $('#tblDet').DataTable({
                    responsive: true,
                    autoWidth: false,
                    destroy: true,
                    deferRender: true,
                    ajax: {
                        url: window.location.pathname,
                        type: 'POST',
                        data: {
                            'action': 'search_details_recibo',
                            'id': data.id
                        },
                        dataSrc: ""
                    },
                    columns: [
                        {"data": "comprobantes"},
                        {"data": "comprobantes.subtotalComp"},
                        {"data": "cheque"},
                        {"data": "cheque.subtotalCheq"},
                    ],
                    columnDefs: [
                        {
                            targets: [-1, -3],
                            class: 'text-center',
                            render: function (data, type, row) {
                                return '$' + parseFloat(data).toFixed(2);
                            }
                        },
                        {
                            targets: [-2],
                            class: 'text-center',
                            render: function (data, type, row) {
                                return data;
                            }
                        },
                    ],
                    initComplete: function (settings, json) {

                    }
                });

                $('#myModelDet').modal('show');
            });
});
