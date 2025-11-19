function bloquearForm() {
    document.getElementById("card_paciente").classList.add("bloqueado");
    document.getElementById("card_oci").classList.add("bloqueado");
    document.getElementById("acoes_form").classList.add("bloqueado");
}

function liberarForm() {
    document.getElementById("card_paciente").classList.remove("bloqueado");
    document.getElementById("card_oci").classList.remove("bloqueado");
    document.getElementById("acoes_form").classList.remove("bloqueado");
}

document.addEventListener("DOMContentLoaded", bloquearForm);


async function buscarCPF() {
    const cpf = document.getElementById("cpf_lookup").value.trim();
    const msg = document.getElementById("statusBusca");

    if (!cpf) {
        bloquearForm();
        msg.textContent = "Digite um CPF antes de buscar.";
        msg.className = "search-status status-warning";
        return;
    }

    msg.textContent = "Buscando...";
    msg.className = "search-status status-info";

    const response = await fetch(`/buscar-paciente/?cpf=${cpf}`);
    const data = await response.json();

    if (data.exists) {
        liberarForm();

        msg.textContent = "Paciente encontrado!";
        msg.className = "search-status status-success";

        document.getElementById("paciente_id").value = data.dados.id;

        document.getElementById("id_nome_completo").value = data.dados.nome;
        document.getElementById("id_cpf").value = data.dados.cpf;
        document.getElementById("id_telefone").value = data.dados.telefone || "";
        document.getElementById("id_codigo_sisreg").value = data.dados.codigo_sisreg || "";
        document.getElementById("id_ubs_solicitante").value = data.dados.ubs || "";
        document.getElementById("id_data_agendamento_sisreg").value = data.dados.data_agendamento || "";

    } else {
        liberarForm();

        msg.textContent = "Paciente não encontrado. Preencha os dados abaixo.";
        msg.className = "search-status status-warning";

        document.getElementById("paciente_id").value = "";

        document.getElementById("id_nome_completo").value = "";
        document.getElementById("id_cpf").value = "";
        document.getElementById("id_telefone").value = "";
        document.getElementById("id_codigo_sisreg").value = "";
        document.getElementById("id_ubs_solicitante").value = "";
        document.getElementById("id_data_agendamento_sisreg").value = "";
    }
}

document.getElementById("cpf_lookup").addEventListener("keypress", function (event) {
    if (event.key === "Enter") consultarHistorico();
});