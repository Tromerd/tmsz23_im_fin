function bootstrap_form(selector) {
    var form = document.querySelector(selector);
    console.log(form)
    form.setAttribute('role',"form");
    //form.setAttribute('class',"form-inline")
    var element_in_form = Array.from(form.getElementsByTagName('p'));
    console.log((element_in_form))
    element_in_form.forEach(function (value, index) {
        var wrapper = document.createElement('div');
        wrapper.setAttribute('class', 'form-group')
        wrapper.innerHTML = value.innerHTML;
        value.parentNode.replaceChild(wrapper,value)
        console.log(value.innerHTML)
    })
    var form = document.querySelectorAll(selector+' div :not(label) ' );
    form.forEach(function(item, i, arr){
    console.log(form[i].setAttribute('class','form-control'))
});
};
