 
export function haversineDistanceBetweenPoints(lat1, lon1, lat2, lon2) {
  const R = 6378; // km
  const p1 = lat1 * Math.PI/180;
  const p2 = lat2 * Math.PI/180;
  const deltaLon = lon2 - lon1;
  const deltaLambda = (deltaLon * Math.PI) / 180;
  const d = Math.acos(
    Math.sin(p1) * Math.sin(p2) + Math.cos(p1) * Math.cos(p2) * Math.cos(deltaLambda),
  ) * R;
  return d;
}

export function cosineDistanceBetweenPoints(lat1, lon1, lat2, lon2) {
  const R = 6371e3;
  const p1 = lat1 * Math.PI/180;
  const p2 = lat2 * Math.PI/180;
  const deltaP = p2 - p1;
  const deltaLon = lon2 - lon1;
  const deltaLambda = (deltaLon * Math.PI) / 180;
  const a = Math.sin(deltaP/2) * Math.sin(deltaP/2) +
            Math.cos(p1) * Math.cos(p2) *
            Math.sin(deltaLambda/2) * Math.sin(deltaLambda/2);
  const d = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)) * R;
  return d;
}


export function findNearest(locations, reference, df) {
  let minDist = Infinity;
  let nearest = null;
  for (const loc of locations) {
    const dist = df(reference.lat, reference.lon, loc.lat, loc.lon);

    if (dist < minDist) {
      minDist = dist;
      nearest = loc;
    }
  }
  
  return {nearest,minDist};
}