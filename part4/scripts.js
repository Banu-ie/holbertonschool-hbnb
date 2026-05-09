const API_URL = 'http://127.0.0.1:5000';

function getCookie(name) {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? decodeURIComponent(match[2]) : null;
}

function getQueryParam(param) {
  return new URLSearchParams(window.location.search).get(param);
}

function renderStars(rating) {
  const full = String.fromCodePoint(0x2605);
  const empty = String.fromCodePoint(0x2606);
  return full.repeat(rating) + empty.repeat(5 - rating);
}

/* TASK 1 - LOGIN */
async function loginUser(email, password) {
  try {
    const response = await fetch(API_URL + '/api/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email, password: password })
    });
    if (response.ok) {
      const data = await response.json();
      document.cookie = 'token=' + data.access_token + '; path=/';
      window.location.href = 'index.html';
    } else {
      const errorDiv = document.getElementById('login-error');
      if (errorDiv) {
        errorDiv.textContent = 'Login failed: invalid email or password.';
        errorDiv.classList.remove('hidden');
      }
    }
  } catch (err) {
    const errorDiv = document.getElementById('login-error');
    if (errorDiv) {
      errorDiv.textContent = 'Network error. Is the API running?';
      errorDiv.classList.remove('hidden');
    }
  }
}

/* TASK 2 - INDEX */
function initIndex() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
  if (loginLink) {
    loginLink.style.display = token ? 'none' : 'block';
  }
  fetchPlaces(token);
}

async function fetchPlaces(token) {
  const headers = {};
  if (token) { headers['Authorization'] = 'Bearer ' + token; }
  try {
    const response = await fetch(API_URL + '/api/v1/places', { headers: headers });
    if (!response.ok) { throw new Error('Failed to fetch'); }
    const places = await response.json();
    displayPlaces(places);
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
      priceFilter.addEventListener('change', function() {
        filterPlaces(places, priceFilter.value);
      });
    }
  } catch (err) {
    const list = document.getElementById('places-list');
    if (list) { list.innerHTML = '<p style="color:var(--text-muted)">Could not load places. Make sure the API is running.</p>'; }
  }
}

function displayPlaces(places) {
  const list = document.getElementById('places-list');
  if (!list) { return; }
  list.innerHTML = '';
  if (!places || places.length === 0) {
    list.innerHTML = '<p style="color:var(--text-muted)">No places found.</p>';
    return;
  }
  places.forEach(function(place) {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.dataset.price = place.price || 0;
    const price = place.price;
    card.innerHTML =
      '<h3>' + place.title + '</h3>' +
      '<p class="price">$' + price + ' / night</p>' +
      '<a href="place.html?id=' + place.id + '" class="details-button">View Details</a>';
    list.appendChild(card);
  });
}

function filterPlaces(places, maxPrice) {
  const cards = document.querySelectorAll('.place-card');
  cards.forEach(function(card) {
    const price = parseFloat(card.dataset.price);
    const show = maxPrice === 'all' || price <= parseFloat(maxPrice);
    card.style.display = show ? '' : 'none';
  });
}

/* TASK 3 - PLACE DETAILS */
function initPlaceDetails() {
  const token = getCookie('token');
  const placeId = getQueryParam('id');
  const loginLink = document.getElementById('login-link');
  if (loginLink) { loginLink.style.display = token ? 'none' : 'block'; }
  const addReview = document.getElementById('add-review');
  if (addReview) { addReview.style.display = token ? 'block' : 'none'; }
  if (!placeId) {
    const section = document.getElementById('place-details');
    if (section) { section.innerHTML = '<p>Invalid place ID.</p>'; }
    return;
  }
  fetchPlaceDetails(token, placeId);
}

async function fetchPlaceDetails(token, placeId) {
  const headers = {};
  if (token) { headers['Authorization'] = 'Bearer ' + token; }
  try {
    const response = await fetch(API_URL + '/api/v1/places/' + placeId, { headers: headers });
    if (!response.ok) { throw new Error('Not found'); }
    const place = await response.json();
    displayPlaceDetails(place);
  } catch (err) {
    const section = document.getElementById('place-details');
    if (section) { section.innerHTML = '<p style="color:var(--text-muted)">Could not load place details.</p>'; }
  }
}

