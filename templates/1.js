function fetchData() {
  fetch('https://api.yotpo.com/products/ml6evbhrou7n2idnijlsQBs6zC5Okr4uo0Exk8SS/{{product.id}}/bottomline').then(response => {
        return response.json();
    })
    .then(data => {
        console.log(data.response.bottomline.total_reviews);
       
        if (data.response.bottomline.total_reviews >= 1) {
          var newNode = document.createElement('div');
          newNode.className = 'yotpo bottomLine';
          document.getElementById('ytpID-{{product.id}}').appendChild(newNode);
          document.getElementsByClassName('yotpo bottomLine')[0].setAttribute('data-product-id', '{{product.id}}');
          yotpo.refreshWidgets();
      }else{
          var newNode = document.createElement('div');
          newNode.className = 'yotpo-bottomline pull-left star-clickable';
          var emptyStars = '<div class="yotpo-bottomline pull-left star-clickable">'
                           +'<div class="standalone-bottomline">'
                           +'<div class="yotpo-bottomline pull-left star-clickable">'
                           +'<span class="yotpo-stars">'
                           +'<span class="yotpo-icon yotpo-icon-empty-star pull-left"></span>'
                           +'<span class="yotpo-icon yotpo-icon-empty-star pull-left"></span>'
                           +'<span class="yotpo-icon yotpo-icon-empty-star pull-left"></span>'
                           +'<span class="yotpo-icon yotpo-icon-empty-star pull-left"></span>'
                           +'<span class="yotpo-icon yotpo-icon-empty-star pull-left"></span></span>'
                           +'<div class="yotpo-clr"></div></div></div>';
          
          document.getElementById('ytpID-{{product.id}}').appendChild(newNode);                      
          document.getElementsByClassName('yotpo-bottomline pull-left star-clickable').innerHTML = emptyStars;
          yotpo.refreshWidgets();
      } 
    })
    .catch(error => {
        console.log("working");
    });
}

      fetchData();



