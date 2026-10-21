document.addEventListener('DOMContentLoaded', function () {
    var list = document.getElementById('menu-list');
    if (!list) {
        return;
    }

    fetch('/api/menu-items/', { headers: { 'Accept': 'application/json' } })
        .then(function (response) {
            if (!response.ok) {
                throw new Error('HTTP ' + response.status);
            }
            return response.json();
        })
        .then(function (items) {
            list.innerHTML = '';
            if (items.length === 0) {
                var empty = document.createElement('li');
                empty.className = 'muted';
                empty.textContent = 'No menu items yet. Add some with POST /api/menu-items/.';
                list.appendChild(empty);
                return;
            }
            items.forEach(function (item) {
                var row = document.createElement('li');
                var title = document.createElement('span');
                var price = document.createElement('span');
                title.textContent = item.title;
                price.className = 'price';
                price.textContent = '$' + item.price;
                row.appendChild(title);
                row.appendChild(price);
                list.appendChild(row);
            });
        })
        .catch(function (error) {
            list.innerHTML = '';
            var failed = document.createElement('li');
            failed.className = 'muted';
            failed.textContent = 'Could not load the menu (' + error.message + ').';
            list.appendChild(failed);
        });
});