function displayPlaceDetails(place) {
  const section = document.getElementById('place-details');
  if (!section) { return; }
  const amenities = place.amenities || [];
  const amenitiesHTML = amenities.map(function(a) {
    return '<span class="amenity-tag">' + (a.name || a) + '</span>';
  }).join('');
  const price = place.price;
  const host = (place.owner && place.owner.first_name) ? place.owner.first_name : (place.host_name || 'Unknown');
  const maxGuest = place.max_guest !== undefined ? place.max_guest : 'N/A';
  section.innerHTML =
    '<h1>' + place.title + '</h1>' +
    '<div class="place-info">' +
      '<span class="info-price">$' + price + ' / night</span>' +
      '<span>Host: ' + host + '</span>' +
      '<span>Max guests: ' + maxGuest + '</span>' +
    '</div>' +
    '<p class="description">' + (place.description || 'No description provided.') + '</p>' +
    '<div class="amenities-list">' + (amenitiesHTML || '<span class="amenity-tag">No amenities listed</span>') + '</div>';

  const reviewsList = document.getElementById('reviews-list');
  if (reviewsList) {
    const reviews = place.reviews || [];
    if (reviews.length === 0) {
      reviewsList.innerHTML = '<p style="color:var(--text-muted)">No reviews yet.</p>';
    } else {
      reviewsList.innerHTML = reviews.map(function(r) {
        const reviewer = (r.user && r.user.first_name) ? r.user.first_name : (r.user_name || 'Guest');
        return '<div class="review-card">' +
          '<p class="reviewer">' + reviewer + '</p>' +
          '<p class="rating">' + renderStars(r.rating) + '</p>' +
          '<p class="comment">' + (r.text || r.comment || '') + '</p>' +
          '</div>';
      }).join('');
    }
  }

  const reviewForm = document.getElementById('review-form');
  const placeId = getQueryParam('id');
  if (reviewForm && placeId) { wireReviewForm(reviewForm, placeId); }
}

/* TASK 4 - ADD REVIEW */
function initAddReview() {
  const token = getCookie('token');
  if (!token) { window.location.href = 'index.html'; return; }
  const placeId = getQueryParam('id');
  if (!placeId) { window.location.href = 'index.html'; return; }
  const reviewForm = document.getElementById('review-form');
  if (reviewForm) { wireReviewForm(reviewForm, placeId, token); }
}

function wireReviewForm(form, placeId, token) {
  const t = token || getCookie('token');
  form.addEventListener('submit', async function(event) {
    event.preventDefault();
    const reviewTextEl = document.getElementById('review-text');
    const ratingEl = form.querySelector('[name="rating"]');
    const reviewText = reviewTextEl ? reviewTextEl.value.trim() : '';
    const rating = ratingEl ? ratingEl.value : '';
    if (!reviewText || !rating) {
      showReviewMessage('Please fill in all fields.', false);
      return;
    }
    await submitReview(t, placeId, reviewText, parseInt(rating));
  });
}

async function submitReview(token, placeId, reviewText, rating) {
  try {
    const response = await fetch(API_URL + '/api/v1/places/' + placeId + '/reviews', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token
      },
      body: JSON.stringify({ text: reviewText, rating: rating })
    });
    if (response.ok) {
      showReviewMessage('Review submitted successfully!', true);
      const form = document.getElementById('review-form');
      if (form) { form.reset(); }
    } else {
      showReviewMessage('Failed to submit review.', false);
    }
  } catch (err) {
    showReviewMessage('Network error. Please try again.', false);
  }
}

function showReviewMessage(message, success) {
  const el = document.getElementById('review-message');
  if (!el) { return; }
  el.textContent = message;
  el.className = success ? 'alert-success' : 'alert-error';
  el.classList.remove('hidden');
  setTimeout(function() { el.classList.add('hidden'); }, 5000);
}

/* ROUTER */
document.addEventListener('DOMContentLoaded', function() {
  const page = window.location.pathname.split('/').pop() || 'index.html';
  if (page === 'index.html' || page === '' || page === '/') { initIndex(); }
  if (page === 'login.html') {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
      loginForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        await loginUser(email, password);
      });
    }
  }
  if (page === 'place.html') { initPlaceDetails(); }
  if (page === 'add_review.html') { initAddReview(); }
});
