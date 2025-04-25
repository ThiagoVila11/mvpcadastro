// Função para inicializar tooltips
$(function () {
    $('[data-bs-toggle="tooltip"]').tooltip();
    
    // Fechar mensagens automaticamente após 5 segundos
    setTimeout(function() {
        $('.alert').alert('close');
    }, 5000);
});

// Função para confirmar ações importantes
function confirmAction(message) {
    return confirm(message || 'Tem certeza que deseja realizar esta ação?');
}