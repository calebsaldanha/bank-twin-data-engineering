#!/bin/bash

echo "=== Iniciando Instalação Completa do Artigo Meridian ==="

# 1. RESTAURAÇÃO DE BACKUP (Para evitar duplicação)
if [ -f index.html.bak ]; then
    echo "Restaurando index.html original..."
    cp index.html.bak index.html
else
    echo "Criando backup de index.html..."
    cp index.html index.html.bak
fi

if [ -f style.css.bak ]; then
    echo "Restaurando style.css original..."
    cp style.css.bak style.css
else
    echo "Criando backup de style.css..."
    cp style.css style.css.bak
fi

if [ -f script.js.bak ]; then
    echo "Restaurando script.js original..."
    cp script.js.bak script.js
else
    echo "Criando backup de script.js..."
    cp script.js script.js.bak
fi

# ==========================================
# 2. DEFINIR O CONTEÚDO HTML COMPLETO
# ==========================================
cat > article_content.tmp << 'HTMLCONTENT'
    <section id="articles" class="articles">
        <div class="container">
            <h2 class="section-title">Artigos Técnicos</h2>
            
            <div class="articles-grid">
                <div class="article-card" data-article="article1">
                    <div class="article-content">
                        <div class="article-meta">
                            <span class="article-category">Data Science / Econometria</span>
                            <span class="article-date">Dez 2025</span>
                        </div>
                        <h3>Meridian: Uma Abordagem Bayesiana Hierárquica para MMM</h3>
                        <p>Uma reconstrução teórica da arquitetura matemática do framework do Google, abordando Adstock Geométrico, Saturação Hill e Priors de Calibração.</p>
                        <a href="javascript:void(0);" class="read-more-btn">Ler Artigo Completo <i class="fas fa-arrow-right"></i></a>
                    </div>
                </div>
            </div>

            <div id="article1" class="article-detail">
                <div class="detail-header">
                    <h3>Meridian: Framework MMM Bayesiano</h3>
                    <button class="close-article">&times;</button>
                </div>
                <div class="detail-content article-body">
                    
                    <div class="article-note" style="background: #f8f9fa; padding: 20px; border-left: 4px solid #3a6ea5; margin-bottom: 30px; border-radius: 4px;">
                        <p style="margin-bottom: 10px; color: #2c3e50;"><strong>Nota Técnica e Contextualização:</strong></p>
                        <p style="font-style: italic; font-size: 0.95rem; color: #555;">
                            Este artigo apresenta uma <strong>análise independente e uma reconstrução teórica</strong> da arquitetura matemática do framework "Meridian", baseada exclusivamente na documentação técnica de código aberto (Open Source) e em papers acadêmicos publicados pela equipe de pesquisa do Google.
                        </p>
                        <p style="font-style: italic; font-size: 0.95rem; color: #555; margin-bottom: 0;">
                            O objetivo deste estudo é demonstrar a aplicação prática de conceitos avançados de estatística Bayesiana e modelagem hierárquica na resolução de problemas modernos de mensuração de marketing. O autor não possui vínculo com o desenvolvimento proprietário da ferramenta, servindo este texto como material educativo e de análise de engenharia reversa conceitual.
                        </p>
                    </div>

                    <h4>Resumo</h4>
                    <p>Este artigo apresenta a estrutura teórica e matemática do Meridian, o <em>framework</em> de Marketing Mix Modeling (MMM) desenvolvido pelo Google. Em contraste com modelos determinísticos ou baseados em cookies, o Meridian utiliza regressão Bayesiana Hierárquica em nível geográfico para inferir causalidade em dados agregados. O modelo incorpora funções de transformação de mídia (Adstock Geométrico e Saturação Hill), priors informativos para calibração via experimentos de incrementalidade e quantificação de incerteza através de amostragem MCMC (<em>Markov Chain Monte Carlo</em>). Discutimos as equações fundamentais, a parametrização dos efeitos de mídia e a otimização orçamentária sob retornos decrescentes.</p>

                    <h4>1. Introdução</h4>
                    <p>Com a depreciação de identificadores de terceiros e o aumento das restrições de privacidade (GDPR, ATT), a atribuição granular (MTA) perde precisão. O Marketing Mix Modeling (MMM) ressurge como a metodologia padrão para mensuração de eficácia de mídia, pois utiliza dados agregados e não requer rastreamento individual.</p>
                    <p>O <strong>Modelo Meridian</strong> inova ao propor uma arquitetura que resolve as limitações clássicas do MMM (colinearidade, falta de causalidade) através de dois pilares:</p>
                    <ul>
                        <li><strong>Modelagem Geo-Level:</strong> Uso de dados seccionados por geografia (ex: Estados, DMAs) para aumentar o tamanho da amostra e variância do sinal.</li>
                        <li><strong>Inferência Bayesiana:</strong> Incorporação de conhecimento prévio (Priors) derivados de experimentos de incrementalidade para restringir o espaço de soluções.</li>
                    </ul>

                    <h4>2. Especificação do Modelo</h4>
                    <p>O Meridian é formulado como um modelo de regressão aditiva, onde a variável resposta (KPI) é decomposta em tendência, sazonalidade, efeitos de mídia e variáveis de controle.</p>

                    <h5>2.1 Equação Geral do Modelo</h5>
                    <p>Seja $Y_{g,t}$ o KPI de interesse (vendas, conversões) na geografia $g$ e tempo $t$. O modelo é definido como:</p>
                    
                    $$Y_{g,t} = \underbrace{\tau_{g,t}}_{\text{Tendência}} + \underbrace{\sum_{m=1}^{M} \beta_{g,m} \cdot f_m(x_{g,t,m})}_{\text{Efeitos de Mídia}} + \underbrace{\sum_{c=1}^{C} \gamma_{g,c} \cdot z_{g,t,c}}_{\text{Variáveis de Controle}} + \epsilon_{g,t}$$

                    <p>Onde:</p>
                    <ul>
                        <li>$\tau_{g,t}$: Componente de tendência e sazonalidade.</li>
                        <li>$x_{g,t,m}$: Execução de mídia bruta (impressões, gasto) do canal $m$.</li>
                        <li>$f_m(\cdot)$: Função de transformação não-linear (Adstock e Saturação).</li>
                        <li>$z_{g,t,c}$: Variáveis de controle (preço, competidores, feriados).</li>
                        <li>$\epsilon_{g,t}$: Termo de erro, tipicamente $\epsilon_{g,t} \sim \text{Normal}(0, \sigma^2)$.</li>
                    </ul>

                    <h4>3. Transformação de Variáveis de Mídia</h4>
                    <p>O Meridian modela a "física" da publicidade: o efeito de um anúncio não é instantâneo nem linear.</p>

                    <h5>3.1 Efeito de Defasagem (Adstock)</h5>
                    <p>O conceito de Adstock captura o efeito residual da publicidade ao longo do tempo (memória do consumidor). O Meridian utiliza, primariamente, o <strong>Adstock Geométrico</strong>.</p>
                    <p>Seja $x_{t}$ o investimento no tempo $t$, o estoque de mídia acumulado $A_t$ é:</p>
                    $$A(x_{t}, \alpha) = x_{t} + \alpha \cdot A(x_{t-1}, \alpha)$$
                    <ul>
                        <li><strong>$\alpha$ (Taxa de Decaimento):</strong> Parâmetro entre $0$ e $1$. Se $\alpha = 0.8$, 80% do efeito do anúncio persiste na semana seguinte.</li>
                        <li>No modelo Bayesiano, $\alpha$ é tratado como uma variável aleatória com uma distribuição <em>Beta</em> como prior: $\alpha \sim \text{Beta}(a, b)$.</li>
                    </ul>

                    <h5>3.2 Efeito de Saturação (Hill Function)</h5>
                    <p>Para modelar os retornos decrescentes (onde o ROI marginal cai à medida que o investimento aumenta), o Meridian aplica a função de Hill sobre o Adstock transformado.</p>
                    $$Hill(A_t; K, S) = \frac{1}{1 + \left( \frac{K}{A_t} \right)^S}$$
                    <p>Onde:</p>
                    <ul>
                        <li><strong>$A_t$</strong>: Mídia transformada pelo Adstock.</li>
                        <li><strong>$S$ (Slope/Forma):</strong> Controla a inclinação da curva em "S". $S > 1$ indica curva em S; $S \leq 1$ indica curva C (côncava).</li>
                        <li><strong>$K$ (Half-Saturation Point):</strong> O ponto onde a resposta atinge 50% do seu valor máximo.</li>
                    </ul>
                    <p>A combinação completa para um canal de mídia $m$ no modelo é:</p>
                    $$Contribution_m = \mu_m \times Hill(Adstock(x_{m}), K_m, S_m)$$

                    <h4>4. Estrutura Bayesiana Hierárquica</h4>
                    <p>A principal vantagem técnica do Meridian é o tratamento hierárquico dos parâmetros. Isso permite que o modelo "aprenda" padrões nacionais enquanto respeita as particularidades regionais (<em>Partial Pooling</em>).</p>

                    <h5>4.1 Hierarquia Geográfica</h5>
                    <p>Para um coeficiente de mídia $\beta_{g,m}$ (eficiência do canal $m$ na geografia $g$), assumimos que ele vem de uma distribuição comum (população nacional):</p>
                    $$
                    \begin{aligned}
                    \beta_{g,m} &\sim \text{LogNormal}(\mu_m, \sigma_m) \\
                    \mu_m &\sim \text{Normal}(\dots) \\
                    \sigma_m &\sim \text{HalfNormal}(\dots)
                    \end{aligned}
                    $$
                    <p>Isso permite o <em>Partial Pooling</em>, onde geografias menores aprendem com a média nacional.</p>

                    <h5>4.2 Amostragem MCMC</h5>
                    <p>O Meridian resolve essas equações complexas não analiticamente, mas computacionalmente, usando o amostrador <strong>NUTS (No-U-Turn Sampler)</strong>, um tipo de <em>Hamiltonian Monte Carlo</em>. Isso gera milhares de cenários plausíveis (distribuição posterior) para cada parâmetro, permitindo intervalos de credibilidade.</p>

                    <h4>5. Calibração com Experimentos (ROI Priors)</h4>
                    <p>Um dos diferenciais críticos do Meridian documentado pelo Google é a capacidade de usar "Ground Truth" para corrigir o modelo. MMMs tradicionais sofrem com correlações espúrias. O Meridian resolve isso injetando resultados de Testes A/B ou Geo-Experiments nos <strong>Priors</strong> do ROI.</p>

                    <h5>5.1 Formulação do Prior de ROI</h5>
                    <p>Se um experimento de incrementalidade indicou que o canal <em>Search</em> tem um ROI de 4.0 com erro padrão de 0.5, o Meridian permite configurar o Prior do coeficiente $\beta_{Search}$ para refletir isso.</p>
                    <p>A relação matemática é:</p>
                    $$ROI_{m} = \frac{\sum \text{Contribuição Marginal}_m}{\sum \text{Custo}_m}$$
                    <p>O modelo penaliza soluções onde o ROI inferido se desvia significativamente do ROI experimental, equilibrando a verossimilhança dos dados históricos com a evidência experimental.</p>
                    $$P(\theta | Data) \propto P(Data | \theta) \times P_{calibração}(\theta)$$

                    <h4>6. Otimização Orçamentária</h4>
                    <p>Com a curva de resposta $f_m(x)$ estimada para cada canal, o objetivo final é encontrar o vetor de investimento $X^* = [x_1, \dots, x_M]$ que maximiza a receita total, sujeito a uma restrição orçamentária $B$.</p>

                    <h5>6.1 Problema de Otimização Restrita</h5>
                    $$
                    \begin{aligned}
                    \text{Maximizar } & \sum_{m=1}^{M} Response_m(x_m) \\
                    \text{Sujeito a } & \sum_{m=1}^{M} x_m \leq B \\
                    & L_m \leq x_m \leq U_m
                    \end{aligned}
                    $$
                    <p>Onde $L_m$ e $U_m$ são limites inferiores e superiores de gasto para evitar extrapolação da curva de Hill para regiões não observadas. O Meridian resolve isso usando otimizadores de gradiente (como SLSQP) sobre a superfície de resposta média posterior.</p>

                    <h4>7. Conclusão</h4>
                    <p>O Modelo Meridian representa o estado da arte em MMM, transicionando da econometria frequentista tradicional para a inferência Bayesiana computacional. Ao modelar explicitamente a hierarquia geográfica e as transformações não-lineares de Adstock/Saturação, e ao permitir a injeção de priors experimentais, o Meridian oferece um caminho robusto para mensuração de causalidade em um ecossistema sem cookies. A transparência do código <em>open-source</em> permite que cientistas de dados validem e adaptem as premissas matemáticas, garantindo que o modelo reflita a realidade do negócio e não seja uma "caixa preta".</p>
                    
                    <div class="article-footer">
                        <h5>Referências Bibliográficas e Documentação</h5>
                        <ul>
                            <li><strong>Google (2024).</strong> <em>Meridian: A Bayesian Mixed Marketing Modeling (MMM) Framework</em>. Google Open Source Documentation.</li>
                            <li><strong>Jin, Y., et al. (2017).</strong> <em>Bayesian Methods for Media Mix Modeling with Carryover and Shape Effects</em>. Google Research. (O <em>paper</em> seminal que fundamenta a matemática de Adstock/Hill usada no Meridian).</li>
                            <li><strong>McElreath, R. (2020).</strong> <em>Statistical Rethinking: A Bayesian Course with Examples in R and Stan</em>. CRC Press. (Fundamentação para a modelagem hierárquica e priors).</li>
                            <li><strong>Tellis, G. J. (2006).</strong> <em>Modeling Marketing Mix</em>. Handbook of Marketing Research. (Teoria clássica de Saturação e Adstock).</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </section>
