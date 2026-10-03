const preview = document.createElement('dialog');
preview.className = 'preview-dialog';
preview.innerHTML = '<div class="preview-bar"><span>Просмотр макета</span><button type="button" class="preview-close" aria-label="Закрыть просмотр">Закрыть ×</button></div><div class="preview-scroll"><img class="preview-image" alt=""></div>';
document.body.append(preview);

let previousFocus = null;
document.querySelectorAll('[data-expand]').forEach(button => {
  button.addEventListener('click', () => {
    const frame = document.getElementById(button.dataset.expand);
    const source = frame?.querySelector('img');
    if (!source) return;
    previousFocus = button;
    const image = preview.querySelector('.preview-image');
    image.src = source.src;
    image.alt = source.alt;
    preview.classList.toggle('mobile', frame.classList.contains('phone'));
    preview.showModal();
    preview.querySelector('.preview-scroll').scrollTop = 0;
    document.body.classList.add('preview-open');
    preview.querySelector('.preview-close').focus();
  });
});

preview.querySelector('.preview-close').addEventListener('click', () => preview.close());
preview.addEventListener('click', event => {
  if (event.target === preview) preview.close();
});
preview.addEventListener('close', () => {
  document.body.classList.remove('preview-open');
  previousFocus?.focus();
});
