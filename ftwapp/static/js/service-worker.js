self.addEventListener('install', event => {
  console.log('Service Worker installed.');
});

self.addEventListener('fetch', event => {
  // Basic fetch passthrough for now
});