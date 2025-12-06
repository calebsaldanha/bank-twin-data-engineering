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
});