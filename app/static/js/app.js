$(document).ready(function () {
    $('.carousel').flickity({
        cellAlign: 'center',
        contain: true,
        pageDots: false,
        prevNextButtons: true,
        cellSpacing: 10,
        resize: true,     // Garante que ele redimensione com a tela
    });
});
