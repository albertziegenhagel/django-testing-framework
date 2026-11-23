function disableAbsentStatusFilters(rows, checkboxes) {
    const presentStatuses = new Set();

    Array.from(rows).forEach(function(row) {
        const statusBadge = row.getElementsByClassName('status-filter')[0];
        if(statusBadge) {
            presentStatuses.add(statusBadge.textContent.trim());
        }
    });

    Array.from(checkboxes).forEach(function(checkbox) {
        checkbox.disabled = !presentStatuses.has(checkbox.value);
    });
}
