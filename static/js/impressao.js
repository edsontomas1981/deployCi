const { jsPDF } = window.jspdf;
const reportCi = (dados) => {
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const marginLeft = 20;
    const marginRight = 20;
    const marginTop = 10;
    const maxWidth = pageWidth - marginLeft - marginRight;
    const centerX = pageWidth / 2;

    // Logo
    doc.addImage('./logonorte.jpg', 'JPEG', 10, 10, 50, 15);

    // Empresa e Detalhes
    doc.setFontSize(12);
    doc.text('SERAFIM TRANSPORTE DE CARGAS LTDA', centerX, 40, { align: 'center' });
    doc.setFontSize(10);
    doc.text('Rua: Nova Veneza, 172 Cumbica – Guarulhos-SP', centerX, 45, { align: 'center' });
    doc.text('Tel(11)2481-9121/2481-9697/2412-4886/2412-3927', centerX, 50, { align: 'center' });

    doc.setFontSize(12);
    doc.text(`Comunicação Interna Nº ${dados.ci_num}`, centerX, 70, { align: 'center' });
    doc.setFontSize(10);
    doc.text(`Data: ${dados.data} Percurso: ${dados.percurso}`, centerX, 75, { align: 'center' });

    doc.setFontSize(12);
    doc.text(`${dados.destinatario},`, marginLeft, 90, { maxWidth });
    doc.text(`Estamos enviando o manifesto de transporte de cargas nº ${dados.manifesto_numero}. Este manifesto inclui conhecimentos de frete.`, marginLeft, 100, { maxWidth });
    doc.text(`De acordo com este manifesto, solicitamos o pagamento de ${dados.valor_frete} ao motorista ${dados.motorista}, referente à Ordem de Pagamento.`, marginLeft, 110, { maxWidth });

    if (dados.isca_2 !== '') {
        doc.text(`Além disso, incluímos as seguintes iscas de monitoramento: ${dados.isca_1} e ${dados.isca_2}.`, marginLeft, 120, { maxWidth });
    } else {
        doc.text(`Também incluímos a seguinte isca de monitoramento: ${dados.isca_1}.`, marginLeft, 120, { maxWidth });
    }

    if (dados.observacao !== '') {
        doc.setFontSize(12);
        doc.text(`Observações:`, marginLeft, 140, { maxWidth });
        doc.setFontSize(10);
        doc.text(dados.observacao, marginLeft, 150, { maxWidth });
    }

    // Assinaturas
    doc.setFontSize(12);
    doc.text('Assinatura da Empresa', marginLeft, 200);
    doc.text('Assinatura do Motorista', marginLeft + 120, 200);

    doc.setFontSize(10);
    doc.text('SERAFIM TRANSPORTE DE CARGAS LTDA', marginLeft, 220);
    doc.text(dados.motorista, marginLeft + 120, 220);

    // Abrir o PDF em uma nova aba
    const pdfOutput = doc.output('blob');
    const url = URL.createObjectURL(pdfOutput);
    window.open(url);
};