(() => {
  const dialog = document.getElementById('news-dialog');
  const data = document.getElementById('news-data');
  if (!dialog || !data || typeof dialog.showModal !== 'function') return;
  const posts = new Map(JSON.parse(data.textContent).map(post => [post.id, post]));
  const image = document.getElementById('news-dialog-image');
  const title = document.getElementById('news-dialog-title');
  const comment = document.getElementById('news-dialog-comment');
  const date = document.getElementById('news-dialog-date');
  const link = document.getElementById('news-dialog-link');
  const previous = dialog.querySelector('.news-previous');
  const next = dialog.querySelector('.news-next');
  const count = dialog.querySelector('.news-slide-count');
  let post, current = 0, opener, priorOverflow, priorURL;
  let touchStart;

  function showPhoto(index) {
    current = (index + post.images.length) % post.images.length;
    image.src = post.images[current];
    image.alt = `${post.image_alt || post.label}${post.images.length > 1 ? ` (${current + 1} / ${post.images.length})` : ''}`;
    count.textContent = `${current + 1} / ${post.images.length}`;
    previous.hidden = next.hidden = count.hidden = post.images.length < 2;
  }

  function openPost(id, trigger, updateURL = true) {
    const selected = posts.get(id);
    if (!selected) return;
    if (!dialog.open) {
      opener = trigger || document.querySelector(`[data-news-id="${CSS.escape(id)}"]`);
      priorOverflow = document.documentElement.style.overflow;
      priorURL = location.pathname + location.search + (location.hash === `#${id}` ? '' : location.hash);
    }
    post = selected;
    image.parentElement.dataset.kind = post.kind || 'photo';
    title.hidden = !post.title;
    title.textContent = post.title || '';
    dialog.setAttribute('aria-label', post.title || 'News post');
    comment.textContent = post.comment;
    date.dateTime = post.date;
    date.textContent = post.displayDate;
    link.hidden = !post.link;
    if (post.link) {
      link.href = post.link;
      link.textContent = post.category === 'Paper' ? 'View publication ↗' : 'Learn more ↗';
    } else {
      link.removeAttribute('href');
    }
    showPhoto(0);
    document.documentElement.style.overflow = 'hidden';
    if (!dialog.open) dialog.showModal();
    dialog.scrollTop = 0;
    if (updateURL) history.replaceState(history.state, '', `#${id}`);
  }

  document.addEventListener('click', event => {
    const trigger = event.target.closest('a[data-news-id]');
    if (!trigger || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    if (!posts.has(trigger.dataset.newsId)) return;
    event.preventDefault();
    openPost(trigger.dataset.newsId, trigger);
  });
  dialog.querySelector('.news-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.documentElement.style.overflow = priorOverflow || '';
    if (post && location.hash === `#${post.id}`) history.replaceState(history.state, '', priorURL || location.pathname + location.search);
    opener?.focus({ preventScroll: true });
  });
  previous.addEventListener('click', () => showPhoto(current - 1));
  next.addEventListener('click', () => showPhoto(current + 1));
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      showPhoto(current + (event.key === 'ArrowLeft' ? -1 : 1));
    }
  });
  image.addEventListener('touchstart', event => {
    touchStart = [event.changedTouches[0].clientX, event.changedTouches[0].clientY];
  }, { passive: true });
  image.addEventListener('touchend', event => {
    if (!touchStart) return;
    const dx = event.changedTouches[0].clientX - touchStart[0];
    const dy = event.changedTouches[0].clientY - touchStart[1];
    if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy)) showPhoto(current + (dx < 0 ? 1 : -1));
    touchStart = null;
  }, { passive: true });
  function followHash() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    if (posts.has(id)) openPost(id, null, false);
    else if (dialog.open) dialog.close();
  }
  window.addEventListener('hashchange', followHash);
  followHash();
})();
