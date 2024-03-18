self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.open('HBB-static-v1').then(function(cache) {
      return cache.match(event.request).then(function(response) {
        return response || fetch(event.request).then(function(response) {
          cache.put(event.request, response.clone());
          return response;
        });
      });
    })
  );
});

self.addEventListener('online', function(event) {
  // Device is back online, display notification
  self.registration.showNotification('Back Online', {
    body: 'You are now back online!',
    icon: '/static/icons8-online-48.png', // Provide ication
    badge: '/static/icons8-online-48.png', // Optional badge icon for notification
    vibrate: [200, 100, 200] // Optional vibration pattern
  });
});

self.addEventListener('offline', function(event) {
  // Device is offline
  // You can optionally handle this event to display a message or take other actions
});
