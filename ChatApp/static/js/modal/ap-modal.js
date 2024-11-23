// 「チャットする」ボタンを押した時に相手の画面に出るモーダル

// ユーザーAのアクションが、ユーザーBの画面に影響を与えるためにはサーバーとの連携が必要？　WebSocket、AJAX?

// メンバーの中の誰か、例えば「友達１」の「チャットする」ボタンを押した時に、モーダルが表示される処理
document.getElementById('apChatButton1').onclick = function() {
    document.getElementById('mgModalContent').style.display = 'block';
}

// モーダルが表示されて、「今はしない」ボタンを押した時に、モーダルが閉じる処理
document.getElementById('apCancelChat').onclick = function() {
    document.getElementById('mgModalContent').style.display = 'none';
}

// モーダルが表示されて、「参加する」ボタンが押された時の処理
document.getElementById('confirmChat').onclick = function() {
    // チャット開始の処理をここに追加
    document.getElementById('chatModal').style.display = 'none';
}