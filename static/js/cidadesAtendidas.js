const excluirCidade = async (id) => {
  deletarCidade(id)
}

async function loadImageAsBase64(url) {
  const response = await fetch(url);
  const blob = await response.blob();
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
}

const obtemDadosCadastroAlteracao = ()=>{
  let id = document.getElementById('idCidade').value
  let cidade = document.getElementById('cidade').value
  let filialResponsavel = obterOpcaoSelecionada('filial').value
  return {id:id,cidade:cidade,filialResponsavel:filialResponsavel}
}

let btnSalvarCidade = document.getElementById('btnSalvar')
btnSalvarCidade.addEventListener('click',()=>{
  let dados = obtemDadosCadastroAlteracao()
  if (dados.id == '' ) {
    cadastrarCidade(dados.cidade,dados.filialResponsavel)
    loadCidades()
    return
  }
  atualizarCidade(dados.id,dados.cidade,dados.filialResponsavel)
  return
})

const cadastrarCidade = async (cidade, filialResponsavel) => {
  const confirmado = await msgConfirmacao("Deseja realmente cadastrar esta cidade?");
  if (!confirmado) return;

  try {
    const resposta = await fetch('/cidades_atendidas', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        cidade: cidade,
        filial_responsavel: filialResponsavel
      })
    });

    const dados = await resposta.json();

    if (resposta.ok) {
      msgOk("Cidade cadastrada com sucesso!");
      loadCidades()
    } else {
      msgErro(`Erro ao cadastrar cidade: ${dados.erro || "Erro desconhecido"}`);
    }
  } catch (erro) {
    msgErroFixa("Erro na requisição para cadastrar cidade.");
    console.error(erro);
  }
};

