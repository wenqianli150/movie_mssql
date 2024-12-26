// globals to be updated after file upload
var data = null;
var name = null;
var file = null;

// Hide the following HTML elements when page (HTML body) loads in browser. 
function initElements() {
    dropDownActors();
    dropDownGenres();
    dropDownRatings();
    getFavorites();
    queryMovieDB();
}


function dropDownActors() {

    $ ("#loader").show();
    $ ("#select_actor").hide();


    var json_data = {};
    $.ajax({
        url:"http://127.0.0.1:8000/api/actors",
        type: "GET",
        contentType: 'application/json',
        data: JSON.stringify(json_data),
    })

    .done(function (json_response) {
        for (var i = 0; i < json_response.length; i++){
            var actor = $("<option>");
            actor.text(json_response[i][0]);
            $("#actor_id").append(actor);
        }
        $ ("#select_actor").show();
        $ ("#loader").hide();
    })

    .fail(function () {
        alert("server error");
    })
}


function dropDownGenres() {

    $ ("#loader").show();
    $ ("#select_genre").hide();


    var json_data = {};
    $.ajax({
        url:"http://127.0.0.1:8000/api/genres",
        type: "GET",
        contentType: 'application/json',
        data: JSON.stringify(json_data),
    })

    .done(function (json_response) {
        for (var i = 0; i < json_response.length; i++){
            var genre = $("<option>");
            genre.text(json_response[i][0]);
            $("#genre_id").append(genre);
        }
        $ ("#select_genre").show();
        $ ("#loader").hide();
    })

    .fail(function () {
        alert("server error");
    })
}


function dropDownRatings() {

    $ ("#loader").show();
    $ ("#select_rating").hide();


    var json_data = {};
    $.ajax({
        url:"http://127.0.0.1:8000/api/ratings",
        type: "GET",
        contentType: 'application/json',
        data: JSON.stringify(json_data),
    })

    .done(function (json_response) {
        for (var i = 0; i < json_response.length; i++){
            var rating = $("<option>");
            rating.text(json_response[i][0]);
            $("#rating_id").append(rating);
        }
        $ ("#select_rating").show();
        $ ("#loader").hide();
    })

    .fail(function () {
        alert("server error");
    })
}


function favoriteMovie(index) {

    $.ajax({
        url:"http://127.0.0.1:8000/api/favorite_movie?id=" + index,
        beforeSend: function(dummy) { $ ("#loader").show(); },
        complete: function(dummy) { $ ("#loader").hide(); },
        type: "PUT",
    })
        .done(function (json_response) {
            var [index, title, country, duration, year, rating] = json_response;
            if (!($('favTable').find('#' + index).length > 0)) {
                $("#favTable").find('tbody')
                    .append($('<tr>')
                        .append($('<td>')
                            .append(title))
                        .append($('<td>')
                            .text(country))
                        .append($('<td>')
                            .text(duration))
                        .append($('<td>')
                            .text(year))
                        .append($('<td>')
                            .text(rating))
                        .append($('<td>')
                                .append($("<button class=\"btn btn-primary\">🗑</button>")
                                    .attr('onClick', 'unfavoriteMovie(' + index + ')')))
                        .attr('id', index)
                    );
                }
        })
        .fail(function () {
            alert("server error");
        })

}


function unfavoriteMovie(index) {

    $.ajax({
        url:"http://127.0.0.1:8000/api/unfavorite_movie?id=" + index,
        beforeSend: function(dummy) { $ ("#loader").show(); },
        complete: function(dummy) { $ ("#loader").hide(); },
        type: "PUT",
    })
        .done(function (json_response) {
            $("#favTable").find('tbody')  // remove data on frontend 
                .find("tr[id=" + index + "]").remove();
        })
        .fail(function () {
            alert("server error");
        })
}


function getFavorites() {
    $ ("#favInfo").hide();
    $ ("#favTable tbody tr").remove();

    $.ajax({
        url:"http://127.0.0.1:8000/api/favorites",
        beforeSend: function(dummy) { $ ("#loader").show(); },
        complete: function(dummy) { $ ("#loader").hide(); },
        type: "GET",
    })
        .done(function (json_response) {
            $ ("#favInfo").show(); // build the table with provided info
            for (const [index, title, country, duration, year, rating] of json_response) {
                $("#favTable").find('tbody')
                    .append($('<tr>')
                        .append($('<td>')
                            .append(title))
                        .append($('<td>')
                            .text(country))
                        .append($('<td>')
                            .text(duration))
                        .append($('<td>')
                            .text(year))
                        .append($('<td>')
                            .text(rating))
                        .append($('<td>')
                                .append($("<button class=\"btn btn-primary\">🗑</button>")
                                    .attr('onClick', 'unfavoriteMovie(' + index + ')')))
                        .attr('id', index)
                );
            }

            if (json_response.length == 0) {
                $ ("#favInfo").hide();
            }
        })

        .fail(function () {
            alert("server error");
        })
}

function queryMovieDB() {
    $ ("#movieInfo").hide();
    $ ("#movieTable tbody tr").remove();

    var actor = $ ("#actor_id").val();
    var genre = $ ("#genre_id").val();
    var rating = $ ("#rating_id").val();

    $.ajax({
        url:"http://127.0.0.1:8000/api/query",
        data: {
            actor: actor,
            genre: genre,
            rating: rating
        },
        beforeSend: function(dummy) { $ ("#loader").show(); },
        complete: function(dummy) { $ ("#loader").hide(); },
        type: "GET",
    })
        .done(function (json_response) {
            $ ("#movieInfo").show(); // build the table with provided info
            for (const [index, title, country, duration, year, rating] of json_response) {
                $("#movieTable").find('tbody')
                    .append($('<tr>')
                        .append($('<td>')
                            .append(title))
                        .append($('<td>')
                            .text(country))
                        .append($('<td>')
                            .text(duration))
                        .append($('<td>')
                            .text(year))
                        .append($('<td>')
                            .text(rating))
                        .append($('<td>')
                            .append($("<button class=\"btn btn-outline-warning\">★</button>")
                                .attr('id', index)
                                .attr('onClick', 'favoriteMovie(' + index + ')')))
                );
            }
        })

        .fail(function () {
            alert("server error");
        })
}


// callback functions
$(function() {

    // an actor was selected
    $('#actor_id').change(function () {
        queryMovieDB();
    })

    // an genre was selected
    $('#genre_id').change(function () {
        queryMovieDB();
    })

    // a rating was selected
    $('#rating_id').change(function () {
        queryMovieDB();
    })
});