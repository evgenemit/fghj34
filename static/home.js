$('form').submit(function (e) {
    e.preventDefault()

    let form_data = new FormData()
    let file = $('input[type=file]')[0].files[0]
    form_data.append('file', file)

    $.ajax({
        url: '/ajax/upload-file/',
        type: 'POST',
        data: form_data,
        processData: false,
        contentType: false,
        headers: {
            'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function (response) {
            console.log(response)
            if (response.status === 'ok') {
                $('#result').text('Файл загружен.').addClass('success').removeClass('error').fadeIn(200)
            } else {
                $('#result').text(response.message).addClass('error').removeClass('success').fadeIn(200)
                $('input[type=file]').addClass('error')
            }
        }
    })
})

$('form').click(function () {
    $('#result').fadeOut(200)
    $('input[type=file]').removeClass('success').removeClass('error')
})
