function renderCommentBadge(projectSlug, testId, resultIndex, comment){
    if (comment === undefined || comment === null) {
        return $('<a>')
            .attr('class', 'btn btn-outline-dark dtf-btn-xs me-1')
            .attr('title', `${projectSlug}/tests/${testId}/${resultIndex}`)
            .attr('onClick', `addComment()`)
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

function addComment(){
    let comment = prompt("Enter comment", " ");
    prompt("Geschafft", comment);
}