// ReadMath Self-Destructing Service Worker
// Automatically deletes all existing caches and unregisters itself
// Guarantees zero stale caching across all client devices and browsers

self.addEventListener('install', () => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.map((k) => caches.delete(k))))
      .then(() => self.registration.unregister())
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', () => {
  // Pass through all network requests directly
  return;
});
