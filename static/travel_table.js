$(document).ready(function () {
    $('#travelTable').DataTable({
        columnDefs: [
            { width: '80%', targets: 0 },
            { width: '20%', targets: 1 }
        ],
        fixedColumns: true
    });

    $('.btn-edit').click(function () {
        var $row = $(this).closest('tr');
        var name = $row.find('.view-mode').text().trim();
        $row.find('.view-mode').html('<input type="text" class="form-control" value="' + name + '">');
        $('.btn-edit, .btn-delete').prop('disabled', true);
        $row.find('.btn-edit').hide();
        $row.find('.edit-mode').show();
        $row.find('.btn-delete').hide();
        $row.find('.btn-show').show();
    });

    $('.btn-cancel').click(function () {
        var $row = $(this).closest('tr');
        var name = $row.find('input').val();
        $row.find('.view-mode').text(name);
        $row.find('.edit-mode').hide();
        $row.find('.btn-edit').show();
        $row.find('.btn-show').hide();
        $('.btn-edit, .btn-delete').prop('disabled', false).show();
    });

    $('.btn-save').click(function () {
        var $row = $(this).closest('tr');
        var id = $row.data('id');
        var name = $row.find('input').val();

        fetch('/admin_menu/edit_travel', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: id, name: name })
        })
            .then(response => response.json())
            .then(response => {
                if (response.success) {
                    $row.find('.view-mode').text(name);
                    $row.find('.edit-mode').hide();
                    $row.find('.btn-show').hide();
                    $row.find('.btn-edit').show();
                    $('.btn-edit, .btn-delete').prop('disabled', false).show();
                } else {
                    alert('Не удалось обновить запись.');
                }
            });
    });

    $('.btn-delete').click(function () {
        var $row = $(this).closest('tr');
        var id = $row.data('id');

        if (confirm('Вы уверены, что хотите удалить эту запись?')) {
            fetch('/admin_menu/delete_travel', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ id: id })
            })
                .then(response => response.json())
                .then(response => {
                    if (response.success) {
                        $row.remove();
                    } else {
                        alert('Не удалось удалить запись.');
                    }
                });
        }
    });

    $('.btn-show').click(function () {
        var $button = $(this);
        var $row = $button.closest('tr');
        var id = $row.data('id');
        var is_show = $button.text().trim() === 'Yes' ? 0 : 1;

        fetch('/admin_menu/travel_table/toggle_show', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: id, is_show: is_show })
        })
            .then(response => response.json())
            .then(response => {
                if (response.success) {
                    if (is_show) {
                        $button.removeClass('btn-danger').addClass('btn-success').text('Yes');
                    } else {
                        $button.removeClass('btn-success').addClass('btn-danger').text('No');
                    }
                } else {
                    alert('Cant update status');
                }
            });
    });
    $('#btn-add').click(function () {
        var $newRow = $('<tr data-id="new">' +
            '<td class="view-mode"><input type="text" class="form-control" placeholder="New line"></td>' +
            '<td>' +
            '<button class="btn btn-success btn-sm btn-save-new edit-mode"><i class="fas fa-save"></i></button> ' +
            '<button class="btn btn-secondary btn-sm btn-cancel-new edit-mode"><i class="fas fa-cancel"></i></button>' +
            '</td>' +
            '</tr>');

        $('#travelTable tbody').append($newRow);
        $('.btn-edit, .btn-delete').prop('disabled', true);
    });

    $(document).on('click', '.btn-save-new', function () {
        var $row = $(this).closest('tr');
        var name = $row.find('input').val();

        fetch('/admin_menu/add_travel', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: name })
        })
            .then(response => response.json())
            .then(response => {
                if (response.success) {
                    $row.attr('data-id', response.id);
                    $row.find('.view-mode').text(name);
                    $row.find('.edit-mode').hide();
                    $row.find('.btn-edit').show();
                    $('.btn-edit, .btn-delete').prop('disabled', false).show();
                } else {
                    alert('Cant add the row');
                }
            });
    });

    $(document).on('click', '.btn-cancel-new', function () {
        var $row = $(this).closest('tr');
        $row.remove();
        $('.btn-edit, .btn-delete').prop('disabled', false).show();
    });
});

