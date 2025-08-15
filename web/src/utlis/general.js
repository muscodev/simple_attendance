
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

export function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}


export function formatAsLocalYYYYMMDD(date) {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0'); // Months are 0-based
  const day = String(d.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
}