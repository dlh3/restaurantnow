// Global for click binding
// Red X in cart
function removeCartItem()
{
    var existing = $(this).parents('.cartitem');
    var oldtotal = parseFloat(existing.children(".ordercartlinetotal").text());
    var price = parseFloat(existing.children(".ordercartprice").text());
    var oldsubtotal = parseFloat($('#ordercartsubtotal').text());
    if (isNaN(price) || isNaN(oldtotal) || isNaN(oldsubtotal))
        return;

    $('#ordercartsubtotal').text((oldsubtotal - oldtotal).toFixed(2));
    $('#' + existing.attr('id').replace('ordercart', '')).attr('value', '');
    existing.remove();
}
// Change count in cart
function changeCartCount(input)
{
    var num = parseInt(input.target.value);
    var existing = $(this).parents('.cartitem');
    var noNum = (isNaN(num) || num == 0);
    if (noNum)
    {
        num = 0;
        input.target.value = '';
        $('#' + existing.attr('id').replace('ordercart', '')).attr('value', '');
    }
    else
    {
        input.target.value = num;
        $('#' + existing.attr('id').replace('ordercart', '')).attr('value', num);
    }

    var oldtotal = parseFloat(existing.children(".ordercartlinetotal").text());
    var price = parseFloat(existing.children(".ordercartprice").text());
    var oldsubtotal = parseFloat($('#ordercartsubtotal').text());
    if (isNaN(price) || isNaN(oldtotal) || isNaN(oldsubtotal))
        return;

    var linetotal = num * price;
    existing.children(".ordercartlinetotal").text(linetotal.toFixed(2));
    $('#ordercartsubtotal').text((oldsubtotal - oldtotal + linetotal).toFixed(2));

    if (noNum)
        existing.remove();
}

$(function()
{
    
    $('#checkout')
        .button()
        .click(function() {
            //Checkout
        });
    // Effects for displaying categories
    $('#menu').accordion({ active:false, autoHeight:false, icons:{ header:'ui-icon-arrowthick-1-e', headerSelected:'ui-icon-arrowthick-1-s' }, navigation:true });
    // Do the right thing with the date/time lines
    $('#id_date').datepicker();
    $('#id_date').datepicker('setDate', (new Date()));
    $('#id_time').timepicker({ ampm:true, stepMinute:5 });
    $('#id_time').timepicker('setDate', (new Date()));

    // Add items to the cart as the user shops
    $('.menuiteminput').change(function(input)
    {
        var num = parseInt(input.target.value);
        var noNum = (isNaN(num) || num == 0);
        if (noNum)
            input.target.value = '';
        else
            input.target.value = num;

        var oldsubtotal = parseFloat($('#ordercartsubtotal').text());
        if (isNaN(oldsubtotal))
            return;

        var existing = $('#ordercart' + input.target.id);
        if (existing.length != 0)
        {
            var oldtotal = parseFloat(existing.children(".ordercartlinetotal").text());
            var price = parseFloat(existing.children(".ordercartprice").text());
            if (isNaN(price) || isNaN(oldtotal))
                return;

            if (noNum)
            {
                existing.remove();
                $('#ordercartsubtotal').text((oldsubtotal - oldtotal).toFixed(2));
            }
            else
            {
                var linetotal = num * price;
                existing.children(".ordercartcount").attr('value', num);
                existing.children(".ordercartlinetotal").text(linetotal.toFixed(2));
                $('#ordercartsubtotal').text((oldsubtotal - oldtotal + linetotal).toFixed(2));
            }
        }
        else if (!noNum)
        {
            var menuitem = $(this).parents('.menuitem');
            var menuitemline = $('#menu' + input.target.id + 'sized');
            var newitem = $('<div id="ordercart' + input.target.id + '" class="cartitem">');
            var price = parseFloat(menuitemline.children(".menuitemprice").text());
            var linetotal = num * price;
            if (isNaN(price))
                return;
            $('#ordercartitems').append(newitem);
            newitem.append('<img src="/static/red_x.png" alt="Remove" width="16" height="16" class="removecartitem" /> ' + '<img src="' + menuitem.find(".menuitemimage").attr('src') + '" width="50" height="50" />'
                            + menuitem.children(".menuitemname").text() + ' (' + menuitemline.children(".menuitemsize").text() + '): <input type="text" size="2" class="ordercartcount" value="' + input.target.value + '" />'
                            + '</span> x $<span class="ordercartprice">' + price.toFixed(2) + '</span> = $<span class="ordercartlinetotal">' + linetotal.toFixed(2) + '</span>');
            newitem.children().addClass('ordercartcontents');
            newitem.children('.removecartitem').bind('click', removeCartItem);
            newitem.children('.ordercartcount').bind('change', changeCartCount);
            $('#ordercartsubtotal').text((oldsubtotal + linetotal).toFixed(2));
        }
    });
});
