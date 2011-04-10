// Submitable?
var submitable = false;

// Generate the select options for Phone and Address categories
var phoneoptions = '<select name="newphonedescription" class="profilecategorydescsel">';
phoneoptions = phoneoptions + '<option value="-1" selected="selected" disabled="disabled"></option>';
$.each(phonecategories, function(key, val){ phoneoptions = phoneoptions + '<option value="' + key + '">' + val + '</option>'; });
phoneoptions = phoneoptions + '</select><br />';

var addressoptions = '<select name="newaddressdescription" class="profilecategorydescsel">';
addressoptions = addressoptions + '<option value="-1" selected="selected" disabled="disabled"></option>';
$.each(addresscategories, function(key, val){ addressoptions = addressoptions + '<option value="' + key + '">' + val + '</option>'; });
addressoptions = addressoptions + '</select><br />';


// Declared globally to allow for change/click binding in new Phone/Address entries
function deletePhone()
{
    var parent = $(this).parents('.phone');
    var hermit = parseInt(parent.attr('id').replace('phone', ''));
    parent.fadeOut('slow');
    if (!isNaN(hermit))
    {
        $('#phoneContainer').append('<input type="hidden" class="hiddeninput" name="removephone" value="' + hermit + '" />');
        $('#existingphone' + hermit).remove();
    }
    submitable = true;
}

function deleteAddress()
{
    var parent = $(this).parents('.address');
    var hermit = parseInt(parent.attr('id').replace('address', ''));
    parent.fadeOut('slow');
    if (!isNaN(hermit))
    {
        $('#addressContainer').append('<input type="hidden" class="hiddeninput" name="removeaddress" value="' + hermit + '" />');
        $('#existingaddress' + hermit).remove();
    }
    submitable = true;
}

function changeHeading()
{
    $(this).parents('.profileeditable').find('.profilecategorydesc').text(this.options[this.selectedIndex].text + ' ');
}

