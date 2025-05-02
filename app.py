import streamlit as st
from fpdf import FPDF

# Constantes ajustadas
TREINAMENTO_FIXO_MENSAL = 166.67
ALUGUEL_POR_M2 = 42.52
AREA_POR_FUNCIONARIO = 7
ALUGUEL_FUNCIONARIO = ALUGUEL_POR_M2 * AREA_POR_FUNCIONARIO
CUSTO_FIXO_INFRA = 125.00
DEPRECIACAO_MOBILIARIO = 20.00
LIMPEZA_MANUTENCAO = 30.00
EQUIPAMENTOS_TI = 120.00
GESTAO_SUPERVISAO = 200.00
ABSENTEISMO_PERC = 0.10

st.set_page_config(page_title="Calculadora de Custos CLT Aion X", layout="centered")

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Aion X - Inteligência para Redução de Custos", ln=True, align="C")
        self.set_font("Arial", "", 12)
        self.cell(0, 10, "www.aionx.com.br", ln=True, align="C")
        self.ln(5)
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Relatório de Custo de Funcionário Administrativo", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f'Página {self.page_no()}', align="C")

def gerar_pdf(dados):
    empresa = dados["empresa"]
    salario = dados["salario"]
    plano = dados["plano"]
    vt = dados["vt"]
    vr = dados["vr"]
    va = dados["va"]

    # Provisões
    prov13 = salario / 12
    prov_ferias = salario / 12
    adic_ferias = prov_ferias / 3
    total_provisoes = prov13 + prov_ferias + adic_ferias

    # Encargos
    fgts = salario * 0.08
    inss = salario * 0.3344
    total_encargos = fgts + inss

    # Benefícios
    beneficios = plano + vt + vr + va
    subtotal_beneficios = salario + total_provisoes + total_encargos + beneficios

    # Infraestrutura
    infraestrutura = ALUGUEL_FUNCIONARIO + CUSTO_FIXO_INFRA
    operacionais = infraestrutura + DEPRECIACAO_MOBILIARIO + LIMPEZA_MANUTENCAO + EQUIPAMENTOS_TI

    # Treinamento e gestão
    apoio = TREINAMENTO_FIXO_MENSAL + GESTAO_SUPERVISAO

    # Sem perdas
    total_sem_perdas = subtotal_beneficios + operacionais + apoio

    # Absenteísmo
    absenteismo = total_sem_perdas * ABSENTEISMO_PERC
    total_perdas = absenteismo

    # Totais finais
    total_mensal = total_sem_perdas + total_perdas
    total_anual = total_mensal * 12

    # Rescisão
    ferias_vencidas = salario + (salario / 3)
    dec_terceiro = salario
    aviso = salario
    multa_fgts = fgts * 12 * 0.40
    total_rescisao = ferias_vencidas + dec_terceiro + aviso + multa_fgts
    total_geral = total_anual + total_rescisao

    # PDF
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Empresa: {empresa}", ln=True)

    def add_line(txt, val):
        pdf.cell(0, 10, f"{txt}: R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), ln=True)

    pdf.cell(0, 10, "Resumo dos Custos:", ln=True)
    add_line("Salário Base", salario)
    add_line("Provisões Legais", total_provisoes)
    add_line("Encargos Patronais", total_encargos)
    add_line("Benefícios", beneficios)
    add_line("Subtotal até Benefícios", subtotal_beneficios)
    add_line("Infraestrutura e Suporte", operacionais)
    add_line("Treinamento e Gestão", apoio)
    add_line("Absenteísmo (10%)", absenteismo)
    add_line("Custo Mensal Estimado", total_mensal)
    add_line("Custo Anual Estimado", total_anual)

    pdf.ln(5)
    pdf.cell(0, 10, "Provisão para Demissão:", ln=True)
    add_line("Férias + 1/3", ferias_vencidas)
    add_line("13º Salário", dec_terceiro)
    add_line("Aviso Prévio", aviso)
    add_line("Multa FGTS", multa_fgts)
    add_line("Total Rescisório", total_rescisao)
    add_line("Custo Total Anual com Rescisão", total_geral)

    # Explicações
    pdf.add_page()
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Explicações Detalhadas dos Cálculos", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.multi_cell(0, 7,
        f"- Provisões Legais:\n"
        "  * 13º salário: 1/12 do salário base por mês\n"
        "  * Férias: 1/12 do salário base + 1/3 constitucional\n\n"
        "- Encargos:\n"
        "  * INSS Patronal: 33,44% sobre o salário base\n"
        "  * FGTS: 8% sobre o salário base\n\n"
        "- Benefícios:\n"
        "  * Informados manualmente pelo usuário\n\n"
        "- Infraestrutura e Suporte:\n"
        f"  * Aluguel: 7 m² × R$ {ALUGUEL_POR_M2}/m² = R$ {ALUGUEL_FUNCIONARIO:.2f}\n"
        f"  * Água, energia, internet (fixo): R$ {CUSTO_FIXO_INFRA:.2f}\n"
        "  * Depreciação mobiliário: R$ 20,00/mês\n"
        "  * Limpeza/manutenção: R$ 30,00/mês\n"
        "  * TI: R$ 120,00/mês (hardware, licenças, suporte)\n\n"
        "- Treinamento e Gestão:\n"
        "  * Treinamento: R$ 166,67/mês\n"
        "  * Gestão/Supervisão: R$ 200,00/mês\n\n"
        "- Absenteísmo:\n"
        "  * 10% sobre o custo sem perdas\n\n"
        "- Verbas Rescisórias:\n"
        "  * Incluem férias vencidas + 1/3, 13º, aviso prévio e multa de 40% sobre FGTS"
    )

    pdf_output = "relatorio_aionx.pdf"
    pdf.output(pdf_output)
    return pdf_output

# Interface Streamlit
st.markdown("### 🧾 Calculadora de Custo CLT - Aion X")
st.markdown("Preencha os campos abaixo para gerar o relatório completo em PDF:")

with st.form("dados_funcionario"):
    empresa = st.text_input("Nome da empresa atendida")
    salario = st.number_input("Salário Base (R$)", min_value=0.0, step=100.0, format="%.2f")
    plano = st.number_input("Plano de Saúde (R$)", min_value=0.0, step=10.0, format="%.2f")
    vt = st.number_input("Vale Transporte (R$)", min_value=0.0, step=10.0, format="%.2f")
    vr = st.number_input("Vale Refeição (R$)", min_value=0.0, step=10.0, format="%.2f")
    va = st.number_input("Vale Alimentação (R$)", min_value=0.0, step=10.0, format="%.2f")
    submitted = st.form_submit_button("Gerar Relatório 📄")

if submitted:
    dados = {
        "empresa": empresa,
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
