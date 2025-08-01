
export function getDeviceType() {
  const ua = navigator.userAgent

  if (/Mobi|Android|iPhone|iPad|iPod/i.test(ua)) {
    return 'mobile'
  }

  if (/Windows|Macintosh|Linux/i.test(ua)) {
    return 'desktop'
  }

  return 'unknown'
}