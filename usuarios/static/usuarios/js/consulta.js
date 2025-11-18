async function buscarCPF() {
    const cpf = document.getElementById("cpf_lookup").value.trim();
    const msg = document.getElementById("statusBusca");
    const resultados = document.getElementById("resultados"); // div para tabela

    resultados.innerHTML = ""; // limpa resultados antigos

    if (!cpf) {
        msg.textContent = "Digite um CPF antes de buscar.";
        msg.className = "search-status status-warning";
        return;
    }

    msg.textContent = "Buscando...";
    msg.className = "search-status status-info";

    const response = await fetch(`/buscar-ocis/?cpf=${cpf}`);
    const data = await response.json();

    if (data.exists) {
        msg.textContent = "Paciente encontrado!";
        msg.className = "search-status status-success";

        // Data atual para comparação
        const hoje = new Date();

        // Monta tabela de OCIs
        let html = `<h2 class="resultados-title">${data.paciente.nome} (${data.paciente.cpf})</h2>`;
        html += `<table class="tabela-pacientes">
            <thead>
                <tr>
                    <th>Codigo</th>
                    <th>OCI</th>
                    <th>Tipo</th>
                    <th>Médico</th>
                    <th>Abertura</th>
                    <th>Conclusão</th>
                    <th>Data Limite</th>
                </tr>
            </thead>
            <tbody>`;

        if (data.ocis.length > 0) {
            data.ocis.forEach(oci => {
                let classeDataLimite = "";
                if (oci.limite) {
                    const dataLimite = new Date(oci.limite.split("/").reverse().join("-"));
                    if (dataLimite < hoje) {
                        classeDataLimite = "vermelho";
                    }
                }

                html += `<tr>
                    <td>${oci.codigo}</td>
                    <td>${oci.nome}</td>
                    <td>${oci.tipo}</td>
                    <td>${oci.medico}</td>
                    <td>${oci.abertura}</td>
                    <td>${oci.conclusao}</td>
                    <td class="${classeDataLimite}">${oci.limite}</td>
                </tr>`;
            });
        } else {
            html += `<tr><td colspan="7">Nenhuma OCI encontrada para este CPF.</td></tr>`;
        }

        html += `</tbody></table>`;
        resultados.innerHTML = html;

    } else {
        msg.textContent = data.erro || "Paciente não encontrado.";
        msg.className = "search-status status-warning";
    }
}
