// ReadMath Resilient PWA Service Worker (v4)
// Strictly prevents null response errors during AI image upload and API syncing
// Bypasses cached HTML for navigation to guarantee hotfix immediacy
const CACHE_NAME = 'readmath-cache-v4';

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => caches.delete(name))
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  // 1. Never intercept non-GET requests (e.g. POST photo upload, user registration, question sync)
  if (event.request.method !== 'GET') {
    return;
  }

  const requestUrl = event.request.url;

  // 2. Never intercept AI APIs, remote database APIs, or browser extensions
  if (
    requestUrl.includes('generativelanguage.googleapis.com') ||
    requestUrl.includes('palin-os.onrender.com') ||
    requestUrl.includes('/api/') ||
    requestUrl.startsWith('chrome-extension://')
  ) {
    return;
  }

  // 3. For HTML documents/navigations, ALWAYS fetch fresh from network without caching stale HTML
  if (event.request.mode === 'navigate' || event.request.destination === 'document') {
    event.respondWith(
      fetch(event.request)
        .catch(async () => {
          const cached = await caches.match(event.request);
          if (cached) return cached;
          return new Response('Offline content unavailable', {
            status: 503,
            statusText: 'Service Unavailable',
            headers: { 'Content-Type': 'text/plain; charset=utf-8' }
          });
        })
    );
    return;
  }

  // 4. Network first with safe cache fallback for static assets
  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache).catch(() => {});
          });
        }
        return networkResponse;
      })
      .catch(async () => {
        const cachedResponse = await caches.match(event.request);
        if (cachedResponse) {
          return cachedResponse;
        }
        // Fallback response guarantees FetchEvent.respondWith never receives null/undefined
        return new Response('Offline content unavailable', {
          status: 503,
          statusText: 'Service Unavailable',
          headers: { 'Content-Type': 'text/plain; charset=utf-8' }
        });
      })
  );
});
