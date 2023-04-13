chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  console.log(`requestO: ${request}`)
  if (request.action == "getCurrentUrl") {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      var url = tabs[0].url;
      // console.log(`url: ${url}`)
      fetch('http://localhost:9000/extract_images', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          url: url
        })
      })
      .then(response => response.json())
      .then(data => {
        // Send the extracted image URLs to the Flask API
        console.log("Inside 8000");
        fetch('http://localhost:8000/predict', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            image_urls: data.image_urls
          })
        })
        .then(response => response.json())
        .then(data => {
          console.log(data.predictions);
        })
        .catch(error => {
          console.error(error);
        });
      })
      .catch(error => {
        console.error(error);
      });
      sendResponse({url: url});
    });
    return true;
  }
});
