function renderCommentBadge(csrfToken, projectSlug, testId, resultIndex, comment){
    if (comment === undefined || comment === null) {
        return $('<a>')
            .attr('class', 'btn btn-outline-dark dtf-btn-xs me-1')
            .attr('title', ``)
            .attr('onClick', 'addComment(\'' + csrfToken + '\',\''+projectSlug+'\','+testId+','+resultIndex+',"")')
            .append($('<i>')
                .attr('class', 'bi bi-chat')
            )
    }
    else {
        return $('<a>')
            .attr('class', 'btn btn-dark dtf-btn-xs me-1')
            .attr('title',`${comment}`)
            .attr('onClick', 'addComment(\'' + csrfToken + '\',\''+projectSlug+'\','+testId+','+resultIndex+',\''+comment+'\')')
            .append($('<i>')
                .attr('class', 'bi bi-chat')
            )
    }
}

function addComment(csrfToken, projectSlug, testId, resultIndex, comment){
    let input = prompt(`Enter comment for ${projectSlug}/tests/${testId}/${resultIndex}`, comment);
    
    $.ajax({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        type: 'GET',
        contentType: "application/json; charset=utf-8",
        url: `/api/projects/${projectSlug}/tests/${testId}`,
        success: function (result) {
            updateComment(result,csrfToken, projectSlug, testId, resultIndex, input)
        },
        error: function (result) {
            console.log(result);
        }
    });
}

function updateComment(result,csrfToken, projectSlug, testId, resultIndex, comment){
    result["results"][`${resultIndex}`]["comment"] = comment;
    $.ajax({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        type: 'PUT',
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(result),
        url: `/api/projects/${projectSlug}/tests/${testId}`,
        success: function (result) {
            //update website
        },
        error: function (result) {
            console.log(result);
        }
    }); 
}

function updateComments(csrfToken, testName, testId, projectSlug) {
    let input = prompt(`Enter comments for ${projectSlug}/tests/${testId}/${testName}`, "");
}