// And away we go....
$(document).ready(function()
{
    //Phone jQueryUI Elements------------------------------------------------------------------------
    var $tab_title_input = $( "#tab_title"),
    $tab_content_input = $( "#tab_content" );
    var phone_tab_counter = $(document).find('#phoneContainer').find('li').last('li').attr('id');
    var address_tab_counter = $(document).find('#addressContainer').find('li').last('li').attr('id');

    // tabs init with a custom tab template and an "add" callback filling in the content
    var $phonetabs = $( "#phoneContainer").tabs({
        tabTemplate: "<li ><a href='#{href}'>#{label}</a></li>",
        add: function( event, ui ) {
            var tab_content = "Tab " + phone_tab_counter + " content.";
            var newentry = $('<div class="phone userprofileedit profileeditbox profileeditable">'
                            + '<div class="userheading newuserheading"><span class="profilecategorydesc"></span>Phone:<a id="deletePhone{{ phone.id }}" class="editUser deletePhone ui-icon ui-icon-trash" href="#" onclick="return false">Delete this entry</a></div>'
                            + '<div class="profileerror"></div>'
                            + '<span class="fieldtitle">Description:<br /></span>'
                            + phoneoptions
                            + '<span class="fieldtitle">Number:<br /></span>'
                            + '<input type="text" name="newphonenumber" maxlength="30" /><br />'
                            + '</div>');            
            $( ui.panel ).append( newentry );
            $(document).find('phoneContainer').find('ul').last('li').attr('id', 'phone_tab_counter'); //TODO: This isn't quite working, we want to find the newly added li element and give it id=phone_tab_counter
            //TODO: Set new tab's li element to have an id=new_tab_counter
            //TODO: Hook up the a element in the li element of the tab with the <span class="profilecategorydesc"></span> so it updates the description when the user changes it when updating
            //TODO: Once these are all fixed, apply the changes to the address tabs as well
            newentry.find('.profilecategorydescsel').bind('change', changeHeading);
            newentry.find('.deletePhone').bind('click', deletePhone);
            newentry.fadeIn('slow');
            $('#userprofilesavebutton').fadeIn('slow');
            submitable = true;

        }
    });

    // actual addTab function: adds new tab using the title input from the form above
    function addPhoneTab() {
        phone_tab_counter++;
        var tab_title = "<span class='profilecategorydesc'>New</span> Phone";
        $phonetabs.tabs( "add", "#phone" + phone_tab_counter, tab_title );
    }

    // addTab button: just opens the dialog
    $( "#addPhone" )
        .button()
        .click(function() {
            addPhoneTab();
        });

    // close icon: removing the tab on click
    $( '.deletePhone').live( "click", function() {
        //Clear tabs internal data
        var parent = $(this).parents('.phone');
        var hermit = parseInt(parent.attr('id').replace('phone', ''));
        parent.fadeOut('slow');
        if (!isNaN(hermit))
        {
            $('#phoneContainer').append('<input type="hidden" class="hiddeninput" name="removephone" value="' + hermit + '" />');
            $('#existingphone' + hermit).remove();
        }
        //Remove the jQuery tab
        var id = parent.attr('id')
                alert("id "+id);
        var index = $( "li", $phonetabs ).index( $( this ).parents('#phoneContainer').find('#'+id));
                alert("index "+index);
        $phonetabs.tabs( "remove", index );
    });
    //End Phone jQueryUI Elements--------------------------------------------------------------------
    
    //Address jQueryUI Elements----------------------------------------------------------------------

    // tabs init with a custom tab template and an "add" callback filling in the content
    var $addresstabs = $( "#addressContainer").tabs({
        tabTemplate: "<li><a href='#{href}'>#{label}</a></li>",
        add: function( event, ui ) {
            var tab_content = "Tab " + address_tab_counter + " content.";
            var newentry = $('<div class="address userprofileedit profileeditbox profileeditable">'
                            + '<div class="userheading newuserheading"><span class="profilecategorydesc"></span>Address:<a id="deleteAddress{{ address.id }}" class="editUser deleteAddress ui-icon ui-icon-trash" href="#" onclick="return false">Delete this entry</a></div>'
                            + '<div class="profileerror"></div>'
                            + '<span class="fieldtitle">Description:<br /></span>'
                            + addressoptions
                            + '<span class="fieldtitle">Line 1:<br /></span>'
                            + '<input type="text" name="newaddress1" maxlength="100" /><br />'
                            + '<span class="fieldtitle">Line 2:<br /></span>'
                            + '<input type="text" name="newaddress2" maxlength="100" /><br />'
                            + '<span class="fieldtitle">Buzz Code:<br /></span>'
                            + '<input type="text" name="newbuzzcode" maxlength="100" /><br />'
                            + '<span class="fieldtitle">City:<br /></span>'
                            + '<input type="text" name="newcity" maxlength="100" /><br />'
                            + '<span class="fieldtitle">Province:<br /></span>'
                            + '<input type="text" name="newstate" maxlength="100" /><br />'
                            + '<span class="fieldtitle">Country:<br /></span>'
                            + '<input type="text" name="newcountry" maxlength="100" /><br />'
                            + '<span class="fieldtitle">Postal Code:<br /></span>'
                            + '<input type="text" name="newpostalcode" maxlength="100" /><br />'
                            + '<span class="fieldtitle">Drivers Notes:<br /></span>'
                            + '<textarea rows="2" cols="40" name="newdrivernotes"></textarea><br />'
                            + '</div>');
            $( ui.panel ).append(newentry);
            newentry.find('.profilecategorydescsel').bind('change', changeHeading);
            newentry.find('.deleteAddress').bind('click', deleteAddress);
            newentry.fadeIn('slow');
            submitable = true;

        }
    });

    // actual addTab function: adds new tab using the title input from the form above
    function addAddressTab() {
        address_tab_counter++;
        var tab_title = "<span class='profilecategorydesc'>New</span> Address";
        $addresstabs.tabs( "add", "#address" + address_tab_counter, tab_title );
    }

    // addTab button: just opens the dialog
    $( "#addAddress" )
        .button()
        .click(function() {
            addAddressTab();
        });

    // close icon: removing the tab on click
    $( '.deleteAddress').live( "click", function() {
        //Clear tabs internal data
        var parent = $(this).parents('.address');
        var hermit = parseInt(parent.attr('id').replace('address', ''));
        parent.fadeOut('slow');
        if (!isNaN(hermit))
        {
            $('#addressContainer').append('<input type="hidden" class="hiddeninput" name="removeaddress" value="' + hermit + '" />');
            $('#existingaddress' + hermit).remove();
        }
        //Remove the jQuery tab
        var id = parent.attr('id')
        var index = $( "li", $addresstabs ).index( $( this ).parents('#addressContainer').find('#'+id));
        $addresstabs.tabs( "remove", index );
    });
    
    //End Address jQueryUI Elements------------------------------------------------------------------
    
    // Toggles the edit profile form
    // Whole form
    $('#profileeditall').click(function()
    {
        $(this).hide();
        $('.profileeditable').trigger('click');
    });
    // Single section
    $('.profileeditable').click(function()
    {
        $(this).addClass('profileeditbox');
        $(this).find('.userprofilemode[id!="profileeditall"]').hide();
        $(this).find('.userprofileedit').fadeIn('slow');
        $('#userprofilesavebutton').fadeIn('slow');
        $(this).find('.editLabel').addClass("hideEditLabel");
        $(this).find('.editLabel').removeClass("editLabel");
        submitable = true;
        $(this).unbind('click');
        $(this).find('input[type="text"]')[0].focus();
    });

    // Change the description in the header
    $('.profilecategorydescsel').change(changeHeading);

    // Delete Phone
    $('.deletePhone').click(deletePhone);
    // Delete Address
    $('.deleteAddress').click(deleteAddress);

    //On Hover
    $('.profileeditable').hover(
        function()
        {
            $(this).find('.editLabel').fadeIn('slow'); //mouseover
        },
        function()
        {
            $(this).find('.editLabel').hide(); // mouseout
        }
    ); // end hover
    
    $('#userprofileform').submit(function()
    {
        var broke = false;
        $('.profilecategorydescsel').each(function()
        {
            if ($(this).attr('value') == -1)
            {
                $(this).focus();
                $(this).parents('.userprofileedit').children('.profileerror').append('<br />Please select a description');
                broke = true;
                return false;
            }
        });
        broke = broke || !submitable;
        if (!submitable)
            setTimeout("$('#profileeditall').trigger('click')", 0);
        return !broke;
    });
    $('.editableerror').trigger('click');
    $('#userprofilesavebutton').button();
    $('#userprofiledeletebutton').button();
});
