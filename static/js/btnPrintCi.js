var btnPrintCi = document.getElementById('btnPrintCi')

btnPrintCi.addEventListener('click',()=>{
    // Obter uma comunicação por ID
    apiService.getById('comunicacao', document.getElementById('idCiNum').value)
    .then(data => populaCi(data))
    .catch(error => console.error('Error:', error));

})