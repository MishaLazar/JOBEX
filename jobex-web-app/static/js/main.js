$(document).ready( function () {
    $('#positions').DataTable();
} );
$(document).ready(
    function tokenSuccess(tokens) {

    if (tokens.access_token != undefined){
        console.log('successfully updated access token');
        window.localStorage.accessToken = response.access_token;
    }
    if (tokens.refresh_token != undefined){
        console.log('successfully updated refreshtoken')
        window.localStorage.refreshToken = response.refresh_token;
    }
});
