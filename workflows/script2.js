const loadbar = document.getElementById('load-bar');

updateLoadbar()

function updateLoadbar(){
  var score = localStorage.getItem('score');
  loadbar.innerHTML =`<h2>Uw datavolwassenheid bedraagt ${score}%</h2>
  <div class="load-bar">
    <span id="bar"></span>
  </div>`
}

