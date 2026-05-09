const API_URL = 'http://127.0.0.1:5000';

/* --- UTILS --- */
function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? decodeURIComponent(match[2]) : null;
}

function getQueryParam(param) {
  return new URLSearchParams(window.location.search).get(param);
}

function renderStars(rating) {
  return '★'.repeat(rating) + '☆'.repeat(5 - rating);
}

/* --- TASK 1: LOGIN --- */
async function loginUser(email, password) {
  const response = await fetch(`${API_URL}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (response.ok) {
    const data = await response.json();
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
  } else {
    const errorDiv = document.getElementById('login-error');
    if (errorDiv) {
      errorDiv.textContent = 'Login failed: invalid email or password.';
      errorDiv.classList.remove('hidden');
    }
  }
}

/* --- TASK 2: INDEX --- */
function initIndex() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  if (loginLink) loginLink.style.display = token ? 'none' : 'block';
  fetchPlaces(token);
}

async function fetchPlaces(token) {
  const headers = {};
  if (token) headers['Authorization'] = `Bearer ${token}`;
  try {
    const response = await fetch(`${API_URL}/places`, { headers });
    if (!response.ok) throw new Error('Failed');
    const places = await response.json();
    displayPlaces(places);
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
      priceFilter.addEventListener('change', () => filterPlaces(places, priceFilter.value));
    }
  } catch {
    document.getElementById('places-list').innerHTML =
      '<p style="color:var(--text-muted)">Could not load places. Make sure the API is running.</p>';
  }
}

function displayPlaces(places) {
  const list = document.getElementById('places-list');
  list.innerHTML = '';
  if (!places || places.length === 0) {
    list.innerHTML = '<p style="color:var(--text-muted)">No places found.</p>';
    return;
  }
  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.dataset.price = place.price_by_night || place.price || 0;
    card.innerHTML = `
      <h3>${place.name}</h3>
      <p class="price">$${place.price_by_night ?? place.price ?? 'N/A'} / night</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;
    list.appendChild(card);
  });
}

function filterPlaces(places, maxPrice) {
  document.querySelectorAll('.place-card').forEach(card => {
    const price = parseFloat(card.dataset.price);
    card.style.display = (maxPrice === 'all' || price <= parseFloat(maxPrice)) ? '' : 'none';
  });
}

/* --- TASK 3: PLACE DETAILS --- */
function initPlaceDetails() {
  const token = getCookie('token');
  const placeId = getQueryParam('id');
  const loginLink = document.getElementById('login-link');
  if (loginLink) loginLink.style.display = token ? 'none' : 'block';
  const addReview = document.getElementById('add-review');
  if (addReview) addReview.style.display = token ? 'block' : 'none';
  if (!placeId) {
    document.getElementById('place-details').innerHTML = '<p>Invalid place ID.</p>';
    return;
  }
  fetchPlaceDetails(token, placeId);
}

async function fetchPlaceDetails(token, placeId) {
  const headers = {};
  if (token) headers['Authorization'] = `Bearer ${token}`;
  try {
    const response = await fetch(`${API_URL}/places/${placeId}`, { headers });
    if (!response.ok) throw new Error('Not found');
    const place = await response.json();
    displayPlaceDetails(place);
  } catch {
    document.getElementById('place-details').innerHTML =
      '<p style="color:var(--text-muted)">Could not load place details.</p>';
  }
}

function displayPlaceDetails(place) {
  const section = document.getElementById('place-details');
  const amenitiesHTML = (place.amenities || [])
    .map(a => `<span class="amenity-tag">${a.name || a}</span>`).join('');
  section.innerHTML = `
    <h1>${place.name}</h1>
    <div class="place-info">
      <span class="info-price">$${place.price_by_night ?? place.price ?? 'N/A'} / night</span>
      <span>Host: ${place.owner?.first_name ?? place.host_name ?? 'Unknown'}</span>
      <span>Max guests: ${place.max_guest ?? 'N/A'}</span>
    </div>
    <p class="description">${place.description || 'No description provided.'}</p>
    <div class="amenities-list">${amenitiesHTML || '<span class="amenity-tag">No amenities listed</span>'}</div>
  `;
  const reviewsList = document.getElementById('reviews-list');
  if (reviewsList) {
    const reviews = place.reviews || [];
    reviewsList.innerHTML = reviews.length === 0
      ? '<p style="color:var(--text-muted)">No reviews yet.</p>'
      : reviews.map(r => `
          <div class="review-card">
            <p class="reviewer">${r.user?.first_name ?? r.user_name ?? 'Guest'}</p>
            <p class="rating">${renderStars(r.rating)}</p>
            <p class="comment">${r.text || r.comment || ''}</p>
          </div>`).join('');
  }
  const reviewForm = document.getElementById('review-form');
  const placeId = getQueryParam('id');
  if (reviewForm && placeId) wireReviewForm(reviewForm, placeId);
}

/* --- TASK 4: ADD REVIEW --- */
function initAddReview() {
  const token = getCookie('token');
  if (!token) { window.location.href = 'index.html'; return; }
  const placeId = getQueryParam('id');
  if (!placeId) { window.location.href = 'index.html'; return; }
  const reviewForm = document.getElementById('review-form');
  if (reviewForm) wireReviewForm(reviewForm, placeId, token);
}

function wireReviewForm(form, placeId, token) {
  token = token || getCookie('token');
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const reviewText = document.getElementById('review-text')?.value?.trim();
    const ratingEl = form.querySelector('[name="rating"]');
    const rating = ratingEl?.value;
    if (!reviewText || !rating) {
      showReviewMessage('Please fill in all fields.', false);
      return;
    }
    await submitReview(token, placeId, reviewText, parseInt(rating));
  });
}

async function submitReview(token, placeId, reviewText, rating) {
  try {
    const response = await fetch(`${API_URL}/places/${placeId}/reviews`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({ text: reviewText, rating }),
    });
    if (response.ok) {
      showReviewMessage('Review submitted successfully!', true);
      document.getElementById('review-form')?.reset();
    } else {
      showReviewMessage('Failed to submit review.', false);
    }
  } catch {
    showReviewMessage('Network error. Please try again.', false);
  }
}

function showReviewMessage(message, success) {
  const el = document.getElementById('review-message');
  if (!el) return;
  el.textContent = message;
  el.className = success ? 'alert-success' : 'alert-error';
  el.classList.remove('hidden');
  setTimeout(() => el.classList.add('hidden'), 5000);
}

/* --- ROUTER --- */
document.addEventListener('DOMContentLoaded', () => {
  const page = window.location.pathname.split('/').pop() || 'index.html';

  if (page === 'index.html' || page === '' || page === '/') initIndex();

  if (page === 'login.html') {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
      loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        await loginUser(email, password);
      });
    }
  }

  if (page === 'place.html') initPlaceDetails();
  if (page === 'add_review.html') initAddReview();
});
