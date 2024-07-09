$(document).ready(function () {

    var userIdToDelete = null;

    $('#adminTable').DataTable({
        columnDefs: [
            { width: '10%', targets: 0 },
            { width: '30%', targets: 1 },
            { width: '30%', targets: 2 },
            { width: '15%', targets: 3 },
            { width: '15%', targets: 4 }
        ],
        fixedColumns: true
    });

    $('.btn-edit').click(function () {
        var $row = $(this).closest('tr');
        $row.find('.view-mode').each(function () {
            var $cell = $(this);
            var text = $cell.text().trim();
            if ($cell.index() !== 3) { // Skip is_show column
                $cell.data('original-content', text);
                $cell.html('<input type="text" class="form-control" value="' + text + '">');
            }
        });
        $('.btn-edit, .btn-delete').prop('disabled', true);
        $row.find('.btn-edit').hide();
        $row.find('.edit-mode').show();
        $row.find('.btn-delete').hide();
        $row.find('.btn-show').prop('disabled', false);
    });

    $('.btn-cancel').click(function () {
        var $row = $(this).closest('tr');
        $row.find('.view-mode').each(function () {
            var $cell = $(this);
            if ($cell.index() !== 3) { // Skip is_show column
                $cell.html($cell.data('original-content'));
            }
        });
        $row.find('.edit-mode').hide();
        $row.find('.btn-edit').show();
        $('.btn-edit, .btn-delete').prop('disabled', false).show();
        $row.find('.btn-show').prop('disabled', true); // Disable the show button
    });

    $('.btn-save').click(function () {
        var $row = $(this).closest('tr');
        var id = $row.data('id');
        var username = $row.find('.view-mode:eq(0) input').val();
        var realname = $row.find('.view-mode:eq(1) input').val();

        $.ajax({
            url: '/admin_menu/edit_user',
            type: 'POST',
            data: { id: id, username: username, realname: realname },
            success: function (response) {
                if (response.success) {
                    $row.find('.view-mode:eq(0)').html(username);
                    $row.find('.view-mode:eq(1)').html(realname);
                    $row.find('.edit-mode').hide();
                    // Enable all edit and delete buttons and show them
                    $('.btn-edit, .btn-delete').prop('disabled', false).show();
                    // Disable current row's show button
                    $row.find('.btn-show').prop('disabled', true);
                } else {
                    alert('Failed to update the user.');
                }
            }
        });
    });

    $('.btn-show').click(function () {
        var $button = $(this);
        var $row = $button.closest('tr');
        var id = $row.data('id');
        var is_show = $button.text().trim() === 'Yes' ? 0 : 1;

        $.ajax({
            url: '/admin_menu/toggle_show',
            type: 'POST',
            data: { id: id, is_show: is_show },
            success: function (response) {
                if (response.success) {
                    if (is_show) {
                        $button.removeClass('btn-danger').addClass('btn-success').text('Yes');
                    } else {
                        $button.removeClass('btn-success').addClass('btn-danger').text('No');
                    }
                } else {
                    alert('Failed to update show status.');
                }
            }
        });
    });

    $('.btn-delete').click(function () {
        var $row = $(this).closest('tr');
        var username = $row.find('.username-cell').text().trim();
        userIdToDelete = $row.data('id');

        $('#usernameToDelete').text(username);
        $('#deleteConfirmationModal').modal('show');
    });

    $('#confirmDeleteBtn').click(function () {
        if (userIdToDelete) {
            $.ajax({
                url: '/admin_menu/delete_user',
                type: 'POST',
                data: { id: userIdToDelete },
                success: function (response) {
                    if (response.success) {
                        $('tr[data-id="' + userIdToDelete + '"]').remove();
                        $('#deleteConfirmationModal').modal('hide');
                    } else {
                        alert('Failed to delete the user.');
                    }
                }
            });
        }
    });
});


