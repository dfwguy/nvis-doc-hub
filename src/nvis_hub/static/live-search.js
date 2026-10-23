/* Match the server's conservative display rule without changing result URLs/data. */
const titleCommands = new Set((document.body.dataset.titleCommands || '').split(' '));
function displaySearchTitle(value) {
  const match = /^(\s*["'“‘(]*)(\S+)/u.exec(value);
  if (!match) return value;
  const token = match[2].replace(/[,;:!?)\]}'"”’]+$/u, '');
  if (!token || !/^\p{Ll}/u.test(token) || titleCommands.has(token)
      || /[\d/\\._\-$@=<>`:]/u.test(token)
      || /\p{Lu}/u.test(token.slice(1))) return value;
  const first = token[0].toUpperCase();
  if (first.length !== 1) return value;
  const offset = match[1].length;
  return value.slice(0, offset) + first + value.slice(offset + 1);
}

/* Optional live suggestions; the ordinary search form remains the fallback. */
document.querySelectorAll('[data-search-input]').forEach((input, index) => {
  const form = input.form;
  const field = input.closest('.search-field');
  if (!form || !field) return;

  const wrapper = document.createElement('div');
  wrapper.className = 'search-combobox';
  const popup = document.createElement('div');
  popup.className = 'search-suggestions';
  popup.hidden = true;
  const list = document.createElement('ul');
  list.className = 'search-suggestions-list';
  list.id = `search-suggestions-${index}`;
  list.setAttribute('role', 'listbox');
  list.setAttribute('aria-label', 'Matching documentation');
  const message = document.createElement('p');
  message.className = 'search-suggestions-message';
  const all = document.createElement('a');
  all.className = 'search-suggestions-all';
  all.textContent = 'Open full search';
  all.tabIndex = -1;
  const announcement = document.createElement('span');
  announcement.className = 'sr-only';
  announcement.setAttribute('role', 'status');
  announcement.setAttribute('aria-live', 'polite');
  announcement.setAttribute('aria-atomic', 'true');
  const hint = document.createElement('span');
  hint.className = 'sr-only';
  hint.id = `search-suggestions-help-${index}`;
  hint.textContent = 'Type at least two characters for suggestions. Use Up and Down to choose, Enter to open, or Escape to close. Enter without a selection searches all results.';
  popup.append(message, list, all);
  field.before(wrapper);
  wrapper.append(field, popup, announcement, hint);
  input.autocomplete = 'off';
  input.setAttribute('role', 'combobox');
  input.setAttribute('aria-autocomplete', 'list');
  input.setAttribute('aria-haspopup', 'listbox');
  input.setAttribute('aria-controls', list.id);
  input.setAttribute('aria-expanded', 'false');
  input.setAttribute('aria-describedby', `${input.getAttribute('aria-describedby') || ''} ${hint.id}`.trim());

  let timer = null;
  let controller = null;
  let generation = 0;
  let choices = [];
  let active = -1;
  let currentKey = '';
  let composing = false;
  let pendingSelection = 0;

  function parameters() {
    const params = new URLSearchParams({ q: input.value.trim() });
    for (const name of ['project', 'topic', 'kind']) {
      const value = form.elements.namedItem(name)?.value;
      if (value) params.set(name, value);
    }
    return params;
  }

  function select(position) {
    active = position;
    choices.forEach((choice, i) => choice.setAttribute('aria-selected', String(i === active)));
    if (active < 0) input.removeAttribute('aria-activedescendant');
    else {
      input.setAttribute('aria-activedescendant', choices[active].id);
      choices[active].scrollIntoView({ block: 'nearest' });
    }
  }

  function dismiss() {
    clearTimeout(timer);
    timer = null;
    controller?.abort();
    controller = null;
    generation += 1;
    pendingSelection = 0;
    popup.hidden = true;
    popup.removeAttribute('aria-busy');
    input.setAttribute('aria-expanded', 'false');
    announcement.textContent = '';
    select(-1);
  }

  function position() {
    if (popup.hidden) return;
    const box = field.getBoundingClientRect();
    const viewport = window.visualViewport;
    const top = viewport?.offsetTop || 0;
    const bottom = top + (viewport?.height || window.innerHeight);
    if (box.bottom <= top || box.top >= bottom) {
      dismiss();
      return;
    }
    const below = bottom - box.bottom - 12;
    const above = box.top - top - 12;
    const flip = below < 200 && above > below;
    popup.classList.toggle('search-suggestions-above', flip);
    popup.style.setProperty('--suggestions-height', `${Math.max(0, Math.floor(flip ? above : below))}px`);
  }

  function open() {
    popup.hidden = false;
    input.setAttribute('aria-expanded', 'true');
    position();
  }

  function showMessage(text) {
    list.replaceChildren();
    choices = [];
    active = -1;
    input.removeAttribute('aria-activedescendant');
    message.textContent = text;
    message.hidden = false;
    announcement.textContent = text;
    open();
  }

  function render(results) {
    list.replaceChildren();
    choices = [];
    for (const result of results.slice(0, 5)) {
      const url = new URL(result.url, window.location.origin);
      if (url.origin !== window.location.origin || !url.pathname.startsWith('/projects/')) continue;
      const row = document.createElement('li');
      row.setAttribute('role', 'presentation');
      const link = document.createElement('a');
      link.className = 'search-suggestion';
      link.id = `${list.id}-option-${choices.length}`;
      link.href = url.href;
      link.tabIndex = -1;
      link.setAttribute('role', 'option');
      link.setAttribute('aria-selected', 'false');
      const title = document.createElement('span');
      title.className = 'search-suggestion-title';
      title.textContent = displaySearchTitle(result.heading || result.title);
      const context = document.createElement('span');
      context.className = 'search-suggestion-context';
      context.textContent = result.heading && result.heading !== result.title
        ? `${displaySearchTitle(result.project_title)} · ${displaySearchTitle(result.title)}` : displaySearchTitle(result.project_title);
      const excerpt = document.createElement('span');
      excerpt.className = 'search-suggestion-excerpt';
      excerpt.textContent = result.snippet.replace(/\s+/g, ' ').trim();
      link.append(title, context, excerpt);
      row.append(link);
      list.append(row);
      choices.push(link);
    }
    if (!choices.length) {
      showMessage('No matching documentation. Try another term.');
      return;
    }
    message.hidden = true;
    active = -1;
    open();
    announcement.textContent = `${choices.length} matching ${choices.length === 1 ? 'section' : 'sections'}. Use Up and Down to choose a result.`;
    if (pendingSelection) select(pendingSelection > 0 ? 0 : choices.length - 1);
    pendingSelection = 0;
  }

  async function load() {
    timer = null;
    if (composing || document.activeElement !== input) return;
    const params = parameters();
    const key = params.toString();
    const request = generation;
    controller = new AbortController();
    all.href = `/search?${key}`;
    popup.setAttribute('aria-busy', 'true');
    showMessage('Searching documentation…');
    try {
      const response = await fetch(`/api/search/suggestions?${key}`, {
        signal: controller.signal,
        headers: { Accept: 'application/json' },
      });
      if (!response.ok) throw new Error('Suggestions unavailable');
      const results = await response.json();
      if (request !== generation || key !== parameters().toString() || document.activeElement !== input) return;
      if (!Array.isArray(results)) throw new Error('Invalid suggestions');
      currentKey = key;
      render(results);
    } catch (error) {
      if (request !== generation || error.name === 'AbortError') return;
      showMessage('Live results are unavailable. Press Enter or use Search to run a full search.');
    } finally {
      if (request === generation) popup.removeAttribute('aria-busy');
    }
  }

  function schedule(delay = 180, selection = 0) {
    dismiss();
    choices = [];
    currentKey = '';
    list.replaceChildren();
    const length = input.value.trim().length;
    if (composing || length < 2 || input.value.length > 200) return;
    pendingSelection = selection;
    timer = setTimeout(load, delay);
  }

  input.addEventListener('input', event => {
    if (!event.isComposing) schedule();
  });
  input.addEventListener('compositionstart', () => { composing = true; dismiss(); });
  input.addEventListener('compositionend', () => { composing = false; schedule(); });
  input.addEventListener('focus', () => {
    if (currentKey === parameters().toString() && choices.length) open();
    else schedule();
  });
  input.addEventListener('keydown', event => {
    if (composing || event.isComposing) return;
    if (event.key === 'Escape') {
      event.preventDefault();
      dismiss();
    } else if (event.key === 'Tab') dismiss();
    else if (event.key === 'Enter' && !popup.hidden && active >= 0) {
      event.preventDefault();
      const destination = choices[active].href;
      dismiss();
      window.location.assign(destination);
    } else if ((event.key === 'ArrowDown' || event.key === 'ArrowUp')
        && !event.altKey && !event.ctrlKey && !event.metaKey && input.value.trim().length >= 2) {
      event.preventDefault();
      const direction = event.key === 'ArrowDown' ? 1 : -1;
      if (choices.length && currentKey === parameters().toString()) {
        open();
        select(active < 0 ? (direction > 0 ? 0 : choices.length - 1)
          : Math.max(0, Math.min(choices.length - 1, active + direction)));
      } else schedule(0, direction);
    } else if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') select(-1);
  });
  form.addEventListener('change', event => { if (event.target !== input) schedule(); });
  form.addEventListener('submit', dismiss);
  document.addEventListener('pointerdown', event => { if (!wrapper.contains(event.target)) dismiss(); });
  document.addEventListener('focusin', event => { if (!wrapper.contains(event.target)) dismiss(); });
  window.addEventListener('resize', position);
  window.addEventListener('scroll', position, { passive: true });
  window.visualViewport?.addEventListener('resize', position);
  window.visualViewport?.addEventListener('scroll', position);
});
