class Querier {
	queriesList = [];
	selectedOption = {};
	queryResponse = {};

	constructor() {
		console.log('Init Querier');
	}

	generateSelectOptions() {
		return this.queriesList.map((option) => {
			return `<option class="select-option" id=${option.id}>${option.name}</option>`;
		});
	}

	generateParamInputs (params) {
		return params.map((param, index) => {
			return `<div class="input-field">
				<label class="param-label" for="param1">${param}</label>
				<input id="input-${index}" name="${param}" class="param-input" required/>
			</div>`;
		});
	}
		
	generateResponseGrid () {
		let titleList = this.queryResponse.displayTitle.split(';'), rowContent;
		titleList = titleList.map(title => `<th>${title}</th>`);
		let dataList = this.queryResponse.data.map((row) => {
			rowContent = row.map(item => `<td>${item}</td>`);
			return `<tr>${rowContent}</tr>`
		});

		return [titleList, dataList];
	}

	fetchParameters (value) {
		this.selectedOption = this.queriesList.find((option) => {
			return option.name === value;
		});
		const params = this.selectedOption.params.split(';')
		return this.generateParamInputs(params);
	}

	fetchQueryResponse (params) {
		let self = this;
		return new Promise((resolve, reject) => {
			const queryId = self.selectedOption.id;
			$.post(`/api/executeQuery/${queryId}`, params, function(response) {
				const parsedResponse = JSON.parse(response);
				self.queryResponse = parsedResponse.result;
				resolve(self.generateResponseGrid());
			});
		})
	}

	fetchQueriesList () {
		let self = this;
		return new Promise((resolve, reject) => {
			$.get('/api/getQueriesList', function(response) {
				const parsedResponse = JSON.parse(response);
				self.queriesList = parsedResponse.queries;
				resolve(self.generateSelectOptions());
			});
		});
	}
}

const querier = new Querier();

$(document).ready(function() {
	querier.fetchQueriesList().then((queriesList) => {
		$('select#querySelector').html('').append(queriesList);
		$('select#querySelector').trigger('change');
	});
});

$('select#querySelector').on('change', function(event) {
	$('.display-section').addClass('hide');
	const paramList = querier.fetchParameters(event.target.value);
	$('#paramsSection').html('').append(paramList);
});

$('#querierForm').on('submit', function(event) {
	event.preventDefault();
	const paramVal = $(this).serializeArray();
	$('#responseGrid').html('');
	querier.fetchQueryResponse(paramVal).then((queryResponse) => {
		$('.display-section').removeClass('hide');
		queryResponse.forEach(element => $('#responseGrid').append(element));
	});
	return false;
});
