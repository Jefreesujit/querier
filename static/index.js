
class Querier {
    queriesList = [];
		selectedOption = {};
		queryResponse = {};

    constructor() {}

    generateSelectOptions(response) {
        return response.map((option) => {
            return `<option class="select-option" id=${option.id}>${option.name}</option>`;
        });
    }

    generateParamInputs (params) {
        return params.map((param, index) => {
            return `<div class="input-field">
                <label class="param-label" for="param1">${param}</label>
                <input id="${param}" class="param-input" required/>
            </div>`;
        });
		}
		
		generateResponseGrid (queryResponse) {
			return queryResponse;
		}

    fetchParameters (id) {
        this.selectedOption = this.queriesList.find((option) => {
            return option.id === id;
        });
        return this.generateParamInputs(this.selectedOption.params);
		}
		
		fetchQueryResponse (params) {
			return new Promise((resolve, reject) => {
				$.post('/api/executeQuery', params, function(response) {
					this.queryResponse = response;
					this.generateResponseGrid(queryResponse)
				});
			})
		}

    fetchQueriesList () {
        return new Promise((resolve, reject) => {
            $.get('/api/getQueriesList', function(response) {
                console.log(response);
                this.queriesList = response;  
                resolve(this.generateSelectOptions(response));
            });
        });
    }
}

$('select#querySelector').on('change', function(event) {
		$('#responseGrid').html('');
		const paramList = querier.fetchParameters(event.target.id);
		$('#paramsSection').html('').append(queriesList);
});

$('#querierForm').on('submit', function(event) {
    const paramVal = this.form.serialize();
    querier.fetchQueryResponse(paraVal).then((queryResponse) => {
				console.log(queryResponse);
    });
});

$(document).ready(function() {
    const querier = new Querier();
    querier.fetchQueriesList().then((queriesList) => {
        $('select#querySelector').html('').append(queriesList);
    });
});
