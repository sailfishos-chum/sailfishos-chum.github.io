/**
 * Called when an image failed to load
 * @this {HTMLImageElement} image
 */
function loadImageFallback() {
  this.onerror = null;
  this.parentNode.children[0].srcset = this.parentNode.children[1].srcset = this.src;
}
