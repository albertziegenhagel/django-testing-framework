function renderCommentBadge(comment){
    if (comment === undefined || comment === null || comment === "") {
        return 
    }
    else {
        return $('<span>')
            .attr('class', 'bi bi-chat')
            .attr('title',`${comment}`)
    }
}

function updateResultsTableComments(result) {
    let resultsRows = $('#resultsTable > tbody > tr');

    resultsRows.each(function(index, tr) {
        const testResultIndex = tr.getAttribute('test-result-index');

        let CommentsData = $(tr).find('#tableDataComments').first();
        let StatusData = $(tr).find('#tableDataStatus').first();

        CommentsData.empty();
        CommentsData.append(renderCommentBadge(result["results"][testResultIndex]["comment"]));

        StatusData.empty();
        StatusData.append(renderStatusBadge(result["results"][testResultIndex]["status"]));
    });
}

function updateComments(result,csrfToken, projectSlug, testId, comment){
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
            $.toast({
                type: 'success',
                content: `Successfully updated comment(s).`
            });
            updateResultsTableComments(result);
            uncheckAllBoxes();
        },
        error: function (result) {
            $.toast({
                type: 'danger',
                content: `Failed to update comment(s).`
            });
            console.log(result);
        }
    }); 
}