HTMLCONTENT

# ==========================================
# 3. ATUALIZAR INDEX.HTML
# ==========================================
echo "Atualizando index.html..."

# Remover links antigos
sed -i '/MathJax-script/d' index.html
sed -i '/polyfill.io/d' index.html

# Configuração ROBUSTA do MathJax
cat > mathjax_config.tmp << 'JS'
    <script>
    window.MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\(', '\\)']],
        displayMath: [['$$', '$$'], ['\\[', '\\]']],
        processEscapes: true
      },
      startup: {
        typeset: false
      }
    };
    </script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
JS

# Inserir MathJax no head
sed -i '/<link rel="stylesheet" href="style.css">/i PLACEHOLDER_MATH' index.html
sed -i '/PLACEHOLDER_MATH/r mathjax_config.tmp' index.html
sed -i '/PLACEHOLDER_MATH/d' index.html
rm mathjax_config.tmp

# Inserir Link "Artigos" no Menu
sed -i '/<li><a href="#projects">Projetos<\/a><\/li>/a \                    <li><a href="#articles">Artigos</a></li>' index.html

# Inserir a Seção de Artigos
sed -i '/<section id="contact" class="contact">/i PLACEHOLDER_ARTICLES' index.html
sed -i '/PLACEHOLDER_ARTICLES/r article_content.tmp' index.html
sed -i '/PLACEHOLDER_ARTICLES/d' index.html
rm article_content.tmp

