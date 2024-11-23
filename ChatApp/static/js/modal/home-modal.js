document.addEventListener('DOMContentLoaded', function() {
    const openModalButtons = document.querySelectorAll('.js-modal-button');
    const closeModalButtons = document.querySelectorAll('.js-close-button');
    const modalLayer = document.querySelector('.js-home-modal');
  
    // モーダルを開く
    openModalButtons.forEach(button => {
      button.addEventListener('click', function() {
        modalLayer.style.display = 'block'; // モーダルを表示
      });
    });
  
    // モーダルを閉じる
    closeModalButtons.forEach(button => {
      button.addEventListener('click', function() {
        modalLayer.style.display = 'none'; // モーダルを非表示
      });
    });
  
    // モーダルの外側をクリックした場合の動作
    modalLayer.addEventListener('click', function(event) {
      if (event.target === modalLayer) {
        modalLayer.style.display = 'none';
      }
    });
  });
  