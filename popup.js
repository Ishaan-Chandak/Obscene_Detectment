chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
  var url = tabs[0].url;
  document.getElementById("url").textContent = url;
});
