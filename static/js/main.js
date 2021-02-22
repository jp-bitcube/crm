window.addEventListener('load', function () {
    var inputs = document.querySelectorAll('#field_wrapper');
    if (inputs && inputs.length > 0) {
        inputs.forEach(function (input) {
            var i = input.querySelector('input');
            i.classList.add('form-control')
        });
    }
});