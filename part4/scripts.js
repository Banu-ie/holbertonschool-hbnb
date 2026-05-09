const API_URL = 'http://127.0.0.1:5000/api/v1';

function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return value || null;
    }
    return null;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

function getStars(rating) {
    return '\u2605'.repeat(rating) + '\u2606'.repeat(5 - rating);
}

async function loginUser(email, password) {
    const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });
    if (response.ok) {
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = 'index.html';
    } else {
        const errorMsg = document.getElementById('error-message');
        if (errorMsg) errorMsg.style.display = 'block';
        alert('Login failed: ' + response.statusText);
    }
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    if (loginLink) loginLink.style.display = token ? 'none' : 'block';
    return token;
}

async function fetchPlaces(token) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;
        const response = await fetch(`${API_URL}/places/`, { headers });
        if (!response.ok) throw new Error('Failed to fetch places');
        const places = await response.json();
        window._allPlaces = places;
        displayPlaces(places);
    } catch (error) {
        const list = document.getElementById('places-list');
        if (list) list.innerHTML = '<p class="empty-state">Unable to load places. Please try again later.</p>';
    }
}

function displayPlaces(places) {
    const list = document.getElementById('places-list');
    if (!list) return;
    list.innerHTML = '';
    if (!places || places.length === 0) {
        list.innerHTML = '<p class="empty-state">No places available.</p>';
        return;
    }
    places.forEach(place => {
        const card = document.createElement('div');
        card.classList.add('place-card');
        card.dataset.price = place.price || 0;
        card.innerHTML = `
            <h3>${place.title || place.name || 'Unnamed Place'}</h3>
            <p class="price">$${place.price || 0} / night</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;
        list.appendChild(card);
    });
}

function filterPlacesByPrice(maxPrice) {
    document.querySelectorAll('.place-card').forEach(card => {
        const price = parseFloat(card.dataset.price) || 0;
        card.style.display = (maxPrice === 'all' || price <= parseFloat(maxPrice)) ? 'flex' : 'none';
    });
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;
        const response = await fetch(`${API_URL}/places/${placeId}`, { headers });
        if (!response.ok) throw new Error('Place not found');
        const place = await response.json();
        displayPlaceDetails(place);
        fetchReviews(token, placeId);
    } catch (error) {
        const details = document.getElementById('place-details');
        if (details) details.innerHTML = '<p class="empty-state">Place not found or unavailable.</p>';
    }
}

function displayPlaceDetails(place) {
    const section = document.getElementById('place-details');
    if (!section) return;
    let amenitiesHTML = '<p>No amenities listed.</p>';
    if (place.amenities && place.amenities.length > 0) {
        const tags = place.amenities.map(a => `<span class="amenity-tag">${a.name || a}</span>`).join('');
        amenitiesHTML = `<div class="amenities-list">${tags}</div>`;
    }
    section.innerHTML = `
        <div class="place-details">
            <div class="place-info">
                <h2>${place.title || place.name || 'Unnamed Place'}</h2>
                <p><strong>Host:</strong> ${place.owner ? place.owner.first_name + ' ' + place.owner.last_name : 'N/A'}</p>
                <p><strong>Price per night:</strong> $${place.price || 0}</p>
                <p><strong>Description:</strong> ${place.description || 'No description available.'}</p>
                <p><strong>Amenities:</strong></p>
                ${amenitiesHTML}
            </div>
        </div>
        <div class="reviews-section">
            <h3>Reviews</h3>
            <div id="reviews-list"><p class="loading">Loading reviews...</p></div>
        </div>
    `;
}

async function fetchReviews(token, placeId) {
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;
        const response = await fetch(`${API_URL}/reviews/places/${placeId}`, { headers });
        const reviewsList = document.getElementById('reviews-list');
        if (!reviewsList) return;
        if (!response.ok) { reviewsList.innerHTML = '<p class="empty-state">No reviews yet.</p>'; return; }
        const reviews = await response.json();
        if (!reviews || reviews.length === 0) { reviewsList.innerHTML = '<p class="empty-state">No reviews yet. Be the first!</p>'; return; }
        reviewsList.innerHTML = '';
        reviews.forEach(review => {
            const card = document.createElement('div');
            card.classList.add('review-card');
            card.innerHTML = `
                <p class="reviewer">${review.user ? review.user.first_name + ' ' + review.user.last_name : 'Anonymous'}</p>
                <p class="rating">${getStars(review.rating || 0)} (${review.rating || 0}/5)</p>
                <p class="comment">${review.text || review.comment || ''}</p>
            `;
            reviewsList.appendChild(card);
        });
    } catch (error) {
        const reviewsList = document.getElementById('reviews-list');
        if (reviewsList) reviewsList.innerHTML = '<p class="empty-state">Could not load reviews.</p>';
    }
}

async function submitReview(token, placeId, reviewText, rating) {
    return await fetch(`${API_URL}/reviews/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ text: reviewText, rating: parseInt(rating), place_id: placeId })
    });
}

function handleResponse(response, form) {
    if (response.ok) {
        alert('Review submitted successfully!');
        if (form) form.reset();
        const placeId = getPlaceIdFromURL();
        window.location.href = placeId ? `place.html?id=${placeId}` : 'index.html';
    } else {
        alert('Failed to submit review. Please try again.');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const page = window.location.pathname.split('/').pop();

    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            await loginUser(
                document.getElementById('email').value.trim(),
                document.getElementById('password').value
            );
        });
    }

    if (page === 'index.html' || page === '') {
        const token = checkAuthentication();
        fetchPlaces(token);
        const priceFilter = document.getElementById('price-filter');
        if (priceFilter) {
            priceFilter.addEventListener('change', (event) => {
                filterPlacesByPrice(event.target.value);
            });
        }
    }

    if (page === 'place.html') {
        const token = checkAuthentication();
        const placeId = getPlaceIdFromURL();
        if (!placeId) {
            const d = document.getElementById('place-details');
            if (d) d.innerHTML = '<p class="empty-state">No place ID specified.</p>';
            return;
        }
        const addReviewSection = document.getElementById('add-review');
        if (addReviewSection) addReviewSection.style.display = token ? 'block' : 'none';
        fetchPlaceDetails(token, placeId);
        const reviewForm = document.getElementById('review-form');
        if (reviewForm && token) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const text = document.getElementById('review-text').value.trim();
                const rating = document.getElementById('rating').value;
                if (!text || !rating) { alert('Please fill in all fields.'); return; }
                const response = await submitReview(token, placeId, text, rating);
                handleResponse(response, reviewForm);
            });
        }
    }

    if (page === 'add_review.html') {
        const token = getCookie('token');
        if (!token) { window.location.href = 'index.html'; return; }
        checkAuthentication();
        const placeId = getPlaceIdFromURL();
        const reviewForm = document.getElementById('review-form');
        if (reviewForm) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const text = document.getElementById('review-text').value.trim();
                const rating = document.getElementById('rating').value;
                if (!text || !rating) { alert('Please fill in all fields.'); return; }
                if (!placeId) { alert('No place specified.'); return; }
                const response = await submitReview(token, placeId, text, rating);
                handleResponse(response, reviewForm);
            });
        }
    }
});
