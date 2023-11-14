function editarMotorista() {
    var select = document.getElementById("SelecionarMotorista");
    var selectedId = select.options[select.selectedIndex].value;
    if (selectedId) {
        window.location.href = `/editarMotorista/${selectedId}`;
    }
}

function editarVeiculo() {
    var select = document.getElementById("SelecionarPlaca");
    var selectedId = select.options[select.selectedIndex].value;
    if (selectedId) {
        window.location.href = `/editarVeiculo/${selectedId}`;
    }
}

function relatorioVeiculo() {
    var select = document.getElementById("SelecionarPlaca");
    var selectedId = select.options[select.selectedIndex].value;
    if (selectedId) {
        window.location.href = `/generate-pdf/${selectedId}`;
    }
}


function editarManutencao() {
    var select = document.getElementById("SelecionarManutencao");
    var selectedId = select.options[select.selectedIndex].value;
    if (selectedId) {
        window.location.href = `/editarTipoManutencao/${selectedId}`;
    }
}