$( document ).ready(function()
{
    const date = new Date();
    const today = date.getDay();
    $(`.day_${today}`).addClass('active')
});