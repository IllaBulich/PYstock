document.addEventListener('DOMContentLoaded', function () {
    const submitButton = document.getElementById('submitData');
    submitButton.addEventListener('click', sendDataToServer);
    

    function sendDataToServer() {
        const rows = document.querySelectorAll('table tbody tr');
        const data = [];

        rows.forEach(row => {
            const id = row.getAttribute('data-item-id');
            const quantity = parseInt(row.querySelector(`input[name="quantity_${id}"]`).value);
            const cost = parseFloat(row.querySelector(`input[name="cost_${id}"]`).value);

            if (quantity !== 0) {
                // Создание словаря и добавление его в массив
                data.push({ id, quantity, cost });
            }
        });

        // Отправка данных на сервер с использованием fetch API
        fetch('/product/sales_item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Добавляем CSRF токен для защиты от CSRF атак
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка сети');
            }
            return response.json();
        })
        .then(data => {
            console.log('Данные успешно отправлены на сервер:', data);
            // Дополнительные действия после успешной отправки данных
        })
        .catch(error => {
            console.error('Ошибка отправки данных:', error.message);
            // Дополнительные действия в случае ошибки
        });
        location.reload();
    }

    // Функция для получения CSRF токена из куки
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});