// 집투 서비스워커 — 목적은 '오프라인 안내' 하나뿐이다.
//
// ⚠ 앱 자산(js/css/데이터)은 절대 캐시하지 않는다. 집투는 하루에도 여러 번 배포하는데
//    자산을 캐시하면 사용자가 옛 빌드에 갇힌다. 실제로 GitHub Pages가 index.html에 거는
//    10분 캐시만으로도 '고쳤는데 안 바뀐다'는 혼선이 반복됐다(2026-08-10).
//    여기서는 화면 이동(navigate) 요청이 '네트워크 실패'했을 때만 안내 페이지를 돌려준다.
//    성공하면 항상 네트워크 응답을 그대로 쓴다 — 캐시가 끼어들 여지가 없다.
//
// 왜 필요한가: iOS 앱 심사(가이드라인 2.1)에서 네트워크가 없을 때 흰 화면이 뜨면 감점된다.
const CACHE = 'zipto-offline-v1'
const OFFLINE = './offline.html'

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll([OFFLINE, './icon-192.png'])).then(() => self.skipWaiting()))
})

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()))
})

self.addEventListener('fetch', e => {
  if (e.request.mode !== 'navigate') return          // 자산·API는 손대지 않는다
  e.respondWith(fetch(e.request).catch(() => caches.match(OFFLINE)))
})

// ── 웹푸시 수신 ────────────────────────────────────────────────────
// 서버(Cloudflare Worker)가 보낸 알림을 띄운다. 매일 실거래 갱신 후 관심 단지에 새 거래가
// 붙으면 발송된다. 클릭하면 그 단지 상세로 바로 들어가게 url을 함께 싣는다.
self.addEventListener('push', e => {
  let d = {}
  try { d = e.data ? e.data.json() : {} } catch { d = { body: e.data && e.data.text() } }
  const title = d.title || '집투'
  e.waitUntil(self.registration.showNotification(title, {
    body: d.body || '',
    icon: './icon-192.png',
    badge: './icon-192.png',
    tag: d.tag || undefined,          // 같은 단지 알림은 겹쳐 쌓이지 않게 묶는다
    data: { url: d.url || './' },
  }))
})

self.addEventListener('notificationclick', e => {
  e.notification.close()
  const url = (e.notification.data && e.notification.data.url) || './'
  // 이미 열린 탭이 있으면 그 탭을 쓰고, 없을 때만 새로 연다 — 알림마다 탭이 쌓이면 성가시다.
  e.waitUntil(self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then(list => {
    for (const c of list) if ('focus' in c) return c.navigate(url).then(x => x.focus()).catch(() => c.focus())
    return self.clients.openWindow(url)
  }))
})
