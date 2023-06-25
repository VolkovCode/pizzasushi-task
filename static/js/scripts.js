axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

const tableBody = document.querySelector('.table__body')
const replenishmentButton = document.querySelector('.replenishment-button')
const debitingButton = document.querySelector('.debiting-button')
const transferButton = document.querySelector('.transfer-button')
const error = document.querySelector('.error-text')

function makeTable(data) {
    tableBody.innerHTML = '';
    for (let i = 0; i < data.length; i++) {
        const tableRow = document.createElement('tr')
        const idAccount = document.createElement('td')
        const idUser = document.createElement('td')
        const balance = document.createElement('td')
        idUser.textContent = data[i].user_id
        idAccount.textContent = data[i].id
        balance.textContent = data[i].balance
        tableRow.appendChild(idAccount)
        tableRow.appendChild(idUser)
        tableRow.appendChild(balance)
        tableBody.appendChild(tableRow)
    }
}

function replenishmentButtonHandler() {
    const userId = document.querySelector('.replenishment-user').value;
    const amount = document.querySelector('.replenishment-amount').value;
    error.textContent = '';
    axios.post('http://127.0.0.1:8000/api/v1/replenishment/', {
        id: userId,
        amount: amount
    }).then(() => getTableData()).catch(function (error) {
        errorHandler(error.response.data.amount || error.response.data?.id)
    });
};

function debitingButtonHandler() {
    const userId = document.querySelector('.debiting-user').value
    const amount = document.querySelector('.debiting-amount').value
    error.textContent = '';
    axios.post('http://127.0.0.1:8000/api/v1/debiting/', {
        id: userId,
        amount: amount
    }).then(() => getTableData()).catch(function (error) {
        errorHandler(error.response.data[0] || error.response.data?.id)
    });
}

function errorHandler(errorText) {
    error.textContent = errorText
}

function transferButtonHandler() {
    const sendUserId = document.querySelector('.send-user').value
    const recipientUserId = document.querySelector('.recipient-user').value
    const amount = document.querySelector('.transfer-amount').value
    error.textContent = ''
    axios.post('http://127.0.0.1:8000/api/v1/transfer/', {
        from_user_id: sendUserId,
        to_user_id: recipientUserId,
        amount: amount
    }).then(() => getTableData()).catch(function (error) {
        errorHandler(error.response.data?.error || error.response.data?.amount || error.response.data?.id)
    });
}

async function getTableData() {
    await axios.get('http://127.0.0.1:8000/api/v1/balance/').then(resp => makeTable(resp.data))
};

getTableData()
replenishmentButton.addEventListener('click', () => replenishmentButtonHandler())
debitingButton.addEventListener('click', () => debitingButtonHandler())
transferButton.addEventListener('click', () => transferButtonHandler())