$(document).ready(function () {
        //Karritora gehitu
        $("[name='plus']").on('click',function(e) {
            e.preventDefault()
            product_id = $(this).attr("id")
            //Unitate kopurua aldatzeko
            container_unit = $(this).parent()
            //Prezioa aldatzeko
            container_main = $(this).parent().parent()
            prezioa_txt = container_main.find('.saskiaprezioa').text()


            $.ajax({
                type:'POST',
                url: "{% url 'unitateak_aldatu' %}",
                data:{
                    aldatu : "gehitu",
                    product_id: product_id,
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                }, // Pass datuak directly as the data
                success: function (response) {
                    //Unitateak aldatu
                    container_unit.find('.unitateak').text(response[0].kantitatea)
                    //Prezioa aldatu
                    prezio_finala = parseFloat(prezioa_txt)
                    prezio_finala += response[0].prezioa
                    prezio_finala = prezio_finala.toFixed(2)
                    container_main.find('.saskiaprezioa').text(prezio_finala + "€")
                    //Guztira aldatzeko
                    guztira = $("#guztira").text()
                    guztira = parseFloat(guztira)
                    guztira += response[0].prezioa
                    guztira = guztira.toFixed(2)
                    guztira = $("#guztira").text(guztira + "€")
                }, error: function (response) {

                }
            })
        })

        //Karritotik kendu
        $("[name='minus']").on('click',function(e) {
            e.preventDefault()
            product_id = $(this).attr("id")
            //Unitate kopurua aldatzeko
            container_unit = $(this).parent()
            //Prezioa aldatzeko
            container_main = $(this).parent().parent()
            prezioa_txt = container_main.find('.saskiaprezioa').text()
            $.ajax({
                type:'POST',
                url: "{% url 'unitateak_aldatu' %}",
                data:{
                    aldatu : "kendu",
                    product_id: product_id,
                    csrfmiddlewaretoken: '{{ csrf_token }}'
                }, // Pass datuak directly as the data
                success: function (response) {
                    //Unitateak aldatu
                    container_unit.find('.unitateak').text(response[0].kantitatea)
                    //Prezioa aldatu
                    prezio_finala = parseFloat(prezioa_txt)
                    prezio_finala -= response[0].prezioa
                    prezio_finala = prezio_finala.toFixed(2)
                    container_main.find('.saskiaprezioa').text(prezio_finala + "€")
                    //Guztira aldatzeko
                    guztira = $("#guztira").text()
                    guztira = parseFloat(guztira)
                    guztira -= response[0].prezioa
                    guztira = guztira.toFixed(2)
                    guztira = $("#guztira").text(guztira + "€")
                }, error: function (response) {

                }
            })
        })

        //Karritotik ezabatu
        $(".delete").on('click',function(e) {
                e.preventDefault()
                var item_id = $(this).attr("id")
                container = $(this).parent().parent()
                $.ajax({
                    type:'POST',
                    url: "{% url 'saskitik_ezabatu' %}",
                    data:{
                        item_id : item_id,
                        csrfmiddlewaretoken: '{{ csrf_token }}'
                    }, // Pass datuak directly as the data
                    success: function(response){
                        container.remove()
                        guztira = $("#guztira").text( "0.00€")
                    },error: function (response) {

                    }
                })
            })

    })