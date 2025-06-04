class PilhaDeModais {
    constructor() {
      this.items = [];
    }
  
    // Adicionar um elemento ao topo da pilha
    push(element) {
      this.items.push(element);
    }
  
    // Remover o elemento do topo da pilha e retorná-lo
    pop() {
      if (this.isEmpty()) {
        return "Underflow";
      }
      return this.items.pop();
    }
  
    // Retorna o elemento no topo da pilha sem removê-lo
    peek() {
      return !this.isEmpty() ? this.items[this.items.length - 1] : "Não existem elementos na pilha";
    }
  
    // Retorna verdadeiro se a pilha estiver vazia, senão retorna falso
    isEmpty() {
      return this.items.length === 0;
    }
  
    // Retorna o tamanho da pilha
    size() {
      return this.items.length;
    }
  
    // Limpa a pilha
    clear() {
      this.items = [];
    }
  
    // Retorna a pilha como uma string
    toString() {
      return this.items.toString();
    }
  }
