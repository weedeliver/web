$(document).ready(function () {
    //Gomendatutako platerak
    $.ajax({
        url: "/gomendioak",
        type: 'GET',
        success: function (data) {
            let produktuenLista = $("#gomendioak");
            produktuenLista.empty();

            data.forEach(function (gomendioa) {
                let imageUrl = gomendioa.image.replace('/web', '');
                let produktuIzena = gomendioa.name;

                produktuenLista.append(
                    '<div class="carouselitem">' +
                    '<img alt="'+ produktuIzena +'" src="' + imageUrl + '">' +
                    '<h4>' + produktuIzena + '</h4>' +
                    '</div>'
                );
            });
        },
        error: function (xhr, status, error) {
            console.log("Error: " + error);
        }
    });
});