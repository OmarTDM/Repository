

<!DOCTYPE html>
<html lang="en">
<head>
  <link rel="stylesheet" href="styles.css">
  <style>
    li{
      margin: 10px;
      font-size: 1.3rem;
    }
    a{
      color: #fff;
      text-decoration: none;
    }
  </style>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <div class="endForm">
  <form action="database.php" method="POST" id="endForm">
    <div class="top">
    <div id="advies">

    </div>
    <button><a href="index.html">Terug naar start</a></button>
  </form>
</body>
<script>
const adviesEl = document.getElementById('advies');

  updateAdvies();

function updateAdvies(){
  var score = localStorage.getItem('score');
  if(score === 5){
    adviesEl.innerHTML = `<li>Optimaliseer gegevensprocessen en automatiseer routinematige taken.</li>
<li>Maak gebruik van big data-technologieën en geavanceerde algoritmen.</li>
<li>Blijf op de hoogte van opkomende trends in datatechnologieën en pas deze toe om concurrentievoordeel te behalen.</li>
`  }else if(score === 4){
  adviesEl.innerHTML = `<li>Cultiveer een organisatiecultuur waarin gegevens een centrale rol spelen bij besluitvorming.</li>
<li>Stel gegevensanalyse en rapportage beschikbaar voor alle relevante teams.</li>
<li>Voer voorspellende analyses en machine learning toe voor strategische inzichten.</li>
`  }else if(score === 3){
  adviesEl.innerHTML = `<li>Investeer in gegevenskwaliteit en beheer om betrouwbare resultaten te garanderen.</li>
<li>Pas datagedreven besluitvorming toe in uw bedrijfsstrategie.</li>
<li>Gebruik geavanceerde analysehulpmiddelen en -technieken om diepgaand inzicht te krijgen.</li>
`  }else if(score === 2){
    adviesEl.innerHTML = `<li>Zorg voor gegevensbeveiliging en privacybewustzijn.</li>
<li>Implementeer eenvoudige analyses om trends en patronen te ontdekken.</li>
<li>Breid uw gegevensverzameling uit om meer inzicht te krijgen in uw processen en klanten.</li>
`  }else{
    adviesEl.innerHTML = `<li>Leer de basisprincipes van dataverzameling en -opslag.</li>
<li>Organiseer uw gegevens in eenvoudige spreadsheets of databases..</li>
<li>Begin met het verzamelen van relevante gegevens over uw bedrijfsactiviteiten.</li>
`
  }
}


</script>
</html>