const editButtonOpen = document.getElementById('edit-button');
const editButtonClose = document.getElementById('update-page-close-btn');

//編集画面のモーダル
//モーダル表示したいHTMLをclass="modal"にしないといけない
const modal = document.getElementById('update-channel-modal');
//編集ボタンがクリックされたとき
editButtonOpen.addEventListener('click',() => {
  modal.style.display = 'block';
})
editButtonClose.addEventListener('click', () => {
  modal.style.display = 'none';
})
//バツ印がクリックされたとき
editButtonClose.addEventListener('click', () => {
  modal.style.display = 'none';
})
addEventListener('click', (e) => {
  //modalはモーダル全体を構成する要素なのでターゲットをモーダルにする
  if (e.target == modal) {
    modal.style.display = 'none';
  }
})


//削除画面のモーダル
const deleteButtonOpen = document.getElementById('delete-button');
const deleteButtonClose = document.getElementById('delete-page-close-btn');

//モーダル表示したいHTMLをclass="modal"にしないといけない
const deleteModal = document.getElementById('delete-channel-modal');
//ボタンがクリックされたとき
deleteButtonOpen.addEventListener('click',() => {
  deleteModal.style.display = 'block';
})
//バツ印がクリックされたとき
deleteButtonClose.addEventListener('click', () => {
  deleteModal.style.display = 'none';
})
addEventListener('click', (e) => {
  //modalはモーダル全体を構成する要素なのでターゲットをモーダルにする
  if (e.target == deleteModal) {
    deleteModal.style.display = 'none';
  }
})

const inviteButtonOpen = document.getElementById('invite-button');
const inviteButtonClose = document.getElementById('invite-page-close-btn');

//モーダル表示したいHTMLをclass="modal"にしないといけない
const inviteModal = document.getElementById('invite-channel-modal');
//ボタンがクリックされたとき
inviteButtonOpen.addEventListener('click',() => {
  inviteModal.style.display = 'block';
})
//バツ印がクリックされたとき
inviteButtonClose.addEventListener('click', () => {
  inviteModal.style.display = 'none';
})
addEventListener('click', (e) => {
  //modalはモーダル全体を構成する要素なのでターゲットをモーダルにする
  if (e.target == inviteModal) {
    inviteModal.style.display = 'none';
  }
})