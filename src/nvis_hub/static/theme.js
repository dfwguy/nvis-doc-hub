/* Apply the saved preference before styles load; native switch applies immediately. */
(() => {
  const storageKey = 'nvis-hub-theme';
  const root = document.documentElement;
  const validTheme = value => value === 'light' || value === 'dark';

  function savedTheme() {
    try {
      const value = window.localStorage.getItem(storageKey);
      return validTheme(value) ? value : 'dark';
    } catch {
      return 'dark';
    }
  }

  function apply(theme, persist = false) {
    const value = validTheme(theme) ? theme : 'dark';
    const dark = value === 'dark';
    root.dataset.theme = value;
    document.querySelector('meta[name="color-scheme"]')?.setAttribute('content', value);
    document.querySelectorAll('[data-theme-toggle]').forEach(button => {
      button.setAttribute('aria-checked', String(dark));
      button.title = dark ? 'Use light mode' : 'Use dark mode';
    });
    if (persist) {
      try {
        window.localStorage.setItem(storageKey, value);
      } catch {
        // The current page can still switch when browser storage is unavailable.
      }
    }
  }

  apply(savedTheme());

  function connect() {
    document.querySelectorAll('[data-theme-toggle]').forEach(button => {
      button.hidden = false;
      button.addEventListener('click', () => {
        apply(root.dataset.theme === 'dark' ? 'light' : 'dark', true);
      });
    });
    apply(root.dataset.theme);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', connect);
  else connect();

  window.addEventListener('storage', event => {
    if (event.key === storageKey || event.key === null) apply(event.newValue);
  });
})();
