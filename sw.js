// Service Worker - 間歇訓練計時器
// 版本號：更新此版號可強制讓瀏覽器重新安裝 SW
const CACHE_NAME = 'interval-timer-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon.svg'
];

// ── 安裝：快取所有靜態資源 ──────────────────────────────────────────────────
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(ASSETS);
    })
  );
  // 立即啟用，不等舊 SW 失效
  self.skipWaiting();
});

// ── 啟用：清理舊版快取 ───────────────────────────────────────────────────────
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
      )
    )
  );
  // 立即接管所有分頁
  self.clients.claim();
});

// ── 攔截 fetch：Cache First，網路失敗時回傳快取版本 ─────────────────────────
self.addEventListener('fetch', event => {
  // 只處理同源請求
  if (!event.request.url.startsWith(self.location.origin)) return;

  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        // 成功取得時，更新快取
        if (response && response.status === 200 && response.type === 'basic') {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      }).catch(() => {
        // 完全離線且快取沒有：回傳 index.html（for navigation requests）
        if (event.request.mode === 'navigate') {
          return caches.match('./index.html');
        }
      });
    })
  );
});

// ── 接收來自主頁面的訊息 ─────────────────────────────────────────────────────
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
