document.addEventListener('DOMContentLoaded', function() {
    
    // Menu mobile toggle
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }

    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', function() {
            if (navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
            }
        });
    });

    // Filtros de projetos
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            const filterValue = this.getAttribute('data-filter');
            
            projectCards.forEach(card => {
                if (filterValue === 'all' || card.getAttribute('data-category') === filterValue) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // Detalhes do projeto - card inteiro clicável
    const projectCardsAll = document.querySelectorAll('.project-card');
    const projectDetails = document.querySelectorAll('.project-detail');
    const closeButtons = document.querySelectorAll('.close-detail');
    
    projectCardsAll.forEach(card => {
        card.addEventListener('click', function(e) {
            if (e.target.tagName === 'A' || e.target.closest('a')) return;
            
            const projectId = this.getAttribute('data-project');
            
            projectDetails.forEach(detail => {
                detail.classList.remove('active');
            });
            
            const currentProjectDetail = document.getElementById(projectId);
            if (currentProjectDetail) {
                currentProjectDetail.classList.add('active');
                currentProjectDetail.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.closest('.project-detail').classList.remove('active');
        });
    });
    
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.project-detail') && !e.target.closest('.project-card')) {
            projectDetails.forEach(detail => {
                detail.classList.remove('active');
            });
        }
    });

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
