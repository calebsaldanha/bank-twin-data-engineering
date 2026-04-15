document.addEventListener('DOMContentLoaded', () => {
    // Scroll suave para links internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Efeito no Header ao rolar
    const header = document.querySelector('header');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.style.padding = '0.8rem 0';
            header.style.background = 'rgba(5, 5, 5, 0.95)';
        } else {
            header.style.padding = '1.2rem 0';
            header.style.background = 'rgba(5, 5, 5, 0.8)';
        }
    });

    // Lógica do Sistema de Modais
    const modalBtns = document.querySelectorAll('.open-modal-btn');
    const closeBtns = document.querySelectorAll('.close-modal-btn');
    const modals = document.querySelectorAll('.modal-overlay');

    modalBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const modalId = btn.getAttribute('data-modal');
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.add('active');
                document.body.style.overflow = 'hidden'; // Impede o scroll da página ao fundo
            }
        });
    });

    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const modal = btn.closest('.modal-overlay');
            modal.classList.remove('active');
            document.body.style.overflow = 'auto'; // Restaura o scroll
        });
    });

    // Fecha o modal se clicar fora da área de conteúdo (no fundo escuro)
    window.addEventListener('click', (e) => {
        modals.forEach(modal => {
            if (e.target === modal) {
                modal.classList.remove('active');
                document.body.style.overflow = 'auto';
            }
        });
    });
});
