
var maskCNPJ = IMask(document.getElementById('id_cnpj'), {
    mask: '00.000.000/0000-00'
})

var maskPostalCode = IMask(document.getElementById('id_postal_code'), {
    mask: '00000-000'
})

var maskPhone = IMask(document.getElementById('phone'), {
    mask: '(00) 0 0000-0000'
})

var maskPhone2 = IMask(document.getElementById('phone2'), {
    mask: '(00) 0 0000-0000'
})
