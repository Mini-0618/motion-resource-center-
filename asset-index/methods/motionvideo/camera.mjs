// Adapted from MotionVideo LaunchFilm, MIT. See LICENSE-MotionVideo.txt.
// t is local scene time in seconds. Anchors use pixels in the source plane.
export function cameraAt(seconds, {duration, anchor, scale, drift = [0, 0],
  tilt = [0, 0], roll = [0, 0], perspective = 1350}) {
  if (![seconds, duration, perspective].every(Number.isFinite) ||
      duration <= 0 || perspective <= 0) throw new RangeError("Invalid camera timing or perspective");
  for (const pair of [anchor, scale, drift, tilt, roll]) {
    if (!Array.isArray(pair) || pair.length !== 2 || !pair.every(Number.isFinite))
      throw new TypeError("Expected a pair of finite numbers");
  }
  if (scale.some(value => value <= 0)) throw new RangeError("Scale must be positive");
  const progress = Math.max(0, Math.min(1, seconds / duration));
  const zoom = scale[0] * (scale[1] / scale[0]) ** progress;
  const rotation = roll[0] + (roll[1] - roll[0]) * progress;
  return {
    perspective: perspective + "px",
    transformOrigin: anchor[0] + "px " + anchor[1] + "px",
    transform: `translate3d(${drift[0] * progress}px, ${drift[1] * progress}px, 0) rotateX(${tilt[0]}deg) rotateY(${tilt[1]}deg) rotateZ(${rotation}deg) scale(${zoom})`
  };
}
