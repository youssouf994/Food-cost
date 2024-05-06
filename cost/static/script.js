$(document).ready(function () {
    const panoramicaContainer = $(".panoramica-container");
    const panoramica = $(".panoramica");
    const prevButton = $(".indietro");
    const nextButton = $(".avanti");

    const itemWidth = 300; // Larghezza di un elemento "prodotto"
    const itemsPerPage = 4; // Numero di elementi da mostrare per pagina
    let currentPage = 1;

    function showPage(page) {
        const startIndex = (page - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;

        const prodotti = $(".prodotto");

        prodotti.each(function (index, element) {
            if (index >= startIndex && index < endIndex) {
                $(element).show();
            } else {
                $(element).hide();
            }
        });
    }

    prevButton.on("click", function () {
        if (currentPage > 1) {
            currentPage--;
            showPage(currentPage);
        }
    });

    nextButton.on("click", function () {
        const prodotti = $(".prodotto");
        const totalItems = prodotti.length;
        const totalPages = Math.ceil(totalItems / itemsPerPage);

        if (currentPage < totalPages) {
            currentPage++;
            showPage(currentPage);
        }
    });

    showPage(currentPage);
});


//----------------------------------------------------------------------------------------------

$(document).ready(function () {
    $("#comparsa").on("click", function () {
        $("#login_div").show();
    });

    $("#comparsa2").on("click", function () {
        $("#login_div2").show();
    });

    $("#chiudi_div").on("click", function () {
        $("#login_div").hide();
    });

    $("#chiudi_div2").on("click", function () {
        $("#login_div2").hide();
    });

    $(document).on("click", function (event) {
        if (!$(event.target).closest("#comparsa, #login_div").length) {
            $("#login_div").hide();
        }
    });

    $(document).on("click", function (event) {
        if (!$(event.target).closest("#comparsa2, #login_div2").length) {
            $("#login_div2").hide();
        }
    });

});


//---------------------------------------------------------------------------------------------

$(document).ready(function () {
    const panoramicaContainer = $(".panoramica-container");
    const panoramica = $(".panoramica");
    const prevButton = $("#indietro");
    const nextButton = $("#avanti");

    const itemWidth = 300; // Larghezza di un elemento "prodotto"
    const itemsPerPage = 4; // Numero di elementi da mostrare per pagina
    let currentPage = 1;

    function showPage(page) {
        const startIndex = (page - 1) * itemsPerPage;
        const endIndex = startIndex + itemsPerPage;

        const prodotti = $(".prodotto");

        prodotti.each(function (index, element) {
            if (index >= startIndex && index < endIndex) {
                $(element).show();
            } else {
                $(element).hide();
            }
        });
    }

    prevButton.on("click", function () {
        if (currentPage > 1) {
            currentPage--;
            showPage(currentPage);
        }
    });

    nextButton.on("click", function () {
        const prodotti = $(".prodotto");
        const totalItems = prodotti.length;
        const totalPages = Math.ceil(totalItems / itemsPerPage);

        if (currentPage < totalPages) {
            currentPage++;
            showPage(currentPage);
        }
    });

    showPage(currentPage);
});