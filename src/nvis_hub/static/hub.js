/* Progressive enhancements: reading and search work without JavaScript. */
const status = document.querySelector('#copy-status');
const filters = document.querySelector('.search-filters');
if (filters && matchMedia('(max-width: 1100px)').matches && filters.dataset.activeFilters === 'false') {
  filters.open = false;
}

const selectedDocument = document.querySelector('.sidebar .tree-link[aria-current="page"]');
const sidebarScroll = document.querySelector('.sidebar-scroll');
if (selectedDocument && sidebarScroll) {
  sidebarScroll.scrollTop += selectedDocument.getBoundingClientRect().top
    - sidebarScroll.getBoundingClientRect().top - sidebarScroll.clientHeight * 0.45;
}

async function copyText(text, button, successText) {
  const original = button.textContent;
  try {
    await navigator.clipboard.writeText(text);
    button.textContent = successText;
    if (status) status.textContent = successText;
    setTimeout(() => { button.textContent = original; }, 2000);
  } catch {
    button.textContent = 'Select and copy';
    if (status) status.textContent = 'Clipboard unavailable. Select the code and copy it.';
    const code = button.parentElement.querySelector('code');
    if (code) {
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
    }
  }
}

document.querySelectorAll('.prose pre').forEach(pre => {
  const code = pre.querySelector('code');
  if (!code) return;
  const button = document.createElement('button');
  button.type = 'button';
  button.className = 'copy-code';
  button.textContent = 'Copy code';
  button.setAttribute('aria-label', 'Copy code block');
  button.addEventListener('click', () => copyText(code.textContent, button, 'Copied'));
  const block = document.createElement('div');
  block.className = 'code-block';
  pre.before(block);
  block.append(button, pre);
  pre.classList.add('has-copy');
});

document.querySelector('[data-copy-page]')?.addEventListener('click', event => {
  copyText(window.location.href, event.currentTarget, 'Link copied');
});

document.addEventListener('keydown', event => {
  if (event.key === 'Escape') {
    const menu = document.querySelector('.mobile-menu[open]');
    if (menu) { menu.open = false; menu.querySelector('summary').focus(); }
  }
  if (event.key !== '/' || event.ctrlKey || event.metaKey || event.altKey) return;
  if (event.target.closest('input, textarea, select, [contenteditable]')) return;
  const input = document.querySelector('[data-search-input]');
  if (input) { event.preventDefault(); input.focus(); }
});

document.querySelectorAll('form[role="search"]').forEach(form => {
  form.addEventListener('submit', event => {
    const button = event.submitter;
    if (!button) return;
    button.dataset.previousLabel = button.textContent;
    button.textContent = 'Searching…';
    button.setAttribute('aria-busy', 'true');
    button.disabled = true;
  });
});
window.addEventListener('pageshow', () => {
  document.querySelectorAll('[data-previous-label]').forEach(button => {
    button.textContent = button.dataset.previousLabel;
    button.disabled = false;
    button.removeAttribute('aria-busy');
  });
});

const tocLinks = [...document.querySelectorAll('.contents-inner nav a')];
if (tocLinks.length && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    const visible = entries.find(entry => entry.isIntersecting);
    if (!visible) return;
    tocLinks.forEach(link => {
      if (decodeURIComponent(link.hash.slice(1)) === visible.target.id) link.setAttribute('aria-current', 'location');
      else link.removeAttribute('aria-current');
    });
  }, { rootMargin: '-10% 0px -65% 0px' });
  document.querySelectorAll('.prose h2[id], .prose h3[id]').forEach(heading => observer.observe(heading));
}
