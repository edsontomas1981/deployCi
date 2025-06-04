// Criar uma instância da PilhaDeModais
var pilhaDeModais = new PilhaDeModais();

// Função para abrir um modal e empilhar
function openModal(modalId) {
    // Esconde o modal atual, se houver
    if (!pilhaDeModais.isEmpty()) {
        var currentModal = pilhaDeModais.peek();
        $('#'+currentModal).modal('hide');
    }
    // Abre o novo modal
    $('#'+modalId).modal('show');
    console.log(pilhaDeModais.peek())
    // Adiciona o novo modal à pilha
    pilhaDeModais.push(modalId);
}

// Função para fechar o modal atual e retornar ao anterior
function closeModal() {
    // Remove o modal atual da pilha
    var currentModal = pilhaDeModais.pop();

    // Fecha o modal atual
    $('#' + currentModal).modal('hide');

    if (!pilhaDeModais.isEmpty()) {
        var previousModal = pilhaDeModais.peek();
        $('#' + previousModal).modal('show');
    }

}
