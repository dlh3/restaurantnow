$(function()
{
    // $('#usernameverify').removeClass('ui-icon-check ui-icon-closethick').addClass('ui-icon-check');
    // $('#usernameverify').removeClass('ui-icon-check ui-icon-closethick').addClass('ui-icon-closethick');

    $('#id_username').keyup(function()
    {
        var uname = $(this).val();
        if (uname.length >= 4)
        {
            $.get(nameserv, { uname:uname }, function(data)
            {
                if (data == '0') //Available
                    $('#usernameverify').attr('src', '/static/green_check.png');
                else //Taken
                    $('#usernameverify').attr('src', '/static/red_x.png');
            });
        }
        else //Too short
            $('#usernameverify').attr('src', '/static/red_x.png');
    });
    $('#id_password').keyup(function()
    {
        if ($(this).val().length >= 8)
            $('#passwordverify').attr('src', '/static/green_check.png');
        else //Too short
            $('#passwordverify').attr('src', '/static/red_x.png');
        $('#id_passwordver').trigger('keyup');
    });
    $('#id_passwordver').keyup(function()
    {
        if ($(this).val() == $('#id_password').val() && $(this).val().length >= 8) //Matches and is long enough
            $('#passwordververify').attr('src', '/static/green_check.png');
        else //Too short or doesn't match
            $('#passwordververify').attr('src', '/static/red_x.png');
    });
    $('#id_email').keyup(function()
    {
        if ($(this).val().match(/^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/))
            $('#emailverify').attr('src', '/static/green_check.png');
        else //Too short
            $('#emailverify').attr('src', '/static/red_x.png');
    });
});
