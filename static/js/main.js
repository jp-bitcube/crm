window.addEventListener('load', function () {
    var inputs = document.querySelectorAll('#field_wrapper');
    if (inputs && inputs.length > 0) {
        inputs.forEach(function (input) {
            var i = input.querySelector('input');
            i.classList.add('form-control')
        });
    }

    $(function () {
        $('form').on('submit', function (e) {
            if ($('#replace') && $('#submit_button')) {
                $('#replace').remove();
                $('#submit_button').append('<div class="loader"></div>')
            }
        });
    })
});

function goBack() {
    window.history.back();
}