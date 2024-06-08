document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('searchInput').addEventListener('keyup', function() {
        let filter = this.value.toLowerCase();
        let rows = document.querySelectorAll('#dataTable tbody tr');

        rows.forEach(row => {
            let cells = row.querySelectorAll('td');
            let match = false;
            cells.forEach(cell => {
                if (cell.textContent.toLowerCase().includes(filter)) {
                    match = true;
                }
            });
            row.style.display = match ? '' : 'none';
        });
    });
});
