document.ready(function () {
	const amenities = {};
	$("li input[type=checkbox]").change(function () {
		if (this.checked) {
			amenities[this.dataset.name] = this.dataset.id;
		} else {
			delete amenities[this.dataset.name];
		}
		$(".amenities h4").text(Object.keys(amenities).sort().join(", "));
	});

});

const apiStatusDiv = document.getElementById('api_status');
function checkApiStatus()
{
    fetch('http://0.0.0.0:5001/api/v1/status/')
    .then(response =>response.json)
    .then(data =>{
        if (data.status == 'OK'){
            apiStatusDiv.classList.add('available');
        }
        else{
            apiStatusDiv.classList.remove('available');
        }
    })
    .catch(error => {
        console.error("Error Fertching API", error);
        apiStatusDiv.classList.remove('available')
    })
}