// Функция, которая будет вызываться при отправке формы
function handleFormSubmit(event) {
  event.preventDefault(); // Предотвращаем отправку формы

  // Определяем, какая кнопка была нажата
  var target = event.submitter;
  var buttonId = target.getAttribute('id');

  // Определяем элемент div, в котором будут отображаться данные
  var statsUser = document.querySelector('.stats-user');

  // Очищаем содержимое элемента div
  statsUser.innerHTML = '';

  // В зависимости от нажатой кнопки выполняем соответствующий запрос и обрабатываем данные
  if (buttonId === 'sendbtn_GET_ALL') {
    // Запрос для получения всех пользователей
    fetch('/users')
      .then(response => response.json())
      .then(data => {
        // Обрабатываем полученные данные и выводим их в элемент div
        data.forEach(user => {
          var userInfo = document.createElement('p');
          userInfo.textContent = 'ID: ' + user.id + ', Имя: ' + user.name + ', Фамилия: ' + user.surname + ', Номер тел.: ' + user.phone;
          statsUser.appendChild(userInfo);
        });
      })
      .catch(error => console.error('Ошибка:', error));
  } else if (buttonId === 'sendbtn_GET_ID') {
    // Запрос для получения пользователя по ID
    var userId = document.getElementById('id').value; // Получаем значение ID из поля ввода
    fetch('/users/' + userId)
      .then(response => response.json())
      .then(data => {
        // Обрабатываем полученные данные и выводим их в элемент div
        var userInfo = document.createElement('p');
        userInfo.textContent = 'ID: ' + data.id + ', Имя: ' + data.name + ', Фамилия: ' + data.surname;
        statsUser.appendChild(userInfo);
      })
      .catch(error => console.error('Ошибка:', error));
  } else if (buttonId === 'sendbtn_POST') {
    // Запрос для добавления нового пользователя
    var formData = new FormData(event.target);
    fetch('/reg', {
      method: 'POST',
      body: formData
    })
      .then(response => response.text())
      .then(data => {
        // Выводим сообщение о результате операции
        var statusField = document.getElementById('statusfield');
        statusField.textContent = data;
      })
      .catch(error => console.error('Ошибка:', error));
  } else if (buttonId === 'sendbtn_PUT') {
    // Запрос для обновления пользователя по ID
    var userId = document.getElementById('id').value; // Получаем значение ID из поля ввода
    var formData = new FormData(event.target);
    fetch('/users/' + userId, {
      method: 'PUT',
      body: formData
    })
      .then(response => response.text())
      .then(data => {
        // Выводим сообщение о результате операции
        var statusField = document.getElementById('statusfield');
        statusField.textContent = data;
      })
      .catch(error => console.error('Ошибка:', error));
  } else if (buttonId === 'sendbtn_DELETE') {
    // Запрос для удаления пользователя по ID
    var userId = document.getElementById('id').value; // Получаем значение ID из поля ввода
    fetch('/users/' + userId, {
      method: 'DELETE'
    })
      .then(response => response.text())
      .then(data => {
        // Выводим сообщение о результате операции
        var statusField = document.getElementById('statusfield');
        statusField.textContent = data;
      })
      .catch(error => console.error('Ошибка:', error));
  }
}

// Добавляем обработчик события отправки формы
var form = document.getElementById('myForm');
form.addEventListener('submit', handleFormSubmit);
