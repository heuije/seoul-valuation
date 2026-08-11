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
