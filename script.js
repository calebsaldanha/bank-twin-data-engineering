// Aguarda o DOM ser completamente carregado antes de executar o script
document.addEventListener('DOMContentLoaded', function() {
    
    // --- Lógica do Menu Mobile ---
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }

    // Fecha o menu mobile ao clicar em um link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', function() {
            if (navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
            }
        });
    });

    // --- Lógica de Filtros de Projetos ---
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');

    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove a classe 'active' de todos os botões de filtro
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Adiciona a classe 'active' ao botão clicado
            this.classList.add('active');
            
            const filterValue = this.getAttribute('data-filter');
            
            // Filtra os cards dos projetos com base no valor do filtro
            projectCards.forEach(card => {
                if (filterValue === 'all' || card.getAttribute('data-category') === filterValue) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
    
    // --- Lógica de Abertura e Fechamento de Detalhes do Projeto ---
    const projectCardsAll = document.querySelectorAll('.project-card');
    const projectDetails = document.querySelectorAll('.project-detail');
    const closeButtons = document.querySelectorAll('.close-detail');
    
    projectCardsAll.forEach(card => {
        card.addEventListener('click', function(e) {
            // Impede que o clique em links dentro do card dispare o evento de abrir o detalhe
            if (e.target.tagName === 'A' || e.target.closest('a')) return;
            
            const projectId = this.getAttribute('data-project');
            
            // Esconde todos os detalhes de projetos abertos
            projectDetails.forEach(detail => {
                detail.classList.remove('active');
            });
            
            // Mostra o detalhe do projeto clicado
            const currentProjectDetail = document.getElementById(projectId);
            currentProjectDetail.classList.add('active');
            
            // Rola suavemente até a seção de detalhes do projeto
            currentProjectDetail.scrollIntoView({ behavior: 'smooth' });
        });
    });
    
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.closest('.project-detail').classList.remove('active');
        });
    });
    
    // Fecha o detalhe do projeto ao clicar fora dele
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.project-detail') && !e.target.closest('.project-card')) {
            projectDetails.forEach(detail => {
                detail.classList.remove('active');
            });
        }
    });

    // --- Lógica dos Slides dentro dos Detalhes do Projeto (seção 'Análise de Campanha...') ---
    const slidesContainer = document.getElementById('slidesContainer');
    if (slidesContainer) {
        const slides = slidesContainer.querySelectorAll('.slide');
        const totalSlides = slides.length;
        let currentSlideIndex = 0;

        function showSlide(index) {
            slides.forEach((slide, i) => {
                slide.style.display = (i === index) ? 'block' : 'none';
            });
            currentSlideIndex = index;
        }

        function nextSlide() {
            currentSlideIndex = (currentSlideIndex + 1) % totalSlides;
            showSlide(currentSlideIndex);
        }

        function prevSlide() {
            currentSlideIndex = (currentSlideIndex - 1 + totalSlides) % totalSlides;
            showSlide(currentSlideIndex);
        }

        // Adiciona event listeners aos botões de navegação dos slides
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        if (prevBtn) {
            prevBtn.addEventListener('click', prevSlide);
        }
        if (nextBtn) {
            nextBtn.addEventListener('click', nextSlide);
        }

        // Exibe o primeiro slide por padrão
        showSlide(currentSlideIndex);
    }
});
