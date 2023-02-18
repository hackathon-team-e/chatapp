//メッセージ詳細画面で下にスクロールした状態で画面遷移
window.onload = function () {
  const elm = document.documentElement;
  // scrollHeight ページの高さ clientHeight ブラウザの高さ
  const bottom = elm.scrollHeight - elm.clientHeight;
  // 垂直方向へ移動
  window.scroll(0, bottom);
};