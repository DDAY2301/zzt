(() => {
  'use strict';
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#main-nav');
  if (!toggle || !nav) return;
  const close = () => { toggle.setAttribute('aria-expanded', 'false'); toggle.setAttribute('aria-label', 'Odpri navigacijo'); nav.classList.remove('is-open'); };
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Zapri navigacijo' : 'Odpri navigacijo');
    nav.classList.toggle('is-open', open);
  });
  nav.addEventListener('click', event => { if (event.target.closest('a')) close(); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && nav.classList.contains('is-open')) { close(); toggle.focus(); }
  });
  document.addEventListener('click', event => {
    if (nav.classList.contains('is-open') && !nav.contains(event.target) && !toggle.contains(event.target)) close();
  });
  window.matchMedia('(min-width: 1181px)').addEventListener('change', e => { if(e.matches) close(); });
  document.querySelectorAll('.photo img').forEach(img => {
    const markUnavailable = () => img.closest('.photo')?.classList.add('is-unavailable');
    img.addEventListener('error', markUnavailable);
    if (img.complete && img.naturalWidth === 0) markUnavailable();
  });
})();
