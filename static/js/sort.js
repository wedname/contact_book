var all = $('#contacts');
var isAscOrder = true;


$(".sort .asc").click(function () {
    var mylist = $('#contacts');
    var listitems = mylist.children('div').get();

    listitems.sort(function(a, b) {
       var compA = $(a).text().toUpperCase();
       var compB = $(b).text().toUpperCase();
       return (compA < compB) ? -1 : (compA > compB) ? 1 : 0;
    })
    $.each(listitems, function(idx, itm) { mylist.append(itm); });
});


$(".sort .desc").click(function () {
    var mylist = $('#contacts');
    var listitems = mylist.children('div').get();

    isAscOrder = false;

    listitems.sort(function(a, b) {
        var compA = $(a).text().toUpperCase();
        var compB = $(b).text().toUpperCase();

        return (isAscOrder ? 1 : -1) * ((compA < compB) ? -1 : (compA > compB) ? 1 : 0);
    });

    $.each(listitems, function(idx, itm) { mylist.append(itm); });
});


$(".group .{{group.group}}").click(function () {

});