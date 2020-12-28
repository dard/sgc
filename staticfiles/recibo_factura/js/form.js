
// ----------------------------------
let tblComprobantes;
let tblCheques;
var detComprobante = {
    items:{
        fecha:'',
        recibo_cliente:'',
        recibo_planilla:'',
        recibo_caja:'',
        estado:'',
        efectivo: 0.00,
        subtotalComp: 0.00,
        total: 0.00,
        comprobantes:[]
    },
    calculate_invoice: function () {
        var subtotalComp = 0.00;

        var efectivo = $('input[name="efectivo"]').val();
        $.each(this.items.comprobantes, function (pos, dict) {
            // console.log(pos)
            // console.log(dict)
            dict.subtotalComp = parseFloat(dict.monto);
            subtotalComp+=dict.subtotalComp;
        });
        this.items.subtotalComp = parseFloat(subtotalComp);
        this.items.efectivo = parseFloat(efectivo);
        this.items.total = this.items.subtotalComp + this.items.efectivo + detCheques.items.subtotalCheq;

        $('input[name="subtotalComp"]').val(this.items.subtotalComp.toFixed(2));
        $('input[name="efectivo"]').val(this.items.efectivo.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function(item){
        this.items.comprobantes.push(item);
        this.list();
    },

    list: function () {
        this.calculate_invoice();

        tblComprobantes = $('#tblComprobantes').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.comprobantes,
            columns: [
                {"data": "id"},// Boton Eliminar
                {"data": "comprobante_cliente"},
                {"data": "fecha_comprobante"},
                // {"data": "monto"},
                // {"data": "cant"},
                {"data": "subtotalComp"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style=color:white;><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
    },
};
// detCheques

var detCheques = {
    items:{
        fecha:'',
        recibo_cliente:'',
        recibo_planilla:'',
        recibo_caja:'',
        estado:'',
        efectivo: 0.00,
        subtotalCheq: 0.00,
        total:0.00,
        cheques:[]
    },

    calculate_invoice: function () {
        var subtotalCheq = 0.00;

        var efectivo = $('input[name="efectivo"]').val();
        $.each(this.items.cheques, function (pos, dict) {
            console.log(pos)
            console.log(dict)
            dict.subtotalCheq = dict.cant * parseFloat(dict.monto);
            subtotalCheq+=dict.subtotalCheq;
        });
        this.items.subtotalCheq = parseFloat(subtotalCheq) ;
        this.items.efectivo = parseFloat(efectivo) ;
        this.items.total = this.items.subtotalCheq + this.items.efectivo + detComprobante.items.subtotalComp;

        $('input[name="subtotalCheq"]').val(this.items.subtotalCheq.toFixed(2));
        $('input[name="efectivo"]').val(this.items.efectivo.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },

    add: function(item){
        this.items.cheques.push(item);
        this.list();
    },

    list: function () {
        this.calculate_invoice();

        tblCheques = $('#tblCheques').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.cheques,
            columns: [
                {"data": "id"},// Boton Eliminar
                {"data": "cheque_banco.nombre"},
                {"data": "fecha"},
                // {"data": "monto"},
                // {"data": "cant"},
                {"data": "subtotalCheq"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat" style=color:white; ><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
    },
};

//main
$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    $('#fecha').datetimepicker({
        format:'YYYY-MM-DD',
        date: moment().format('YYYY-MM-DD'),
        locale: 'es',
        //maxDate: moment().format("YYYY-MM-DD")
        //minDate: moment().format("YYYY-MM-DD")
    });

    $("input[name='efectivo']").TouchSpin({
        min: 0,
        max: 10000,
        step: 0.1,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        postfix: '$'
    }).on('change', function () {
        detComprobante.calculate_invoice();
    })
    .val(0);

    // busqueda de comprobante
    $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_comprobantes',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            //console.log(ui.item);
            event.preventDefault();
            console.clear();
            ui.item.cant = 1;
            // ui.item.monto = 0.00;

            console.log(detComprobante.items);

            detComprobante.add(ui.item);
            detComprobante.list();

            $(this).val('');

        }
    });
    // eliminar todos los comprobantes
    $('.btnRemoveAll').on('click', function () {
        if (detComprobante.items.comprobantes.length === 0) return false;
        // alert_action('Notificación', '¿Estas seguro de eliminar todos los comprobantes de tu detalle?', function () {
            detComprobante.items.comprobantes = [];
            detComprobante.list();
        // });
    });
    //eliminar fila de comprobante
    $('#tblComprobantes tbody')
        .on('click', 'a[rel="remove"]', function () {
            // alert('X')
            var tr = tblComprobantes.cell($(this).closest('td, li')).index();
            // alert_action('Notificación', '¿Estas seguro de eliminar el comprobante de tu detalle?', function () {
                detComprobante.items.comprobantes.splice(tr.row, 1);
                detComprobante.list();
            // });
        });
        // eliminar todos los Cheques
        $('.btnRemoveAllCheq').on('click', function () {
            if (detCheques.items.cheques.length === 0) return false;
            // alert_action('Notificación', '¿Estas seguro de eliminar todos los cheques de tu detalle?', function () {
                detCheques.items.cheques = [];
                detCheques.list();
            // });
        });
        //eliminar fila de Cheques
        $('#tblCheques tbody')
            .on('click', 'a[rel="remove"]', function () {
                // alert('X')
                var tr = tblCheques.cell($(this).closest('td, li')).index();
                // alert_action('Notificación', '¿Estas seguro de eliminar el cheques de tu detalle?', function () {
                    detCheques.items.cheques.splice(tr.row, 1);
                    detCheques.list();
                // });
            })
    // ------------------------------------
    // busqueda de cheque
    $('#search_cheq').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_cheques',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            //console.log(ui.item);
            event.preventDefault();
            console.clear();
            console.log(ui.item);
            ui.item.cant = 1;
            // ui.item.monto = 0.00;

            console.log(detCheques.items);

            detCheques.add(ui.item);
            detCheques.list();

            $(this).val('');
        }
    });
    // limpiar caja de busqueda de comprobantes
    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    });
    // limpiar caja de busqueda de cheques
    $('.btnClearSearchCheq').on('click', function () {
        $('input[name="search_cheq"]').val('').focus();
    });
    // evento submit boton guardar
    $('form').on('submit', function (e) {
        // alert('x');
        e.preventDefault();

        if(detComprobante.items.comprobantes.length === 0 && detCheques.items.cheques.length === 0){
            message_error('Debe ingresar datos antes de Guardar');
            return false;
        }

        detComprobante.items.fecha = $('input[name="fecha"]').val();
        detComprobante.items.recibo_cliente = $('select[name="recibo_cliente"]').val();
        detComprobante.items.recibo_planilla = $('select[name="recibo_planilla"]').val();
        detComprobante.items.recibo_caja = $('select[name="recibo_caja"]').val();
        detComprobante.items.estado = $('select[name="estado"]').val();

        detCheques.items.fecha = $('input[name="fecha"]').val();
        detCheques.items.recibo_cliente = $('select[name="recibo_cliente"]').val();
        detCheques.items.recibo_planilla = $('select[name="recibo_planilla"]').val();
        detCheques.items.recibo_caja = $('select[name="recibo_caja"]').val();
        detCheques.items.estado = $('select[name="estado"]').val();


        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('detComprobante', JSON.stringify(detComprobante.items));
        parameters.append('detCheques', JSON.stringify(detCheques.items));

        submit_with_ajax_recibo(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            console.log();
            location.href = '/sgcapp/listReciboFactura/';
        });
    });

    detComprobante.list();
// main end
});
