// 1. Спільний стан між сторінками (Global Shared State)
const state = {
    token: localStorage.getItem('token') || null,
    articles: []
};

const API_URL = 'http://127.0.0.1:8000'; // Адреса API з Lab 2

// 2. Базова навігація (Router)
function render() {
    const app = document.getElementById('app-content');
    const nav = document.getElementById('navbar');
    const hash = window.location.hash.replace('#', '') || 'home';

    // Якщо немає токена - показуємо сторінку логіну
    if (!state.token) {
        nav.style.display = 'none';
        app.innerHTML = `
            <h2>Авторизація</h2>
            <div id="error-msg" class="error"></div>
            <input type="text" id="username" placeholder="Логін (admin)">
            <input type="password" id="password" placeholder="Пароль (1234)">
            <button onclick="login()">Увійти</button>
        `;
        return;
    }

    // Якщо авторизований
    nav.style.display = 'flex';

    if (hash === 'home') {
        app.innerHTML = `<h2>Список статей</h2><div id="articles-container">Завантаження...</div>`;
        fetchArticles();
    } else if (hash === 'profile') {
        app.innerHTML = `
            <h2>Профіль користувача</h2>
            <p>Ви успішно авторизовані.</p>
            <p>Ваш збережений токен: <strong>${state.token}</strong></p>
        `;
    }
}

// 3. Авторизація та збереження токена
function login() {
    const user = document.getElementById('username').value;
    const pass = document.getElementById('password').value;
    
    if (user === 'admin' && pass === '1234') {
        state.token = 'fake-jwt-token-12345';
        localStorage.setItem('token', state.token); // Збереження токена
        window.location.hash = 'home';
        render();
    } else {
        document.getElementById('error-msg').innerText = 'Невірний логін або пароль!';
    }
}

function logout() {
    state.token = null;
    localStorage.removeItem('token');
    window.location.hash = '';
    render();
}

// 4. Підключення до API та обробка помилок
async function fetchArticles() {
    try {
        const response = await fetch(`${API_URL}/articles`);
        if (!response.ok) throw new Error(`HTTP помилка: ${response.status}`);
        
        state.articles = await response.json(); // Оновлення глобального стану
        
        const html = state.articles.map(article => `
            <div class="card">
                <h3>${article.title}</h3>
                <p>${article.content}</p>
                <small>ID Автора: ${article.author_id}</small>
            </div>
        `).join('');
        
        document.getElementById('articles-container').innerHTML = html || 'Немає даних.';
    } catch (error) {
        // Обробка помилок
        document.getElementById('articles-container').innerHTML = `
            <p class="error">Помилка підключення до API: ${error.message}</p>
            <p>Переконайтеся, що сервер Lab 2 запущено на порту 8000.</p>
        `;
    }
}

// Слухаємо зміни хешу для перемикання сторінок
window.addEventListener('hashchange', render);

// Перший рендер при завантаженні
render();
