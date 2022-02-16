function renderCommentBadge(comment){
    if (comment === undefined || comment === null || comment === "") {
        return $('<a>')
            .attr('class', 'btn btn-outline-dark dtf-btn-xs me-1')
            .attr('title', ``)
            .append($('<i>')
                .attr('class', 'bi bi-chat')
            )
    }
    else {
        return $('<a>')
            .attr('class', 'btn btn-dark dtf-btn-xs me-1')
            .attr('title',`${comment}`)
            .append($('<i>')
                .attr('class', 'bi bi-chat')
            )
    }
}

function updateResultsTableComments(result) {
    let resultsRows = $('#resultsTable > tbody > tr');

    resultsRows.each(function(index, tr) {
        const testResultIndex = tr.getAttribute('test-result-index');

        let CommentsData = $(tr).find('#tableDataComments').first();

        CommentsData.empty();
        CommentsData.append(renderCommentBadge(result["results"][testResultIndex]["comment"]));
    });
}

function addComments(result,csrfToken, projectSlug, testId, comment){
    let resultsRows = $('#resultsTable > tbody > tr');

    resultsRows.each(function(index, tr) {
        let checkBox = $(tr).find('#updateCheckbox')[0];
        if(checkBox.checked) {
            const testResultIndex = tr.getAttribute('test-result-index');
            result["results"][testResultIndex]["comment"] = comment;
        }
    });

    $.ajax({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        type: 'PUT',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(result),
        url: `/api/projects/${projectSlug}/tests/${testId}`,
        success: function (result) {
            updateResultsTableComments(result);
            uncheckAllBoxes();
        },
        error: function (result) {
            console.log(result);
        }
    }); 
}

function updateComments(csrfToken, testId, projectSlug) {
    let input = prompt(`Enter comments for ${projectSlug}/tests/${testId}`, "");

    $.ajax({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        type: 'GET',
        contentType: "application/json; charset=utf-8",
        url: `/api/projects/${projectSlug}/tests/${testId}`,
        success: function (result) {
            addComments(result,csrfToken, projectSlug, testId, input)
        },
        error: function (result) {
            console.log(result);
        }
    });

}