# ==========================================
# 4. ATUALIZAR STYLE.CSS
# ==========================================
echo "Atualizando style.css..."

cat >> style.css << 'CSS'

/* --- Seção de Artigos --- */
.articles {
    background-color: var(--white);
}

.articles-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
    justify-content: center;
}

.article-card {
    background-color: var(--light-gray);
    border-radius: 8px;
    padding: 2rem;
    transition: transform 0.3s, box-shadow 0.3s;
    border-left: 5px solid var(--secondary-blue);
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.article-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.article-meta {
    font-size: 0.85rem;
    color: var(--medium-gray);
    margin-bottom: 1rem;
    display: flex;
    justify-content: space-between;
    text-transform: uppercase;
    font-weight: 600;
}

.article-content h3 {
    color: var(--primary-blue);
    margin-bottom: 1rem;
    font-size: 1.3rem;
    line-height: 1.4;
}

.read-more-btn {
    margin-top: 1.5rem;
    color: var(--secondary-blue);
    font-weight: 600;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}

/* Detalhes do Artigo (Modal) */
.article-detail {
    display: none;
    background-color: var(--white);
    padding: 3rem;
    border-radius: 10px;
    margin-top: 2rem;
    box-shadow: 0 5px 25px rgba(0, 0, 0, 0.15);
    border: 1px solid #e0e0e0;
}

.article-detail.active {
    display: block;
    animation: fadeIn 0.5s ease;
}

.article-body {
    font-family: 'Georgia', serif;
    font-size: 1.1rem;
    line-height: 1.8;
    color: #333;
    max-width: 800px;
    margin: 0 auto;
}

.article-body h4 {
    font-family: 'Segoe UI', sans-serif;
    color: var(--primary-blue);
    margin-top: 2.5rem;
    margin-bottom: 1rem;
    font-size: 1.4rem;
    border-bottom: 1px solid #eee;
    padding-bottom: 0.5rem;
}

.article-body h5 {
    font-family: 'Segoe UI', sans-serif;
    color: var(--secondary-blue);
    margin-top: 1.5rem;
    margin-bottom: 0.5rem;
    font-size: 1.2rem;
}

.article-body p {
    margin-bottom: 1.5rem;
}

.article-body ul {
    margin-bottom: 1.5rem;
    padding-left: 2rem;
}

.article-body li {
    margin-bottom: 0.5rem;
}

/* Ajustes MathJax */
mjx-container {
    overflow-x: auto;
    overflow-y: hidden;
    max-width: 100%;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
    .article-detail {
        padding: 1.5rem;
    }
}
CSS

# ==========================================
# 5. ATUALIZAR SCRIPT.JS (Com Fix do MathJax)
# ==========================================
echo "Atualizando script.js..."

# Remover fechamento anterior
sed -i '$d' script.js

cat >> script.js << 'JS'

    // --- Lógica para Artigos (Com Fix de MathJax) ---
    const articleCards = document.querySelectorAll('.article-card');
    const articleDetails = document.querySelectorAll('.article-detail');
    const closeArticleButtons = document.querySelectorAll('.close-article');

    // Inicializa o MathJax na carga da página
    if (window.MathJax) {
        window.MathJax.typesetPromise().catch((err) => console.log('Erro MathJax Init:', err));
    }

    articleCards.forEach(card => {
        card.addEventListener('click', function() {
            const articleId = this.getAttribute('data-article');
            
            // Fecha outros abertos
            articleDetails.forEach(detail => detail.classList.remove('active'));
            
            const currentArticle = document.getElementById(articleId);
            if (currentArticle) {
                currentArticle.classList.add('active');
                
                // Força o MathJax a renderizar as fórmulas AGORA que o elemento está visível
                if (window.MathJax) {
                    window.MathJax.typesetPromise([currentArticle]).then(() => {
                        console.log('Fórmulas renderizadas com sucesso.');
                    });
                }

                currentArticle.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    closeArticleButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.closest('.article-detail').classList.remove('active');
            document.querySelector('#articles').scrollIntoView({ behavior: 'smooth' });
        });
    });

    // Fechar ao clicar fora
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.article-detail') && !e.target.closest('.article-card')) {
            articleDetails.forEach(detail => {
                detail.classList.remove('active');
            });
        }
    });
});
JS

echo "Processo concluído! O artigo foi inserido com sucesso."
