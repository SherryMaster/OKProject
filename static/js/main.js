function FilterList() {
    const input = $('#search-input').val();
    const tableBody = $('#item-table tbody');
    const items = tableBody.find('tr');

    items.each(function() {
        const itemName = $(this).find('td:nth-child(1)').text();
        if (itemName.toLowerCase().indexOf(input.toLowerCase()) > -1) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });
}