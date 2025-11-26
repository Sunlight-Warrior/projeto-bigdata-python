import matplotlib.pyplot as plt
import pandas as pd

# Lendo os arquivos CSV
df_roubos = pd.read_csv('roubo.csv', sep=';', decimal=',')
df_populacao = pd.read_csv('populacao.csv')
df_salarios = pd.read_csv('salariomedia.csv', sep=';', decimal=',')
df_faixa_etaria = pd.read_csv('População_Residente_por_Sexo_Faixa_Etária.csv', sep=';', decimal=',', encoding='latin-1')
df_imoveis = pd.read_csv('imovel.csv')

# Definindo cores fixas para cada bairro (para gráficos de barras simples)
CORES_BAIRROS = {
    'Santa Cruz': '#1f77b4',
    'Jacarepaguá': '#ff7f0e', 
    'Barra da Tijuca': '#2ca02c',
    'Bangu': '#d62728',
    'Realengo': '#9467bd',
    'Campo Grande': '#d5d83d'
}

BAIRROS_SELECIONADOS = ['Santa Cruz', 'Jacarepaguá', 'Barra da Tijuca', 'Bangu', 'Realengo', 'Campo Grande']

class GraphSlider:
    def __init__(self):
        self.fig = plt.figure(figsize=(14, 8))
        self.current_slide = 0
        self.total_slides = 6 
        
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.create_slides()
        
    # CRIA O PRIMEIRO DISPLAY
    def create_slides(self):
        ax = self.fig.add_subplot(111)
        self.create_total_population_chart(ax)
        ax.set_title('População Total por Bairro - IBGE 2022', fontsize=16, fontweight='bold', pad=20)
        self.fig.suptitle('Figura 1', fontsize=18, fontweight='bold')

    # SLIDE 1 — TOTAL DE POPULAÇÃO
    def create_total_population_chart(self, ax):
        df_filtrado = df_populacao[df_populacao['bairro'].isin(BAIRROS_SELECIONADOS)]

        df_filtrado = df_filtrado.copy()
        df_filtrado['Total'] = df_filtrado['Homens/2022'] + df_filtrado['Mulheres/2022']
        df_filtrado = df_filtrado.sort_values('Total', ascending=False)

        x_pos = range(len(df_filtrado))
        cores = [CORES_BAIRROS[bairro] for bairro in df_filtrado['bairro']]

        bars = ax.bar(
            x_pos, df_filtrado['Total'],
            color=cores,
            edgecolor='black',
            linewidth=2,
            alpha=0.9
        )

        for bar, value in zip(bars, df_filtrado['Total']):
            ax.text(
                bar.get_x() + bar.get_width()/2,
                bar.get_height() + (value * 0.02),
                f'{value:,.0f}'.replace(',', '.'),
                ha='center',
                va='bottom',
                fontsize=12,
                fontweight='bold'
            )

        ax.set_xticks(x_pos)
        ax.set_xticklabels(df_filtrado['bairro'])
        ax.set_xlabel('Bairros', fontsize=12, fontweight='bold')
        ax.set_ylabel('População Total', fontsize=12, fontweight='bold')
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_ylim(0, df_filtrado['Total'].max() * 1.15)

    # SLIDE 2 — HOMENS x MULHERES
    def create_gender_chart(self, ax):
        df_filtrado = df_populacao[df_populacao['bairro'].isin(BAIRROS_SELECIONADOS)]

        df_filtrado = df_filtrado.copy()
        df_filtrado['Total'] = df_filtrado['Homens/2022'] + df_filtrado['Mulheres/2022']
        df_filtrado = df_filtrado.sort_values('Total', ascending=False)

        x_pos = range(len(df_filtrado))
        largura = 0.35
        bars_h = ax.bar(
            [x - largura/2 for x in x_pos],
            df_filtrado['Homens/2022'],
            width=largura,
            label='Homens',
            color='#1f77b4',
            edgecolor='black',
            alpha=0.9
        )

        bars_m = ax.bar(
            [x + largura/2 for x in x_pos],
            df_filtrado['Mulheres/2022'],
            width=largura,
            label='Mulheres',
            color='#e377c2',
            edgecolor='black',
            alpha=0.9
        )

        for bars, values in [(bars_h, df_filtrado['Homens/2022']),
                             (bars_m, df_filtrado['Mulheres/2022'])]:
            for bar, value in zip(bars, values):
                ax.text(
                    bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 3000,
                    f'{value:,.0f}'.replace(',', '.'),
                    ha='center',
                    fontsize=12,
                    fontweight='bold'
                )

        ax.set_xticks(x_pos)
        ax.set_xticklabels(df_filtrado['bairro'])
        ax.set_xlabel('Bairros',fontsize=12,fontweight='bold')
        ax.set_ylabel('População',fontsize=12,fontweight='bold')
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.3)

        maxp = max(df_filtrado['Homens/2022'].max(), df_filtrado['Mulheres/2022'].max())
        ax.set_ylim(0, maxp * 1.15)

    # SLIDE 3 — HOMENS E MULHERES 15-50 ANOS
    def create_gender_15_50_chart(self, ax):
        df_filtrado = df_faixa_etaria[df_faixa_etaria['bairro'].isin(BAIRROS_SELECIONADOS)]
        
        # Calcular total de homens entre 15 e 50 anos
        colunas_homens_15_50 = [
            'Sexo masculino, 15 a 19 anos',
            'Sexo masculino, 20 a 24 anos', 
            'Sexo masculino, 25 a 29 anos',
            'Sexo masculino, 30 a 39 anos',
            'Sexo masculino, 40 a 49 anos'
        ]
        
        # Calcular total de mulheres entre 15 e 50 anos
        colunas_mulheres_15_50 = [
            'Sexo feminino, 15 a 19 anos',
            'Sexo feminino, 20 a 24 anos', 
            'Sexo feminino, 25 a 29 anos',
            'Sexo feminino, 30 a 39 anos',
            'Sexo feminino, 40 a 49 anos'
        ]
        
        df_filtrado = df_filtrado.copy()
        df_filtrado['Homens_15_50'] = df_filtrado[colunas_homens_15_50].sum(axis=1)
        df_filtrado['Mulheres_15_50'] = df_filtrado[colunas_mulheres_15_50].sum(axis=1)
        df_filtrado['Total_15_50'] = df_filtrado['Homens_15_50'] + df_filtrado['Mulheres_15_50']
        df_filtrado = df_filtrado.sort_values('Total_15_50', ascending=True)
        
        y_pos = range(len(df_filtrado))
        altura = 0.35
        bars_h = ax.barh(
            [y - altura/2 for y in y_pos],
            df_filtrado['Homens_15_50'],
            height=altura,
            label='Homens 15-50 anos',
            color='#1f77b4',  # Azul
            edgecolor='black',
            alpha=0.9
        )

        bars_m = ax.barh(
            [y + altura/2 for y in y_pos],
            df_filtrado['Mulheres_15_50'],
            height=altura,
            label='Mulheres 15-50 anos',
            color='#e377c2',  # Rosa
            edgecolor='black',
            alpha=0.9
        )

        for bars, values in [(bars_h, df_filtrado['Homens_15_50']),
                             (bars_m, df_filtrado['Mulheres_15_50'])]:
            for bar, value in zip(bars, values):
                ax.text(
                    bar.get_width() + 500,
                    bar.get_y() + bar.get_height()/2,
                    f'{value:,.0f}'.replace(',', '.'),
                    ha='left',
                    va='center',
                    fontsize=12,
                    fontweight='bold'
                )

        ax.set_yticks(y_pos)
        ax.set_yticklabels(df_filtrado['bairro'])
        ax.set_ylabel('Bairros', fontsize=12, fontweight='bold')
        ax.set_xlabel('População 15-50 anos', fontsize=12, fontweight='bold')
        ax.legend()
        ax.grid(axis='x', linestyle='--', alpha=0.3)

        maxp = max(df_filtrado['Homens_15_50'].max(), df_filtrado['Mulheres_15_50'].max())
        ax.set_xlim(0, maxp * 1.15)

    # SLIDE 4 — SALÁRIOS MÉDIOS
    def create_salary_chart(self, ax):
        df_filtrado = df_salarios[df_salarios['bairro'].isin(BAIRROS_SELECIONADOS)]
        
        # Ordenar por valor médio
        df_filtrado = df_filtrado.sort_values('valor médio', ascending=False)
        
        x_pos = range(len(df_filtrado))
        
        cores = [CORES_BAIRROS[bairro] for bairro in df_filtrado['bairro']]

        bars = ax.bar(
            x_pos, df_filtrado['valor médio'],
            color=cores,
            edgecolor='black',
            linewidth=2,
            alpha=0.9
        )

        for bar, value in zip(bars, df_filtrado['valor médio']):
            ax.text(
                bar.get_x() + bar.get_width()/2,
                bar.get_height() + 50,
                f'R$ {value:,.0f}'.replace(',', '.'),
                ha='center',
                va='bottom',
                fontsize=12,
                fontweight='bold'
            )

        ax.set_xticks(x_pos)
        ax.set_xticklabels(df_filtrado['bairro'])
        ax.set_xlabel('Bairros', fontsize=12, fontweight='bold')
        ax.set_ylabel('Salário Médio (R$)', fontsize=12, fontweight='bold')
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_ylim(0, df_filtrado['valor médio'].max() * 1.15)

    # SLIDE 5 — ROUBOS
    def create_robbery_chart(self, ax):
        cores = [CORES_BAIRROS[bairro] for bairro in df_roubos['Bairros']]

        bars = ax.barh(
            df_roubos['Bairros'],
            df_roubos['Média'],
            color=cores,
            alpha=0.85,
            edgecolor='black'
        )

        for bar in bars:
            v = bar.get_width()
            ax.text(v + 2, bar.get_y() + bar.get_height()/2,
                    f'{v:.0f}', va='center',
                    fontsize=12,
                    fontweight='bold')

        ax.set_xlabel('Média de Roubos',fontsize=12,fontweight='bold')
        ax.set_ylabel('Bairros',fontsize=12, fontweight='bold')
        ax.grid(axis='x', linestyle='--', alpha=0.3)
        ax.set_xlim(0, df_roubos['Média'].max() * 1.15)

    # SLIDE 6 — VALOR MÉDIO DE IMÓVEIS NÃO RESIDENCIAIS
    def create_property_value_chart(self, ax):
        # Filtrar apenas imóveis não residenciais
        df_nao_residencial = df_imoveis[df_imoveis['uso'] == 'NAO RESIDENCIAL']
        
        # Mapear os nomes dos bairros do dataset de imóveis para os bairros selecionados
        bairros_mapeamento = {
            'Santa Cruz': 'Santa Cruz',
            'Jacarepaguá': 'Jacarepaguá', 
            'Barra da Tijuca': 'Barra da Tijuca',
            'Bangu': 'Bangu',
            'Realengo': 'Realengo',
            'Campo Grande': 'Campo Grande'
        }
        
        # Filtrar apenas os bairros selecionados
        df_filtrado = df_nao_residencial[df_nao_residencial['bairro'].str.strip().isin(bairros_mapeamento.keys())]
        
        # Calcular a média do valor do imóvel por bairro
        df_medias = df_filtrado.groupby('bairro')['média_valor_imóvel'].mean().reset_index()
        
        # Ordenar por valor médio (do maior para o menor)
        df_medias = df_medias.sort_values('média_valor_imóvel', ascending=True)
        
        # Usar cores fixas para cada bairro
        cores = [CORES_BAIRROS[bairro.strip()] for bairro in df_medias['bairro']]

        bars = ax.barh(
            df_medias['bairro'],
            df_medias['média_valor_imóvel'],
            color=cores,
            alpha=0.85,
            edgecolor='black'
        )
        for bar in bars:
            v = bar.get_width()
            ax.text(v + (v * 0.01),
                   bar.get_y() + bar.get_height()/2,
                   f'R$ {v:,.0f}'.replace(',', '.'),
                   va='center',
                   fontsize=12,
                   fontweight='bold')

        ax.set_xlabel('Média de valores de Imóveis Não Residenciais (R$)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Bairros', fontsize=12, fontweight='bold')
        ax.grid(axis='x', linestyle='--', alpha=0.3)
        max_valor = df_medias['média_valor_imóvel'].max()
        ax.set_xlim(0, max_valor * 1.15)

    
    # NAVEGAÇÃO
   
    def on_key_press(self, event):
        if event.key in ('right', ' '):
            self.next_slide()
        elif event.key == 'left':
            self.previous_slide()
        elif event.key == 'escape':
            plt.close()

    def next_slide(self):
        if self.current_slide < self.total_slides - 1:
            self.current_slide += 1
            self.update_slide()

    def previous_slide(self):
        if self.current_slide > 0:
            self.current_slide -= 1
            self.update_slide()

    def update_slide(self):
        self.fig.clear()

        ax = self.fig.add_subplot(111)

        if self.current_slide == 0:
            self.create_total_population_chart(ax)
            ax.set_title('População Total por Bairro - IBGE 2022', fontsize=16, fontweight='bold', pad=20)
            self.fig.suptitle('Figura 1', fontsize=18, fontweight='bold')

        elif self.current_slide == 1:
            self.create_gender_chart(ax)
            ax.set_title('Homens e Mulheres por Bairro - IBGE 2022', fontsize=16, fontweight='bold', pad=20)
            self.fig.suptitle('Figura 2', fontsize=18, fontweight='bold')

        elif self.current_slide == 2:
            self.create_gender_15_50_chart(ax)
            ax.set_title('Homens e Mulheres entre 15 e 50 anos por Bairro - IBGE 2022', fontsize=16, fontweight='bold', pad=20)
            self.fig.suptitle('Figura 3', fontsize=18, fontweight='bold')

        elif self.current_slide == 3:
            self.create_salary_chart(ax)
            ax.set_title('Salário Médio Mensal por Bairro - Data Rio 2022', fontsize=16, fontweight='bold', pad=20)
            self.fig.suptitle('Figura 4', fontsize=18, fontweight='bold')

        elif self.current_slide == 4:
            self.create_robbery_chart(ax)
            ax.set_title('Média de Roubos por bairro - Jornal O Globo 2024', fontsize=16, fontweight='bold', pad=20)
            self.fig.suptitle('Figura 5', fontsize=18, fontweight='bold')

        elif self.current_slide == 5:
            self.create_property_value_chart(ax)
            ax.set_title('Média de valores de Imóveis Não Residenciais - Data Rio 2022', fontsize=16, fontweight='bold', pad=20)
            self.fig.suptitle('Figura 6', fontsize=18, fontweight='bold')

        self.fig.tight_layout()
        self.fig.canvas.draw()

    def show(self):
        plt.tight_layout()
        plt.show()

slider = GraphSlider()
slider.show()