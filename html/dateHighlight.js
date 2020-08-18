$( document ).ready(function()
{
    const date = new Date();
    const today = date.getDay() + 1;
    $(`.day_${today}`).addClass('active')
});