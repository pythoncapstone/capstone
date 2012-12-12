$('#DisplayAllExercises').click(function() {
	$.get('/Exercise/displayAll/', function(data) {
		displayExercises(data)
	});
});

var displayExercises = function(data) {
	$('#Exercises').html(data);
	$('#Exercises').dialog();
	
};

$('.exercise').click(function() {
	var id = $(this).data('exerciseid');
	$.get('/Exercise/load/' + id, function(exercise) {
		loadExercise(exercise);
	});
});

var loadExercise = 	function(exercise) {
	clearAll();
	var userCodeSegment = "#" + exercise.WordProblem;
	userCodeSegment += "\n" + exercise.MethodBody;

	workbenchViewModel.set("userCodeSegment", userCodeSegment);
	workbenchViewModel.loadExpectedResults(exercise.MethodCalls);
	loadEditorText();
	$('#Exercises').dialog('close')

	checkToggleGrid();
};