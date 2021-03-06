
function resetForm(form_id) {
    let form = $(form_id).first();
    form[0].reset();
    form.find('input,select').each(function () {
        let field = $(this)
        field.removeClass("is-invalid");
        field.removeClass("is-valid");
    });
    let alert = $(form_id).find("div[role='alert']")
    alert.attr("hidden", true);
    alert.text("");
}

function fillForm(form_id, data) {
    $(form_id).find('input,select').each(function () {
        let field = $(this)
        if (this.name in data) {
            const value = data[this.name];
            if (this.type == 'checkbox') {
                field.prop('checked', value);
            }
            else {
                if((typeof value === 'object') && ('id' in value) && field.attr('id').startsWith('id_')) {
                    field.val(value['id']);
                }
                else {
                    field.val(value);
                }
            }
        }
    })
}

function fillFormErrors(form_id, errors) {
    if ("__all__" in errors) {
        let alert = $(form_id).find("div[role='alert']");
        alert.removeAttr("hidden");
        alert.text("");
        errors["__all__"].forEach(function (element) {
            if($.trim(alert.text())) {
                alert.append('<br>');
            }
            alert.append(element['message']);
        });
    }
    $(form_id).find('input,select').each(function () {
        let field = $(this)
        if (this.name in errors) {
            field.removeClass("is-valid");
            field.addClass("is-invalid");
            let fieldErrors = errors[this.name]
            let immediateSibling = field.next();
            if (immediateSibling.hasClass('invalid-feedback')) {
                immediateSibling.text(fieldErrors[0]['message']);
            }
        }
        else {
            field.removeClass("is-invalid");
            field.addClass("is-valid");
            let immediateSibling = field.next();
            if (immediateSibling.hasClass('invalid-feedback')) {
                immediateSibling.text("");
            }
        }
    });
}

function deleteInstance(base_url, instance_id, id_prefix, csrf_token) {
    let url = base_url + instance_id
    $.ajax({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        type: 'DELETE',
        url: url,
        success: function (data) {
            let element = $(id_prefix + instance_id)
            element.fadeOut('fast', function () {
                element[0].remove();
            })
        },
        error: function () {
            alert("Error!")
        }
    })
}

function startEditInstance(base_url, instance_id, id_prefix, csrf_token) {
    let url = base_url + instance_id
    $.ajax({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        type: 'GET',
        url: url,
        success: function (data) {
            let form_id = id_prefix + 'form_id';
            let form = $(form_id).first();
            resetForm(form_id);
            fillForm(form_id, data);
            form.find(":submit[name='edit']").removeAttr("hidden");
            form.find(":submit[name='add']").attr("hidden", true);
            $(id_prefix + 'edit_cancel').removeAttr("hidden");
        },
        error: function () {
            alert("Error!")
        }
    })
}

function cancelEditInstance(id_prefix) {
    let form_id = id_prefix + 'form_id';
    let form = $(form_id).first();
    resetForm(form_id);
    form.find(":submit[name='add']").removeAttr("hidden");
    form.find(":submit[name='edit']").attr("hidden", true);
    $(id_prefix + 'edit_cancel').attr("hidden", true);
}

function submitForm(url, id_prefix, scope, action, csrf_token, successCallback) {
    let form_id = id_prefix + 'form_id';
    let form = $(form_id).first()

    let data = form.serializeArray().reduce(function(obj, item) {
        obj[item.name] = item.value;
        return obj;
    }, {});
    $(':disabled[name]', form).each(function () {
        data[this.name] = $(this).val();
    });
    data['scope'] = scope
    data['action'] = action

    $.ajax({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        },
        type: 'POST',
        url: url,
        data: data,
        success: function (data) {
            if (data["result"] == "valid") {
                successCallback(data[scope]);
            }
            if (data["result"] == "invalid") {
                fillFormErrors(form_id, data["errors"])
            }
        },
        error: function () {
            alert("Error!")
        }
    })
}