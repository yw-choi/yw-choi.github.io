for (const button of document.querySelectorAll('.figure-preview')) {
  const dialog = document.getElementById(button.getAttribute('aria-controls'));
  button.addEventListener('click', () => dialog.showModal());
  dialog.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const box = dialog.getBoundingClientRect();
    if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) dialog.close();
  });
}
