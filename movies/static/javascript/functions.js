function rateMovie()
{
    document.getElementById("star-form").submit();
}


function follow(username)
{
    let url = "{% url 'follow' username=0 %}".replace('0', username);
    var followElement = $("#follow");

    if (followElement.text()=='Follow'){
            followElement.text('Unfollow');
        
    } else {
            followElement.text('Follow');
    }

    $.ajax({
        type: "GET",
        url: url,
        success: () => {},
    });
}

function reviewLike(reviewId)
{
    let url = "{% url 'review_like' review_id=0 %}".replace('0', reviewId);
    var likeElement = $("#like-" + reviewId);
    var likeCount = $("#like-count-" + reviewId);
    var likeCountEl = likeCount.text().split(" ");

    if (likeElement.text().substring(0,5)=='Liked'){
            likeElement.text('Like ');
            likeElement.css("color", "white");
            likeElement.append('<i class="fa fa-heart" style="font-size: 10px;"></i>');
            likeCount.text(" cnt likes".replace('cnt', parseInt(likeCountEl[1])-1));
    } else {
            likeElement.text('Liked ');
            likeElement.css("color", "rgb(215, 139, 201)");
            likeElement.append('<i class="fa fa-heart" style="font-size: 10px;"></i>');
            likeCount.text(" cnt likes".replace('cnt', parseInt(likeCountEl[1])+1));
    }

    $.ajax({
        type: "GET",
        url: url,
        success: () => {},
    });
}

function openForm(formId) {
    document.getElementById(formId).style.display = "block";
}

function closeForm(formId) {
    document.getElementById(formId).style.display = "none";
}

function reviewDelete(reviewId)
{
    let url = "{% url 'review_delete' review_id=0 %}".replace('0', reviewId);
    document.getElementById('review-'+reviewId).style.display = "none";

    $.ajax({
        type: "GET",
        url: url,
        success: function(data) {
            alert("Deleted successfully");
        },
        error: function(data) {
            alert("Error");
        }
    });
}

function reviewEdit(reviewId)
{
    event.preventDefault();
    var form = $("#editform-"+ reviewId);
    let url = "{% url 'review_edit' review_id=0 %}".replace('0', reviewId);
    var popUp = document.getElementById("edit-"+reviewId).style.display = "none";
    var new_text = decodeURI(form.serialize().split("=")[2]);

    if (new_text.length == 0){
        return;
    }

    var p = document.getElementById("review-text-"+reviewId);
    p.innerHTML = new_text;

    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(),
        success: () => {},
    });
}

$("#watchlist").on("click", function (e) {

    e.preventDefault();
    let movie_id  = $(this).val();
    var el = document.getElementById("watchlist");

    if (el.style.color == "white"){
        el.style.color = 'rgb(' + 215 + ',' + 139 + ',' + 201 + ')';
    } else {
        el.style.color = "white";
    }

    let url = "{% url 'movie_to_watchlist' movie_id=0 %}".replace('0', movie_id);
    $.ajax({
        type: "GET",
        url: url,
        success: function () {
        }
    });
});

$("#like-movie").on("click", function (e) {

    e.preventDefault();
    let movie_id  = $(this).val();
    var el = document.getElementById("like-movie");

    if (el.style.color == "white"){
        el.style.color = 'rgb(' + 215 + ',' + 139 + ',' + 201 + ')';
    } else {
        el.style.color = "white";
    }

    let url = "{% url 'like_movie' movie_id=0 %}".replace('0', movie_id);
    $.ajax({
        type: "GET",
        url: url,
        success: function () {
        }
    });
});

$("#watched").on("click", function (e) {

    e.preventDefault();
    let movie_id  = $(this).val();
    var el = document.getElementById("watched");

    if (el.style.color == "white"){
        el.style.color = 'rgb(' + 215 + ',' + 139 + ',' + 201 + ')';
    } else {
        el.style.color = "white";
    }

    let url = "{% url 'movie_to_watched' movie_id=0 %}".replace('0', movie_id);
    $.ajax({
        type: "GET",
        url: url,
        success: function () {
        }
    });
});

function openTab(evt, tabName) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

document.getElementById("defaultOpen").click();