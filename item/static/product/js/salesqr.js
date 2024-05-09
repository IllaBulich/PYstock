    document.addEventListener('DOMContentLoaded', function () {
        const submitButton = document.getElementById('submitData');
        submitButton.addEventListener('click', sendDataToServer);
        

        function sendDataToServer() {
            const date = document.getElementById('id_date');
            const selectedDate = date.value;
            const data = [];
            const quantity = document.getElementById('quantity').value;
            const cost = document.getElementById('cost').value;
            const id = document.getElementById('submitData').getAttribute('data-item-id');

            if (quantity !== 0) {
                // Создание словаря и добавление его в массив
                data.push({ id, quantity, cost, selectedDate });
            }
            

            // Отправка данных на сервер с использованием fetch API
            fetch('/item/sales_item', {
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