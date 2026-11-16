(() => {
  'use strict';

  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('#main-nav');

  if (toggle && nav) {
    const setMenuOpen = (open) => {
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Zapri navigacijo' : 'Odpri navigacijo');
      nav.classList.toggle('is-open', open);
    };

    toggle.addEventListener('click', () => {
      setMenuOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    nav.addEventListener('click', (event) => {
      if (event.target.closest('a')) setMenuOpen(false);
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && nav.classList.contains('is-open')) {
        setMenuOpen(false);
        toggle.focus();
      }
    });

    document.addEventListener('pointerdown', (event) => {
      if (nav.classList.contains('is-open') &&
          !nav.contains(event.target) && !toggle.contains(event.target)) {
        setMenuOpen(false);
      }
    });

    const desktop = window.matchMedia('(min-width: 1181px)');
    if (typeof desktop.addEventListener === 'function') {
      desktop.addEventListener('change', ({ matches }) => {
        if (matches) setMenuOpen(false);
      });
    }
  }

  for (const img of document.querySelectorAll('.photo img')) {
    const figure = img.closest('.photo');
    if (!figure) continue;

    const showFallback = () => figure.classList.add('is-unavailable');
    const showImage = () => figure.classList.remove('is-unavailable');
    img.addEventListener('error', showFallback);
    img.addEventListener('load', showImage);

    if (img.complete) {
      if (img.naturalWidth > 0) showImage();
      else showFallback();
    }
  }
})();
