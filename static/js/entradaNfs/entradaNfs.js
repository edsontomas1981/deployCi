inptChaveAcesso.addEventListener('blur', ()=> {
    let dadosChave = separarChaveNFe(inptChaveAcesso.value)
    console.log(dadosChave)

    let {data , hora} = obterDataHoraAtual()

    inptCnpjRem.value = dadosChave.cnpj
    inptNumeroNf.value = dadosChave.numero

    inptData.value=data
    inptHora.value = hora
})


btnImprimirEtiquetas.addEventListener('click',()=>{
    gerarEtiqueta()
})

function gerarEtiqueta() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({
        unit: "mm",
        format: [28, 89] // Etiqueta com largura de 89mm e altura de 28mm
    });

    // Adiciona texto da etiqueta
    doc.setFont("helvetica", "bold");
    doc.setFontSize(10);
    doc.text("Transportadora XYZ", 5, 10);
    doc.text("Volume: 001", 5, 16);
    doc.text("Filial: São Paulo", 5, 22);

    // Criar um SVG dinamicamente para o código de barras
    let svgElement = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svgElement.id = "barcode";
    document.body.appendChild(svgElement); // Adiciona ao DOM temporariamente

    window.open(doc.output("bloburl"), "_blank");

}