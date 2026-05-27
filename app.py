import os
from datetime import datetime, timedelta

import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="EduTrack AI", page_icon="🎓", layout="wide")

XANO_BASE_URL = st.secrets.get("xano_base_url", os.getenv("XANO_BASE_URL", ""))

def api_url(path: str) -> str:
    return f"{XANO_BASE_URL.rstrip('/')}/{path.lstrip('/')}"

def auth_headers() -> dict:
    token = st.session_state.get("auth_token")
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def api_request(method: str, endpoint: str, json=None, params=None, auth=True):
    if not XANO_BASE_URL:
        st.error("Configure Xano base URL in Streamlit secrets as 'xano_base_url' or set XANO_BASE_URL.")
        return None
    url = api_url(endpoint)
    headers = auth_headers() if auth else {"Content-Type": "application/json"}
    try:
        response = requests.request(method, url, headers=headers, json=json, params=params, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(f"API request failed: {exc}")
        if exc.response is not None:
            try:
                st.write(exc.response.json())
            except ValueError:
                st.write(exc.response.text)
        return None

def fetch_current_user():
    user = api_request("GET", "auth/me")
    if user:
        st.session_state["user"] = user
    return user

def login_user(email: str, password: str):
    data = api_request("POST", "auth/login", json={"email": email, "password": password}, auth=False)
    if data and "authToken" in data:
        st.session_state["auth_token"] = data["authToken"]
        st.session_state["user_id"] = data.get("user_id")
        fetch_current_user()
        st.success("Login realizado com sucesso.")
        return True
    return False

def signup_user(name: str, email: str, password: str):
    data = api_request("POST", "auth/signup", json={"name": name, "email": email, "password": password}, auth=False)
    if data and "authToken" in data:
        st.session_state["auth_token"] = data["authToken"]
        st.session_state["user_id"] = data.get("user_id")
        fetch_current_user()
        st.success("Cadastro realizado com sucesso.")
        return True
    return False

def logout_user():
    for key in ["auth_token", "user_id", "user"]:
        if key in st.session_state:
            del st.session_state[key]

def load_subjects():
    subjects = api_request("GET", "subjects")
    return subjects or []

def load_tasks(filters=None):
    params = filters or {}
    tasks = api_request("GET", "academic_tasks", params=params)
    return tasks or []

def create_subject(name: str):
    return api_request("POST", "subjects", json={"name": name})

def archive_subject(subject_id: int):
    return api_request("PATCH", f"subjects/{subject_id}", json={"archived": True})

def delete_subject(subject_id: int):
    return api_request("DELETE", f"subjects/{subject_id}")

def create_task(task_data: dict):
    return api_request("POST", "academic_tasks", json=task_data)

def update_task(task_id: int, data: dict):
    return api_request("PATCH", f"academic_tasks/{task_id}", json=data)

def delete_task(task_id: int):
    return api_request("DELETE", f"academic_tasks/{task_id}")

def update_profile(name: str, email: str):
    return api_request("PATCH", "user/edit_profile", json={"name": name, "email": email})

def request_reset_link(email: str):
    return api_request("GET", f"reset/request-reset-link", params={"email": email}, auth=False)

def display_login():
    st.title("EduTrack AI")
    st.write("Faça login ou cadastre-se para começar a acompanhar suas disciplinas e tarefas.")
    with st.expander("Já tenho conta"):
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Senha", type="password", key="login_password")
            submitted = st.form_submit_button("Entrar")
            if submitted:
                if not login_user(email, password):
                    st.error("Falha no login. Verifique suas credenciais.")
    with st.expander("Criar nova conta"):
        with st.form("signup_form"):
            name = st.text_input("Nome", key="signup_name")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Senha", type="password", key="signup_password")
            submitted = st.form_submit_button("Criar conta")
            if submitted:
                if not signup_user(name, email, password):
                    st.error("Não foi possível criar a conta.")
    with st.expander("Recuperar senha"):
        with st.form("reset_form"):
            reset_email = st.text_input("Email para recuperação", key="reset_email")
            submitted = st.form_submit_button("Enviar link de recuperação")
            if submitted:
                result = request_reset_link(reset_email)
                if result is not None:
                    st.success("Solicitação enviada. Verifique seu email.")
                else:
                    st.error("Falha ao solicitar a recuperação de senha.")

def summary_metrics(subjects: list[dict], tasks: list[dict]) -> dict:
    now = datetime.utcnow()
    active_subjects = [s for s in subjects if not s.get("archived", False)]
    pending_tasks = [t for t in tasks if t.get("status") != "concluida"]
    overdue_tasks = []
    upcoming = []
    completed_tasks = [t for t in tasks if t.get("status") == "concluida"]
    for task in tasks:
        due_date = task.get("due_date")
        try:
            due_dt = datetime.fromisoformat(due_date) if due_date else None
        except ValueError:
            due_dt = None
        if due_dt:
            if due_dt < now and task.get("status") != "concluida":
                overdue_tasks.append(task)
            if 0 <= (due_dt - now).days <= 7:
                upcoming.append(task)
    progress = int((len(completed_tasks) / len(tasks)) * 100) if tasks else 0
    return {
        "active_subjects": len(active_subjects),
        "pending_tasks": len(pending_tasks),
        "overdue_tasks": len(overdue_tasks),
        "upcoming_tasks": len(upcoming),
        "progress": progress,
        "tasks": tasks,
        "completed_tasks": len(completed_tasks),
        "active_subjects_list": active_subjects,
        "upcoming_tasks_list": upcoming,
        "overdue_tasks_list": overdue_tasks,
    }

def dashboard_page():
    st.title("Dashboard")
    subjects = load_subjects()
    tasks = load_tasks()
    metrics = summary_metrics(subjects, tasks)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Disciplinas Ativas", metrics["active_subjects"])
    col2.metric("Tarefas Pendentes", metrics["pending_tasks"])
    col3.metric("Tarefas Atrasadas", metrics["overdue_tasks"])
    col4.metric("Próximas 7 dias", metrics["upcoming_tasks"])
    st.progress(metrics["progress"])
    st.caption(f"Progresso geral: {metrics['progress']}% de {len(tasks)} tarefas concluídas")
    st.markdown("---")
    st.subheader("Próximas tarefas")
    upcoming = metrics["upcoming_tasks_list"]
    if upcoming:
        for task in upcoming[:5]:
            st.write(f"**{task.get('title')}** — Prazo: {task.get('due_date')} — Prioridade: {task.get('priority')}")
    else:
        st.info("Nenhuma tarefa com prazo nos próximos 7 dias.")
    st.markdown("---")
    st.subheader("Tarefas atrasadas")
    if metrics["overdue_tasks_list"]:
        for task in metrics["overdue_tasks_list"][:5]:
            st.warning(f"{task.get('title')} — Prazo: {task.get('due_date')} — Disciplina ID: {task.get('subject_id')}")
    else:
        st.success("Nenhuma tarefa atrasada no momento.")

def subjects_page():
    st.title("Disciplinas")
    subjects = load_subjects()
    with st.expander("Cadastrar nova disciplina"):
        with st.form("new_subject_form"):
            subject_name = st.text_input("Nome da disciplina")
            submitted = st.form_submit_button("Salvar")
            if submitted:
                if subject_name:
                    result = create_subject(subject_name)
                    if result:
                        st.success("Disciplina criada com sucesso.")
                        st.experimental_rerun()
                    else:
                        st.error("Falha ao criar a disciplina.")
                else:
                    st.error("Informe o nome da disciplina.")
    if subjects:
        for subject in subjects:
            with st.expander(f"{subject.get('name')} (ID: {subject.get('id')})"):
                st.write(f"**Criada em:** {subject.get('created_at')}")
                st.write(f"**Arquivada:** {subject.get('archived', False)}")
                col1, col2 = st.columns([1, 1])
                with col1:
                    if not subject.get("archived", False):
                        if st.button("Arquivar disciplina", key=f"archive_{subject['id']}"):
                            confirm = st.checkbox("Confirmar arquivamento", key=f"confirm_archive_{subject['id']}")
                            if confirm:
                                archive_subject(subject["id"])
                                st.success("Disciplina arquivada.")
                                st.experimental_rerun()
                with col2:
                    if st.button("Excluir disciplina", key=f"delete_{subject['id']}"):
                        confirm = st.checkbox("Confirmar exclusão", key=f"confirm_delete_{subject['id']}")
                        if confirm:
                            delete_subject(subject["id"])
                            st.success("Disciplina excluída.")
                            st.experimental_rerun()
    else:
        st.info("Nenhuma disciplina encontrada. Cadastre uma nova disciplina para começar.")

def tasks_page():
    st.title("Tarefas")
    subjects = load_subjects()
    subject_options = {s['name']: s['id'] for s in subjects}
    filters = {}
    st.sidebar.subheader("Filtros")
    subject_filter = st.sidebar.selectbox("Disciplina", ["Todas"] + list(subject_options.keys()))
    status_filter = st.sidebar.selectbox("Status", ["Todas", "pendente", "em_progresso", "concluida"])
    priority_filter = st.sidebar.selectbox("Prioridade", ["Todas", "baixa", "media", "alta"])
    if subject_filter != "Todas":
        filters["subject_id"] = subject_options.get(subject_filter)
    if status_filter != "Todas":
        filters["status"] = status_filter
    if priority_filter != "Todas":
        filters["priority"] = priority_filter
    tasks = load_tasks(filters)
    with st.expander("Criar nova tarefa"):
        with st.form("new_task_form"):
            title = st.text_input("Título")
            description = st.text_area("Descrição")
            due_date = st.date_input("Prazo")
            priority = st.selectbox("Prioridade", ["baixa", "media", "alta"], index=1)
            status = st.selectbox("Status", ["pendente", "em_progresso", "concluida"])
            subject_name = st.selectbox("Disciplina", [""] + list(subject_options.keys()))
            submitted = st.form_submit_button("Salvar tarefa")
            if submitted:
                if title and subject_name:
                    subject_id = subject_options[subject_name]
                    task_data = {
                        "title": title,
                        "description": description,
                        "due_date": due_date.isoformat(),
                        "priority": priority,
                        "status": status,
                        "subject_id": subject_id,
                    }
                    if create_task(task_data):
                        st.success("Tarefa criada com sucesso.")
                        st.experimental_rerun()
                    else:
                        st.error("Falha ao criar tarefa.")
                else:
                    st.error("Título e disciplina são obrigatórios.")
    if tasks:
        grouped = pd.DataFrame(tasks)
        grouped["due_date"] = pd.to_datetime(grouped["due_date"], errors="coerce")
        grouped = grouped.sort_values(by="due_date")
        for _, task in grouped.iterrows():
            status = task.get("status")
            due_date = task.get("due_date")
            st.markdown(f"### {task.get('title')} - {status}")
            st.write(f"**Disciplina ID:** {task.get('subject_id')}  |  **Prazo:** {due_date}")
            st.write(f"**Prioridade:** {task.get('priority')}  |  **Descrição:** {task.get('description')}")
            if st.button("Marcar como Concluída", key=f"complete_{task['id']}"):
                update_task(task['id'], {"status": "concluida"})
                st.success("Tarefa marcada como concluída.")
                st.experimental_rerun()
            if st.button("Excluir tarefa", key=f"delete_task_{task['id']}"):
                confirm = st.checkbox("Confirmar exclusão", key=f"confirm_delete_task_{task['id']}")
                if confirm:
                    delete_task(task['id'])
                    st.success("Tarefa excluída.")
                    st.experimental_rerun()
            st.markdown("---")
    else:
        st.info("Nenhuma tarefa encontrada para os filtros selecionados.")

def reports_page():
    st.title("Relatórios")
    tasks = load_tasks()
    if not tasks:
        st.info("Nenhuma tarefa disponível para gerar relatório.")
        return
    df = pd.DataFrame(tasks)
    df["due_date"] = pd.to_datetime(df["due_date"], errors="coerce")
    start_date = st.date_input("Data inicial", value=datetime.utcnow().date() - timedelta(days=30))
    end_date = st.date_input("Data final", value=datetime.utcnow().date())
    filtered = df[(df["due_date"] >= pd.to_datetime(start_date)) & (df["due_date"] <= pd.to_datetime(end_date))]
    st.write(f"Mostrando {len(filtered)} tarefas entre {start_date} e {end_date}.")
    st.dataframe(filtered[["title", "subject_id", "status", "priority", "due_date"]])
    csv = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Exportar CSV", data=csv, file_name="relatorio_tarefas.csv", mime="text/csv")

def profile_page():
    st.title("Perfil")
    user = st.session_state.get("user") or fetch_current_user()
    if not user:
        st.error("Não foi possível carregar os dados do usuário.")
        return
    st.write(f"**Nome:** {user.get('name')}")
    st.write(f"**Email:** {user.get('email')}")
    with st.form("profile_form"):
        name = st.text_input("Nome", value=user.get("name", ""))
        email = st.text_input("Email", value=user.get("email", ""))
        submitted = st.form_submit_button("Atualizar perfil")
        if submitted:
            result = update_profile(name, email)
            if result:
                st.success("Perfil atualizado com sucesso.")
                fetch_current_user()
            else:
                st.error("Falha ao atualizar perfil.")

def main():
    if "auth_token" not in st.session_state:
        display_login()
        return
    if "user" not in st.session_state:
        fetch_current_user()
    page = st.sidebar.radio("Navegação", ["Dashboard", "Disciplinas", "Tarefas", "Relatórios", "Perfil", "Sair"])
    if page == "Sair":
        if st.button("Confirmar logout"):
            logout_user()
            st.experimental_rerun()
        return
    st.sidebar.markdown("---")
    st.sidebar.write(f"Logado como: {st.session_state.get('user', {}).get('name', 'Usuário')}")
    if page == "Dashboard":
        dashboard_page()
    elif page == "Disciplinas":
        subjects_page()
    elif page == "Tarefas":
        tasks_page()
    elif page == "Relatórios":
        reports_page()
    elif page == "Perfil":
        profile_page()

if __name__ == "__main__":
    main()