const addButtonOpen = document.getElementById('add-button');
const addButtonClose = document.getElementById('add-page-close-btn');

//追加画面のモーダル
//モーダル表示したいHTMLをclass="modal"にしないといけない
const addModal = document.getElementById('add-channel-modal');
//編集ボタンがクリックされたとき
addButtonOpen.addEventListener('click',() => {
  addModal.style.display = 'block';
})
//バツ印がクリックされたとき
addButtonClose.addEventListener('click', () => {
  addModal.style.display = 'none';
})

//モーダル画面以外にクリックされたときモーダル閉じる
addEventListener('click', (e) => {
  //modalはモーダル全体を構成する要素なのでターゲットをモーダルにする
  if (e.target == addModal) {
    addModal.style.display = 'none';
  }
})