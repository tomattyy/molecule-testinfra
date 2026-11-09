# Desafio 01 - Automação e Testes de Infraestrutura

Entrega prática baseada no **Roteiro Prático — Desafio DevOps com Ansible, Molecule e Testinfra**, com as cinco etapas obrigatórias: metadados, tasks, configuração Molecule, convergência e auditoria Testinfra.

## Estrutura

```text
servidor_nginx/
├── meta/
│   └── main.yml
├── tasks/
│   └── main.yml
├── molecule/
│   └── default/
│       ├── molecule.yml
│       ├── converge.yml
│       └── tests/
│           └── test_default.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Pré-requisitos

- Ambiente **Linux** com Python 3.10+ e Docker Engine disponível (`docker info`). Em Windows, use **WSL2 com integração Docker Desktop** ou **GitHub Codespaces**.
- A conta que executará os comandos precisa de permissão para acessar o daemon Docker.
- O uso de `privileged: true` e montagem de cgroups é **apenas para o laboratório de teste de systemd**. Não replique em containers de produção.
- Codespaces deve permitir contêiner privilegiado e as montagens solicitadas; algumas configurações de ambiente hospedado podem bloquear a operação.

## Preparação (dentro da pasta `servidor_nginx`)

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
ansible-galaxy collection install community.docker

docker info
molecule --version
```

> O PDF da atividade sugere `pip install ansible molecule molecule-docker pytest-testinfra`. A opção `molecule-plugins[docker]` substitui o antigo pacote `molecule-docker` em instalações recentes; consultadas as instruções atuais do Molecule. Se sua turma usa versões antigas e compatíveis, respeite as versões fixadas pelo professor.

### Compatibilidade (somente se o seu ambiente exigir)

O roteiro da disciplina orienta exportar a variável abaixo quando aparecer um erro relacionado a condicionais de versões recentes do Ansible e do driver Docker:

```bash
export ANSIBLE_ALLOW_BROKEN_CONDITIONALS=true
```

É uma **solução temporária de compatibilidade**, não uma configuração recomendada para produção. Prefira usar versões compatíveis do Ansible e do plugin; não ative essa variável se não houver necessidade.

## Executar o ciclo completo

```bash
molecule test
```

A sequência definida em `molecule/default/molecule.yml` é:

1. dependency / cleanup / destroy: preparação e descarte de sobras.
2. syntax: valida a sintaxe do playbook.
3. create: cria o contêiner Ubuntu 22.04 com systemd.
4. converge: aplica a role Ansible pela primeira vez.
5. idempotence: reaplica a role e espera `changed=0`.
6. verify: o Testinfra inspeciona pacote, serviço e porta.
7. cleanup / destroy: remove o contêiner temporário.

### Depurar passo a passo

```bash
molecule create
molecule converge
molecule verify
molecule idempotence
molecule destroy
```

> `molecule converge` pode realizar etapas preparatórias automaticamente, conforme a versão. Em caso de erro, use `molecule --debug test` e confira `docker info`, permissões do daemon, suporte a cgroups v2 e acesso à imagem do Docker Hub.

## Como comprovar a conclusão

- **Create:** imagem/contêiner criado com sucesso.
- **Converge:** `failed=0` (o contador `changed` pode variar).
- **Idempotence:** `changed=0`.
- **Verify:** `1 passed` na função Testinfra (quatro asserts no mesmo teste).
- **Destroy:** remoção bem-sucedida do contêiner.

O requisito `privileged: true` foi solicitado pelo material para executar o `systemd` dentro do container; **não exponha o Docker daemon nem execute este laboratório com arquivos desconhecidos**.

## Explicação de cada arquivo

| Arquivo | Papel |
|---|---|
| `meta/main.yml` | Declara o namespace `laboratorio` e o nome `servidor_nginx`. |
| `tasks/main.yml` | Instala o pacote Nginx, inicia e habilita seu serviço. `cache_valid_time` contribui para a idempotência. |
| `molecule/default/molecule.yml` | Orquestra contêiner descartável, converge, idempotence e verify. |
| `molecule/default/converge.yml` | Inclui a role `laboratorio.servidor_nginx`. O nome deve acompanhar o namespace em `meta/main.yml`. |
| `molecule/default/tests/test_default.py` | Audita pacote, serviço e porta 80 usando Testinfra. |

## Fontes e observações

Material didático enviado: **Roteiro Prático — Desafio DevOps com Ansible, Molecule e Testinfra**, **Guia de Testes de Infraestrutura para Iniciantes**, **Automated Infrastructure Testing**.

Documentação oficial: [Molecule - Configuração](https://docs.ansible.com/projects/molecule/configuration/), [Molecule - Instalação](https://docs.ansible.com/projects/molecule/installation/), [Ansible apt](https://docs.ansible.com/projects/ansible/latest/collections/ansible/builtin/apt_module.html), [Testinfra](https://testinfra.readthedocs.io/en/latest/).

**Validação local:** a entrega foi submetida a verificação estática de YAML e de sintaxe Python. O ciclo `molecule test` requer Docker e não foi executado no ambiente de criação desta entrega; os logs esperados são critérios de sucesso, não resultados comprovados.
