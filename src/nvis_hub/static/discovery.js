/* Native document discovery with optional filter and shelf enhancements. */
document.querySelectorAll('[data-discovery-form]').forEach(form => {
  form.addEventListener('change', event => {
    if (event.target instanceof HTMLSelectElement) form.requestSubmit();
  });
});

document.querySelectorAll('[data-shelf]').forEach(section => {
  const shelf = section.querySelector('.document-shelf');
  const controls = section.querySelector('.shelf-controls');
  const previous = section.querySelector('.shelf-previous');
  const next = section.querySelector('.shelf-next');
  if (!shelf || !controls || !previous || !next) return;
  function update() {
    const end = shelf.scrollWidth - shelf.clientWidth;
    controls.hidden = end <= 1;
    previous.disabled = shelf.scrollLeft <= 1;
    next.disabled = shelf.scrollLeft >= end - 1;
  }
  function move(direction) {
    shelf.scrollBy({
      left: direction * shelf.clientWidth * 0.9,
      behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth',
    });
  }
  previous.addEventListener('click', () => move(-1));
  next.addEventListener('click', () => move(1));
  shelf.addEventListener('scroll', update, { passive: true });
  if ('ResizeObserver' in window) new ResizeObserver(update).observe(shelf);
  else window.addEventListener('resize', update);
  update();
});
