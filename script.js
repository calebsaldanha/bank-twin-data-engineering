// Menu mobile toggle
document.querySelector('.menu-toggle').addEventListener('click', function() {
    document.querySelector('.nav-links').classList.toggle('active');
});

// Filtros de projetos
const filterButtons = document.querySelectorAll('.filter-btn');
const projectCards = document.querySelectorAll('.project-card');

filterButtons.forEach(button => {
    button.addEventListener('click', function() {
        // Remove active class de todos os botões
        filterButtons.forEach(btn => btn.classList.remove('active'));
        // Adiciona active class ao botão clicado
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
        // Impede que o clique em links dentro do card dispare o evento
        if (e.target.tagName === 'A' || e.target.closest('a')) return;
        
        const projectId = this.getAttribute('data-project');
        
        // Esconde todos os detalhes
        projectDetails.forEach(detail => {
            detail.classList.remove('active');
        });
        
        // Mostra o detalhe do projeto clicado
        document.getElementById(projectId).classList.add('active');
        
        // Rola até o detalhe do projeto
        document.getElementById(projectId).scrollIntoView({ behavior: 'smooth' });
    });
});

closeButtons.forEach(button => {
    button.addEventListener('click', function() {
        this.closest('.project-detail').classList.remove('active');
    });
});

// Fecha detalhes do projeto ao clicar fora
document.addEventListener('click', function(e) {
    if (!e.target.closest('.project-detail') && !e.target.closest('.project-card')) {
        projectDetails.forEach(detail => {
            detail.classList.remove('active');
        });
    }
});

// Fecha menu mobile ao clicar em um link
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', function() {
        document.querySelector('.nav-links').classList.remove('active');
    });
});
