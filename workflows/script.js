const quizData = [
  {
    question: 'In hoeverre zijn gegevens binnen uw organisatie gedocumenteerd en gestructureerd?',
    a: 'Geen documentatie of structuur' , a_v: 'a',
    b: 'Enkele documentatie, weinig structuur', b_v: 'b',
    c: 'Beperkte documentatie, enige structuur', c_v: 'c',
    d: 'Goede documentatie, matige structuur', d_v: 'd',
    e: 'Uitgebreide documentatie, duidelijke structuur', e_v: 'e',
  },
  {
    question: 'Heeft uw organisatie een aangewezen persoon of team dat verantwoordelijk is voor gegevensbeheer?',
    a: 'Geen verantwoordelijke' , a_v: 'a',
    b: 'Informele verantwoordelijke', b_v: 'b',
    c: 'Beperkte verantwoordelijkheid', c_v: 'c',
    d: 'Aangewezen verantwoordelijke', d_v: 'd',
    e: 'Specifiek team voor gegevensbeheer', e_v: 'e',
  },
  {
    question: 'Worden gegevensstandaarden en -richtlijnen regelmatig gecommuniceerd binnen uw organisatie?',
    a: 'Zelden gecommuniceerd' , a_v: 'a',
    b: 'Af en toe gecommuniceerd', b_v: 'b',
    c: 'Soms gecommuniceerd', c_v: 'c',
    d: 'Meestal gecommuniceerd', d_v: 'd',
    e: 'Altijd gecommuniceerd', e_v: 'e',
  },
  {
    question: 'Worden gegevenskwaliteitscontroles uitgevoerd voor belangrijke datasets?',
    a: 'Zelden gecontroleerd' , a_v: 'a',
    b: 'Af en toe gecontroleerd', b_v: 'b',
    c: 'Soms gecontroleerd', c_v: 'c',
    d: 'Meestal gecontroleerd', d_v: 'd',
    e: 'Altijd gecontroleerd', e_v: 'e',
  },
  {
    question: 'Heeft uw organisatie een gegevenscatalogus waarin alle beschikbare datasets worden gedocumenteerd?',
    a: 'Geen gegevenscatalogus' , a_v: 'a',
    b: 'Beperkte catalogus', b_v: 'b',
    c: 'Eenvoudige catalogus', c_v: 'c',
    d: 'Uitgebreide catalogus', d_v: 'd',
    e: 'Uitgebreide catalogus met metagegevens', e_v: 'e',
  },
  {
    question: 'Worden medewerkers getraind in gegevensbeheer en -gebruik?',
    a: 'Geen training' , a_v: 'a',
    b: 'Minimale training', b_v: 'b',
    c: 'Beperkte training', c_v: 'c',
    d: 'Regelmatige training', d_v: 'd',
    e: 'Voortdurende training', e_v: 'e',
  },
  {
    question: 'Worden gegevens regelmatig gecontroleerd op naleving van wettelijke voorschriften (bijv. AVG, HIPAA)?',
    a: 'Zelden gecontroleerd' , a_v: 'a',
    b: 'Af en toe gecontroleerd', b_v: 'b',
    c: 'Soms gecontroleerd', c_v: 'c',
    d: 'Meestal gecontroleerd', d_v: 'd',
    e: 'Altijd gecontroleerd', e_v: 'e',
  },
  {
    question: 'Heeft uw organisatie een gegevensbeveiligingsbeleid en -procedures?',
    a: 'Geen beleid/procedures' , a_v: 'a',
    b: 'Beperkt beleid/procedures', b_v: 'b',
    c: 'Basisbeleid/procedures', c_v: 'c',
    d: 'Goed beleid/procedures', d_v: 'd',
    e: 'Uitgebreid beleid/procedures', e_v: 'e',
  },
  {
    question: 'Worden gegevens actief gebruikt voor strategische besluitvorming en innovatie binnen uw organisatie?',
    a: 'Zelden gebruikt' , a_v: 'a',
    b: 'Af en toe gebruikt', b_v: 'b',
    c: 'Soms gebruikt', c_v: 'c',
    d: 'Meestal gebruikt', d_v: 'd',
    e: 'Voortdurend gebruikt', e_v: 'e',
  },
  {
    question: 'Heeft uw organisatie een data-analysecentrum met toegewijde analisten?',
    a: 'Geen data-analysecentrum' , a_v: 'a',
    b: 'Beperkt data-analysecentrum', b_v: 'b',
    c: 'Basis data-analysecentrum', c_v: 'c',
    d: 'Goed data-analysecentrum', d_v: 'd',
    e: 'Uitgebreid data-analysecentrum', e_v: 'e',
  }
  
  
]
const questionEl = document.getElementById('question');
const quiz = document.getElementById('quiz');
const a_text = document.getElementById('a_text');
const b_text = document.getElementById('b_text');
const c_text = document.getElementById('c_text');
const d_text = document.getElementById('d_text');
const e_text = document.getElementById('e_text');
const submitBtn = document.getElementById('submit');

