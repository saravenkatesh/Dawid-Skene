$(document).ready(function() {
  // set default parameters
  if(typeof gParameters == "undefined") { gParameters = new Object(); }
  defaultPrm = {
    imageIds: [882380, 882384, 882385],
    submitURL: "http://www.mturk.com/mturk/externalSubmit",
    assignment_id: 'ID', //'ASSIGNMENT_ID_NOT_AVAILABLE',
    excludeWorkers: [],
    welcomeText: '{{welcomeText}}',
    welcomeTraining: 'If this is the first time you try a HIT of this kind, then you must complete a brief training session before you start working. The training session should take about 5-10 minutes. If you complete the training and at least two HITs, you will receive a bonus of $1.',
    sideInstructions: '{{sideInstructions}}',
    trainingInstructions: '{{trainingInstructions}}',
    trainingImage: 'http://vision.caltech.edu/~welinder/mturk/corals/synthetic2/EX-2-003-arrow.jpg',
    trainingQuestion: '{{trainingQuestion}}',
    posText: '{{posText}}',
    negText: '{{negText}}',
    postTrainFeedback: '{{postTrainFeedback}}',
    examplesBaseUrl: "http://vision.caltech.edu/~welinder/mturk/corals/synthetic2/",
    examplesExt: 'jpg',
    examplesPosSuffix: "-arrow",
    examples: [
      ['EX-1-001',0],
      ['EX-2-001',1],
      ['EX-2-002',1],
      ['EX-1-002',0],
      ['EX-2-003',1],
      ['EX-1-003',0]],
    exampleChoices: [(“Hindi”, “Hindi.jpg”), (“Punjabi”, “Punjabi.jpg”), (“Tamil, “Tamil.jpg”), (“Malayalam”, “Malayalam.jpg”), (“Kannada”, “Kannada.jpg”), (“Telugu”, “Telugu.jpg”)],
    showRewardFeedback: 0,
    showBinaryRewardFeedback: 0,
    showScore: 0,
    rewardMatrix: [[5, -5], [-10, 10]],
    choices: [(“Hindi”, “Hindi.jpg”), (“Punjabi”, “Punjabi.jpg”), (“Tamil, “Tamil.jpg”), (“Malayalam”, “Malayalam.jpg”), (“Kannada”, “Kannada.jpg”), (“Telugu”, “Telugu.jpg”)]
  }
  for(key in defaultPrm) {
   if(gParameters[key] == undefined) { gParameters[key] = defaultPrm[key]; }
  }
  // determine no. of images
  prm = gParameters; numIm = prm.imageIds.length;
  // exclude workers in list
  var urlParams = {};
  (function () {
      var e,
          a = /\+/g,  // Regex for replacing addition symbol with a space
          r = /([^&=]+)=?([^&]*)/g,
          d = function (s) { return decodeURIComponent(s.replace(a, " ")); },
          q = window.location.search.substring(1);

      while (e = r.exec(q))
         urlParams[d(e[1])] = d(e[2]);
  })();
  if($.inArray(urlParams['workerId'], prm.excludeWorkers) >= 0) {
    $('.view').hide();
    $('#exclude-workers').show();
    return;
  }
  // training data
  var trainRecord = { 'views' : {}};
  var trainScore = [];
  // set up welcome
  $('#welcome-text').append(prm.welcomeText);
  $('#welcome-train').append(prm.welcomeTraining);
  // setup work view
  var hasStartedWorking = 0;
  function setupWorkView() {
    hasStartedWorking = 1;
    $('.view').hide();
    // add warning if no assignment id
    if(prm.assignment_id == "ASSIGNMENT_ID_NOT_AVAILABLE") {
      $('#preview-filter').show();
      return;
    }
    $('#work-screen').show();
    $('#work-nav').show();
    $('#max-images').html(numIm);
    $('#prev-image').click(function() {
      switchImage(-1);
    });
    // replace top and side instructions
    $('#side-instructions').html(prm.sideInstructions);
    // setup choices
    function createChoiceCallback(index) {
      return function() {
        commitAnswer(index);
      }
    }
    for(var i=0; i<prm.choices.length; i++) {
      var c = prm.choices.length-i;
      $('#choices').append('<button id="choice-'+c+'" STYLE=”background-image:’+prm.choices[i][1]+’”/></button>');
      $('#choice-'+c).button().click(createChoiceCallback(c));
    }
    switchImage(1);
    // set up masking overlay
    $('#choices-saving').height($('#choices').height());
    $('#choices-saving').width($('#choices').width());
    $('#choices-saving').hide();
    // save training info
    var d = new Date();
    trainRecord['end'] = d.getTime();
    saveTrainRecord();
  }
  $('#start-training').click(showTrainingIntro);
  $('#start-work').click(setupWorkView);
  function resumeWork() {
    $('.view').hide();
    $('#work-screen').show();
    $('#work-nav').show();
    // save training info
    var d = new Date();
    trainRecord['resume'] = d.getTime();
    saveTrainRecord();
  }
  $('#view-examples').click(showTrainingIntro);
  // switches the image
  var currentImage = -1;
  var startTime = 0;
  var switchImage = function(step) {
      currentImage += step;
      if(currentImage>0) {
        $('#prev-image').show();
      } else {
        $('#prev-image').hide();
      }
      if(currentImage >= prm.imageIds.length) {
          // reached end of task
          $('#work-screen').hide();
          $('#work-nav').hide();
          $('#end-screen').show();
          return;
      }
      var d = new Date(); startTime = d.getTime();
      var id = prm.imageIds[currentImage];
      // set image
      var url = 'http://s3.amazonaws.com/visipedia/images/'+id+'/original.jpg';
      $('#work-screen .image-cell img').fadeTo(500, 0)
      $('#work-screen .image-cell').empty().append('<img src="'+url+'" style="display:none"/>');
      $('#work-screen .image-cell img').fadeTo(500, 1.0);
      // set navigation
      $('#current-image').html(currentImage+1);
  };
  // add browser info
  $('#mturk-form').attr('action', prm.submitURL)
  $('#assignmentId').attr('value', prm.assignment_id);
  $('#browser_name').attr('value', navigator.appName);
  $('#browser_version').attr('value', navigator.appVersion);
  $('#user_agent').attr('value', navigator.userAgent);
  $('#screen_width').attr('value', screen.width);
  $('#screen_height').attr('value', screen.height);
  // set up confidence buttons
  var commitAnswer = function(score) {
      var id = prm.imageIds[currentImage];
      var answer = { 'value': score };
      answer['startTime'] = startTime;
      var d = new Date(); answer['endTime'] = d.getTime();
      var fieldDiv = $('#field-'+id);
      if(fieldDiv.length==0) {
        $('#mturk-form').append('<input type="hidden" name="image['+id+']" value="" id="field-'+id+'"/>');
      }
      $('#field-'+id).val(JSON.stringify(answer));
      // animate saving so that user doesn't double-click
      $('#choices-saving').fadeIn(200).fadeOut(1500);
      // show next image
      switchImage(1);
  };
  // setup the training intro screen
  $('#training-instructions').html(prm.trainingIntructions);
  $('#train-intro-screen .image-cell').append('<img src="'+prm.trainingImage+'"/>');
  function showTrainingIntro() {
    $('.view').hide();
    $('#train-intro-screen').show();
    var d = new Date();
    trainRecord['start'] = d.getTime();
    preloadExamples();
  }
  $('#start-view-examples').click(startViewExamples);
  // setup the training examples screen
  function startViewExamples() {
    $('.view').hide();
    $('#train-example-screen').show();
    $('#example-nav').show();
    if(prm.showScore) {
      $('#score-display').show();
    }
    // setup choices
    function createExChoiceCallback(index) {
      return function() {
        commitExAnswer(index);
      }
    }
    for(var i=0; i<prm.exampleChoices.length; i++) {
      var c = prm.exampleChoices.length-i;
      $('#example-choices').append('<button id="ex-choice-'+c+'">'+prm.exampleChoices[i]+'</button>');
      $('#ex-choice-'+c).button().click(createExChoiceCallback(c));
    }
    // start on first example
    viewExample(0);
  }
  $('#resume-work').click(resumeWork);
  var numExamples = prm.examples.length;
  $('#max-example').html(numExamples);
  $('#prev-example').click(function() { viewExample(-1); });
  var exampleIndex = -1;
  function viewExample(step) {
    $('#answer-incorrect').hide();
    $('#answer-correct').hide();
    $('#reward-feedback').hide();
    if(hasStartedWorking) {
      $('#resume-work').show();
    } else {
      $('#resume-work').hide();
    }
    // determine step direction
    if(step == 0) {
      exampleIndex = 0;
    } else {
      exampleIndex += step;
    }
    if(exampleIndex == numExamples) {
      // reached end
      showTrainingEnd();
      return;
    }
    // set navigation
    if(exampleIndex>0) {
      $('#prev-example').show();
    } else {
      $('#prev-example').hide();
    }
    $('#current-example').html(exampleIndex+1);
    // show question and image
    $('#example-text').html(prm.trainingQuestion);
    var url = exampleUrl(prm.examples[exampleIndex][0]);
    $('#train-example-screen .image-cell img').fadeTo(100, 0);
    $('#train-example-screen .image-cell').empty().append('<img src="'+url+'" style="display:none;"/>');
    $('#train-example-screen .image-cell img').fadeTo(500, 1);
    $('#next-example').hide().unbind('click').bind('click', function() {
      var d = new Date();
      trainRecord['views'][exampleIndex]['e'] = d.getTime();
      viewExample(1);
    });
    $('#example-choices').show();
    // record viewing
    var d = new Date();
    trainRecord['views'][exampleIndex] = {'s' : d.getTime()};
  }
  // commit an example answer
  function commitExAnswer(ans) {
    if(prm.examples[exampleIndex][1] == 1) {
      // positive example
      if(prm.examples[exampleIndex][1]) {
        var posImgUrl = exampleUrl(prm.examples[exampleIndex][0],1);
        $('#train-example-screen .image-cell').fadeTo(100, 0);
        $('#train-example-screen .image-cell').empty()
          .append('<img src="'+posImgUrl+'"/>');
        $('#train-example-screen .image-cell').fadeTo(500, 1);
      }
      $('#example-text').html(prm.posText);
    } else {
      $('#train-example-screen .image-cell img').fadeTo(100, 0).fadeTo(500, 1);
      $('#example-text').html(prm.negText);
    }
    // show correct/incorrect answer
    if(prm.showRewardFeedback) {
      var gt = prm.examples[exampleIndex][1];
      var reward = prm.rewardMatrix[gt][ans-1];
      trainScore[exampleIndex] = reward;
      var totalScore = computeScore();
      var answerText = prm.exampleChoices[prm.exampleChoices.length-ans];
      $('#reward-feedback').show();
      $('#your-answer').html('You answered "'+answerText+'", so you get score:');
      $('#your-score').html(reward);
      $('#your-total-score').html('Your total score so far is '+totalScore+'.');
      $('#score').html(totalScore);
    } else if(prm.showBinaryRewardFeedback) {
      if((ans-1) === prm.examples[exampleIndex][1]) {
        $('#answer-correct').show();
      } else {
        $('#answer-incorrect').show();
      }
    }
    // show navigation
    $('#example-choices').hide();
    $('#next-example').show();
  }
  function computeScore() {
    var i=0, score=0;
    for(i=0; i<trainScore.length; i++) {
      if(trainScore[i] !== undefined) {
        score += trainScore[i];
      }
    }
    return score;
  }
  // training end screen
  $('#post-train-feedback').html(prm.postTrainFeedback);
  $('#start-work-after-train').click(setupWorkView);
  $('#resume-work-after-train').click(resumeWork);
  function showTrainingEnd() {
    $('.view').hide();
    $('#train-done-screen').show();
    if(hasStartedWorking) {
      $('#resume-work-after-train').show();
      $('#start-work-after-train').hide();
    } else {
      $('#resume-work-after-train').hide();
      $('#start-work-after-train').show();
    }
  }
  function saveTrainRecord() {
    $('#training').val(JSON.stringify(trainRecord));
  }
  // final screen
  $('#feedback-button').click(function() {
    $('#feedback-button').hide();
    $('#feedback-wrapper').show("blind");
  });
  $('#submit').click(function() {
    $('#feedback').val($("#feedback-field").val());
    $('#mturk-form').submit();
  });
  // set button styles
  $('button').button();
  // preload images
  for(var i=0; i<prm.imageIds.length; i++) {
    var id = prm.imageIds[i];
    var url = 'http://s3.amazonaws.com/visipedia/images/'+id+'/original.jpg';
    var img = new Image();
    img.src = url;
  }
  // preload examples
  function exampleUrl(name, isGt) {
    if(isGt) {
      return prm.examplesBaseUrl + name + prm.examplesPosSuffix + '.' + prm.examplesExt;
    } else {
      return prm.examplesBaseUrl + name + '.' + prm.examplesExt;
    }
  }
  function preloadExamples() {
    for(var i=0; i<prm.examples.length; i++) {
      var img = new Image();
      img.src = exampleUrl(prm.examples[i][0]);
      if(prm.examples[i][1]) {
        var img2 = new Image();
        img2.src = exampleUrl(prm.examples[i][0],1);
      }
    }
  }
});
