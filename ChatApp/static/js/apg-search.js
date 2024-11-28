const searchInput = document.getElementById('search-input'); // 検索フォームに入力された値を取得
const searchTargets = document.querySelectorAll('.search-target'); // 検索対象の要素全てを取得

// 検索結果を表示する関数
function showSearchResult(target) {
  target.style.display = 'block';
}

// 検索結果を非表示にする関数
function hideSearchResult(target) {
  target.style.display = 'none';
}

// 検索結果をフィルタリングする関数
function filterSearchResults() {
  const keyword = searchInput.value.trim().toLowerCase(); // 入力されたキーワードを取得し、前後空白の削除、小文字に変換して定義
  searchTargets.forEach((target) => { // 各検索要素に対して処理を実行
    const text = target.textContent.toLowerCase(); //要素のテキストを小文字に変換
    if (text.includes(keyword)) { // テキストがキーワードを含むかどうか、キーワードと合致するか？を判定
      showSearchResult(target); // 含む場合は表示
    } else {
      hideSearchResult(target); // 含まない場合は非表示
    }
  });
}

// 検索フォームに入力があった時に、filterSearchResults関数を呼び出す
searchInput.addEventListener('input', filterSearchResults);