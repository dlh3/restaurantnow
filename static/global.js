
function showlogin()
{ 
    $('#loginbox').fadeIn('slow');
    $('#login_username').focus();
}



$(function()
{
    $('#showloginboxlink').click(function()
    {
        showlogin();
    });

    $('#hideloginbox').click(function()
    {
        $('#loginbox').hide();
    });

    // Make it so you can click anywhere in a main menu item to go where the link points
    $('.webMenuItem').click(function()
    {
        var link=$(this).find('a').attr('href');
        if (link=="#") showlogin();
        else window.location=link;
    });

    
});
