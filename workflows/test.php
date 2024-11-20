<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="styles.css">
  
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TEST QUICKSCAN</title>
</head>
<body>
  <div class="quiz-container" id="quiz">
    <div class="quiz-header">
      <h2 id="question">Question Txt</h2>
      <ul>
        <li>
          <input type="radio" id="a" name="answer" class="answer">
          <label for="a" id="a_text">Question</label>
        </li>
        <li>
          <input type="radio" id="b" name="answer" class="answer">
          <label for="a" id="b_text">Question</label>
        </li>
        <li>
          <input type="radio" id="c" name="answer" class="answer">
          <label for="a" id="c_text">Question</label>
        </li>
        <li>
          <input type="radio" id="d" name="answer" class="answer">
          <label for="a" id="d_text">Question</label>
        </li>
        <li>
          <input type="radio" id="e" name="answer" class="answer">
          <label for="a" id="e_text">Question</label>
        </li>
      </ul>
    </div>

    <div id="dataContainer"></div>
    <button id="submit">Submit</button>
  </div>
  
  </div>
</body>  
<script src="script.js"></script>
  
</html>