const answersEls = document.querySelectorAll('.answer');

let currentQuiz = 0;
let answer = undefined;
let score = 0;

loadQuiz();

function loadQuiz(){
  deselectAnswers()
  const currentQuizData = quizData[currentQuiz];
  questionEl.innerHTML = currentQuizData.question;
  a_text.innerText = currentQuizData.a;
  b_text.innerText = currentQuizData.b;
  c_text.innerText = currentQuizData.c;
  d_text.innerText = currentQuizData.d;
  e_text.innerText = currentQuizData.e;
}

function getSelected(){

  let answer = undefined;

  answersEls.forEach((answerEl) => {
    if(answerEl.checked){
      answer = answerEl.id;
    }
  });
  return answer;
}

function deselectAnswers(){
  answersEls.forEach((answerEl) => {
    answerEl.checked =false
    }
)};

submitBtn.addEventListener('click', () => {
  const answer = getSelected(); 
  if(answer){
    if(answer === quizData[currentQuiz].a_v){
      score += 1;
    }
    else if(answer === quizData[currentQuiz].b_v){
      score += 2;
    }
    else if(answer === quizData[currentQuiz].c_v){
      score += 3;
    }
    else if(answer === quizData[currentQuiz].d_v){
      score += 4;
    }
    else if(answer === quizData[currentQuiz].e_v){
      score += 5;
    }
    currentQuiz++;
    if(currentQuiz < quizData.length){
      loadQuiz()}
      else{
        score *= 2;
        localStorage.setItem('score', score);
        if(score > 80){
          window.location.href = 'database-5.php';
        }else if(score > 60){
          window.location.href = 'database-4.php';
        }else if(score > 40){
          window.location.href = 'database-3.php';
        }else if(score > 20){
          window.location.href = 'database-2.php';
        }else {
          window.location.href = 'database-1.php';

        }
      //   quiz.innerHTML = `  <div class="endForm">
      //   <form method="POST" id="endForm">
      //     <div class="top">
      //         <label class="lb" for="">Bedrijfsnaam:</label>
      //         <input class="inp" name="bedrijf" type="text" class="bedrijfsnaam">
      //         <label class="lb" for="">Naam</label>
      //         <input class="inp" name="naam" type="text" class="naam">
      //     </div>
      //     <label class="lb" for="">Email:</label>
      //     <input class="inp" name="email" type="text">
      //     <input id="scoreEl" value="${score}%" name="score" readonly>
      //     <button id="submitForm"  type="submit" name="submit">Submit</button>
      // </form>
      //   <h2>Uw datavolwassenheid bedraagt ${score}%</h2>
      //     <div class="load-bar">
      //       <span id="bar"></span>
      //     </div>
      //   </div>
      //   <script src="script2.js"></script>`;
        const loadBar = document.getElementById('bar');
        // loadBar.style.display = 'flex';
        loadBar.style.width = score + '%';
        }
      }
    }
)

// function endQuiz(){
//   score *= 2;
//   return score;
// }


// function updateScore(score) {
//   scoreEl.value = `${score}%`;
//   console.log('halll');
// }


