import streamlit as st
from fpdf import FPDF

# Percentuais fixos
P_INFRA = 0.247
P_TREIN = 0.093
P_FALHAS = 0.20

st.set_page_config(page_title="Calculadora Aion X", layout="centered")

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Relatório de Custo de Funcionário Administrativo", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f'Página {self.page_no()}', align="C")

def gerar_pdf(dados):
    salario = dados["salario"]
    plano = dados["plano"]
    vt = dados["vt"]
    vr = dados["vr"]
    va = dados["va"]

    prov13 = salario / 12
    prov_ferias = salario / 12
    adic_ferias = prov_ferias / 3
    total_provisoes = prov13 + prov_ferias + adic_ferias

    fgts = salario * 0.08
    inss = salario * 0.3344
    total_encargos = fgts + inss
    beneficios = plano + vt + vr + va

    infra = salario * P_INFRA
    treinamento = salario * P_TREIN
    falhas = salario * P_FALHAS

    total_fixo = salario + total_provisoes + total_encargos
    total_mensal = total_fixo + beneficios + infra + treinamento + falhas
    total_anual = total_mensal * 12

    ferias_vencidas = salario + (salario / 3)
    dec_terceiro = salario
    aviso = salario
    multa_fgts = fgts * 12 * 0.40
    total_rescisao = ferias_vencidas + dec_terceiro + aviso + multa_fgts
    total_geral = total_anual + total_rescisao

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", '', 12)

    def add_line(txt, val):
        pdf.cell(0, 10, f"{txt}: R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), ln=True)

    pdf.cell(0, 10, "Resumo dos Custos:", ln=True)
    add_line("Salário Base", salario)
    add_line("Provisões Legais", total_provisoes)
    add_line("Encargos", total_encargos)
    add_line("Benefícios", beneficios)
    add_line("Infraestrutura (24,7%)", infra)
    add_line("Treinamento (9,3%)", treinamento)
    add_line("Falhas Humanas (20%)", falhas)
    add_line("Total Mensal", total_mensal)
    add_line("Total Anual", total_anual)
    pdf.ln(5)
    pdf.cell(0, 10, "Verbas Rescisórias:", ln=True)
    add_line("Férias + 1/3", ferias_vencidas)
    add_line("13º Salário", dec_terceiro)
    add_line("Aviso Prévio", aviso)
    add_line("Multa FGTS", multa_fgts)
    add_line("Total Rescisório", total_rescisao)
    add_line("Custo Total Anual com Rescisão", total_geral)

    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Explicações Detalhadas dos Cálculos", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7,
        "- Provisões legais: 13º, férias, adicional de 1/3.\n"
        "- Encargos: FGTS (8%), INSS patronal (33,44%).\n"
        "- Benefícios: Informados pelo usuário.\n"
        "- Infraestrutura: 24,7% do salário base (Campinas/SP).\n"
        "- Treinamento: 9,3% do salário.\n"
        "- Falhas Humanas: 20%.\n"
        "- Verbas Rescisórias: férias vencidas + 1/3, 13º, aviso, FGTS."
    )

    pdf_output = "relatorio_aionx.pdf"
    pdf.output(pdf_output)
    return pdf_output

# UI
st.markdown("### 🧾 Calculadora de Custo CLT")
st.markdown("Preencha os campos abaixo para gerar o relatório detalhado em PDF:")

with st.form("dados_funcionario"):
    salario = st.number_input("Salário Base (R$)", min_value=0.0, step=100.0, format="%.2f")
    plano = st.number_input("Plano de Saúde (R$)", min_value=0.0, step=10.0, format="%.2f")
    vt = st.number_input("Vale Transporte (R$)", min_value=0.0, step=10.0, format="%.2f")
    vr = st.number_input("Vale Refeição (R$)", min_value=0.0, step=10.0, format="%.2f")
    va = st.number_input("Vale Alimentação (R$)", min_value=0.0, step=10.0, format="%.2f")
    submitted = st.form_submit_button("Gerar Relatório 📄")

if submitted:
    dados = {
        "salario": salario,
        "plano": plano,
        "vt": vt,
        "vr": vr,
        "va": va
    }
    arquivo = gerar_pdf(dados)
    with open(arquivo, "rb") as f:
        st.success("✅ Relatório gerado com sucesso!")
        st.download_button("⬇️ Baixar PDF", f, file_name="relatorio_aionx.pdf")
