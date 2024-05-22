document.getElementById('submitBtn').addEventListener('click', function() {
    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/compare', true);
    xhr.setRequestHeader('X-CSRFToken', '{{ csrf_token }}');
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);
            var product1_name = document.querySelector('.l-pc-name.product1');
            var product2_name = document.querySelector('.l-pc-name.product2');
            var test = document.querySelector('.test');
            
            test.innerHTML = response.test_string;
            product1_name.innerHTML = response.product1;
            product2_name.innerHTML = response.product2;

        }
    };
    xhr.send(JSON.stringify({}));
});