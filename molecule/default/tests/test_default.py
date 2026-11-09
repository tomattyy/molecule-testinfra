"""Etapa 5: auditoria independente do estado real da instância Ubuntu."""


def test_nginx_instalado_e_rodando(host):
    """Valida pacote, serviço, habilitação no boot e porta TCP 80."""
    pacote_nginx = host.package("nginx")
    assert pacote_nginx.is_installed, "O pacote nginx não foi instalado"

    servico_nginx = host.service("nginx")
    assert servico_nginx.is_running, "O serviço nginx não está em execução"
    assert servico_nginx.is_enabled, "O serviço nginx não inicia no boot"

    porta_web = host.socket("tcp://0.0.0.0:80")
    assert porta_web.is_listening, "A porta TCP 80 não está escutando"
