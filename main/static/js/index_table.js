$(document).ready(function () {
    $('#indexTable').DataTable({
        "pageLength": 50,

        columnDefs: [
            { width: '5%', targets: 0 },
            { width: '15%', targets: 1 },
            { width: '30%', targets: 2 },
            { width: '10%', targets: 3 },
            { width: '15%', targets: 4 },
            { width: '10%', targets: 5 },
            { width: '15%', targets: 6 }
        ],
        fixedColumns: true
    });
});
