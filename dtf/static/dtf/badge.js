
function renderStatusBadge(status) {
    const statusToBadgeClass = {
        successful: "text-success border-success",
        unstable:   "text-warning border-warning",
        failed:     "text-danger border-danger",
        broken:     "text-danger border-danger",
        unknown:    "text-secondary border-secondary",
        skip:       "text-info border-info"
    }
    const statusToIconClass = {
        successful: "bi-check-circle-fill",
        unstable:   "bi-exclamation-circle-fill",
        failed:     "bi-x-circle-fill",
        broken:     "bi-dash-circle-fill",
        unknown:    "bi-question-circle-fill",
        skip:       "bi-slash-circle-fill"
    }

    let badgeClass = statusToBadgeClass[status];
    if(badgeClass === undefined) {
        badgeClass = statusToBadgeClass.unknown;
    }

    let iconClass = statusToIconClass[status];
    if(iconClass === undefined) {
        iconClass = statusToIconClass.unknown;
    }

    return $('<span>')
        .attr('class', `badge border ${badgeClass}`)
        .append($('<i>')
            .attr('class', `me-1 bi ${iconClass}`)
        )
        .append($('<span>')
            .attr('class', 'status-filter')
            .append(`${status}`)
        )
}