const atualizarCidade = async (id, cidade, filialResponsavel) => {
  const confirmado = await msgConfirmacao("Deseja realmente atualizar esta cidade?");
  if (!confirmado) return;

  try {
    const resposta = await fetch(`/listar_cidades_atendidas/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        cidade: cidade,
        filial_responsavel: filialResponsavel
      })
    });

    const dados = await resposta.json();

    if (resposta.ok) {
      msgOk("Cidade atualizada com sucesso!");
      loadCidades()
    } else {
      msgErro(`Erro ao atualizar cidade: ${dados.erro || "Erro desconhecido"}`);
    }
  } catch (erro) {
    msgErroFixa("Erro na requisição para atualizar cidade.");
    console.error(erro);
  }
};


const deletarCidade = async (id) => {
  const confirmado = await msgConfirmacao("Deseja realmente excluir esta cidade?");
  if (!confirmado) return;

  try {
    const resposta = await fetch(`/listar_cidades_atendidas/${id}`, {
      method: 'DELETE'
    });

    const dados = await resposta.json();

    if (resposta.ok) {
      msgOk("Cidade excluída com sucesso!");
      loadCidades()
    } else {
      msgErro(`Erro ao excluir cidade: ${dados.erro || "Erro desconhecido"}`);
    }
  } catch (erro) {
    msgErroFixa("Erro ao tentar excluir cidade.");
    console.error(erro);
  }
};

const editaCidade = async (id) => {
    let modal = new bootstrap.Modal('modalEditaCidade');
    openModal('modalEditaCidade')
    let cidade = await buscarCidadeId(id)
    document.getElementById('cidade').value = cidade.cidade
    selecionaValorSelect('filial', cidade.filial_responsavel);
    document.getElementById('idCidade').value = cidade.id
}

const loadCidades = async ()=>{

  let botoesCidades={
          excluir:{
              classe: "btn btn-danger text-white btn-table",
              texto: '<i class="fa fa-trash" aria-hidden="true"></i>',
              callback:excluirCidade
              },
          buscar:{
              classe: "btn btn-primary text-white btn-table",
              texto: '<i class="fa fa-edit" aria-hidden="true"></i>',
              callback: editaCidade
              }
  };

  let dados = await  jsonCidades()

  popula_tbody_paginacao('navCidadesAtendidas','tbodyCidadesAtendidas',dados,botoesCidades,1,20,false)
  let inptCidade = document.getElementById('inptBuscaCidade')

  inptCidade.addEventListener('input',()=>{
      let dadosFiltrados = buscarCidade(dados,inptCidade.value)
      popula_tbody_paginacao('navCidadesAtendidas','tbodyCidadesAtendidas',dadosFiltrados,botoesCidades,1,20,false)
  })

}

document.addEventListener('DOMContentLoaded',async ()=>{
  loadCidades()
})

let btnCadastrarCidade = document.getElementById('btnCadastrarCidade')
btnCadastrarCidade.addEventListener('click', ()=>{
  openModal('modalEditaCidade')
  document.getElementById('cidade').value = ""
  document.getElementById('idCidade').value = ""
})

const gerarPDFCidades = async () => {
  try {
    const resposta = await fetch('/listar_cidades_atendidas');
    const cidades = await resposta.json();

    if (!resposta.ok) {
      msgErro("Erro ao buscar cidades.");
      return;
    }

    if (cidades.length === 0) {
      msgAviso("Nenhuma cidade encontrada.");
      return;
    }

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    // Carregar imagem da logo
    const logoBase64 = await loadImageAsBase64('/static/image/logo.png');
    const originalWidth = 300; // largura real da imagem em pixels
    const originalHeight = 100; // altura real da imagem em pixels

    const newWidth = 60;
    const newHeight = (originalHeight / originalWidth) * newWidth;


    // Inserir imagem na posição (x, y) com a nova altura calculada
    doc.addImage(logoBase64, 'PNG', 10, 10, newWidth, newHeight);

    const pageWidth = doc.internal.pageSize.getWidth();
    let textY = 20; // mesma altura vertical da imagem

    doc.setFontSize(10);
    doc.text("Serafim Transportes de Cargas Ltda.", pageWidth - 10, textY, { align: 'right' });
    textY += 5;
    doc.text("Rua Nova Veneza, 172 - Cumbica - Guarulhos - CEP 07243-180", pageWidth - 10, textY, { align: 'right' });
    textY += 5;
    doc.text("Fone: (11) 2481-9697", pageWidth - 10, textY, { align: 'right' });
    textY += 5;
    doc.text("CNPJ: 23.926.683/0002-99", pageWidth - 10, textY, { align: 'right' });


    // Título do relatório
    textY += 10;
    doc.setFontSize(14);
    doc.text("Relação de Cidades Atendidas", 105, textY, { align: 'center' });

    doc.setFontSize(8);
    let y = textY + 10;
    const lineHeight = 7;

    const drawHeader = () => {
      doc.setFillColor(40, 40, 40);
      doc.setTextColor(255);
      doc.rect(10, y, 90, lineHeight, 'F');
      doc.rect(110, y, 90, lineHeight, 'F');
      doc.text("Cidade", 12, y + 5);
      doc.text("Filial", 60, y + 5);
      doc.text("Cidade", 112, y + 5);
      doc.text("Filial", 160, y + 5);
      y += lineHeight;
    };

    drawHeader();

    for (let i = 0; i < cidades.length; i += 2) {
      const cidade1 = cidades[i];
      const cidade2 = cidades[i + 1];
      const isPar = Math.floor(i / 2) % 2 === 0;
      const bgColor = isPar ? [245, 245, 245] : [220, 220, 220];

      doc.setFillColor(...bgColor);
      doc.setTextColor(0);
      doc.rect(10, y, 90, lineHeight, 'F');
      doc.rect(110, y, 90, lineHeight, 'F');

      doc.text(cidade1.cidade, 12, y + 5);
      doc.text(cidade1.filial_responsavel, 60, y + 5);

      if (cidade2) {
        doc.text(cidade2.cidade, 112, y + 5);
        doc.text(cidade2.filial_responsavel, 160, y + 5);
      }

      y += lineHeight;

      if (y > 275) {
        doc.addPage();
        y = 20;
        drawHeader();
      }
    }

    doc.save("relacao_cidades_atendidas.pdf");
    msgOk("PDF gerado com sucesso!");
  } catch (erro) {
    console.error(erro);
    msgErroFixa("Erro ao gerar o PDF.");
  }
};




const gerarExcelCidades = async () => {
  try {
    const resposta = await fetch('/listar_cidades_atendidas');
    const cidades = await resposta.json();

    if (!resposta.ok) {
      msgErro("Erro ao buscar cidades para gerar Excel.");
      return;
    }

    if (cidades.length === 0) {
      msgAviso("Nenhuma cidade encontrada para exportar.");
      return;
    }

    // Criar uma nova planilha
    const worksheet = XLSX.utils.json_to_sheet(cidades);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Cidades");

    // Gerar e baixar o arquivo
    XLSX.writeFile(workbook, "cidades_atendidas.xlsx");

    msgOk("Planilha gerada com sucesso!");
  } catch (erro) {
    console.error(erro);
    msgErroFixa("Erro ao gerar a planilha Excel.");
  }
};

document.getElementById('btnGerarXLS').addEventListener('click',()=>{
  gerarExcelCidades()
})


document.getElementById('btnGerarPDF').addEventListener('click',()=>{
  gerarPDFCidades()
})
