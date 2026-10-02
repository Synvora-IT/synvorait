
  const toggles = document.querySelectorAll('.nav-toggle');
  toggles.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const panel = document.getElementById('dd-' + btn.dataset.dropdown);
      const isOpen = panel.classList.contains('open');
      document.querySelectorAll('.dropdown').forEach(d => d.classList.remove('open'));
      toggles.forEach(t => t.classList.remove('open'));
      if(!isOpen){ panel.classList.add('open'); btn.classList.add('open'); }
    });
  });
  document.addEventListener('click', () => {
    document.querySelectorAll('.dropdown').forEach(d => d.classList.remove('open'));
    toggles.forEach(t => t.classList.remove('open'));
  });

  const hamburger = document.getElementById('hamburger');
  const mobilePanel = document.getElementById('mobilePanel');
  hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('open');
    mobilePanel.classList.toggle('open');
  });
  document.querySelectorAll('.m-toggle').forEach(t => {
    t.addEventListener('click', () => {
      const target = document.getElementById(t.dataset.target);
      const isOpen = target.classList.contains('open');
      document.querySelectorAll('.m-sub').forEach(s => s.classList.remove('open'));
      document.querySelectorAll('.m-toggle').forEach(m => m.classList.remove('open'));
      if(!isOpen){ target.classList.add('open'); t.classList.add('open'); }
    });
  });


 // Intersection Observer for scroll-based animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, observerOptions);

        document.querySelectorAll('.card').forEach(card => {
            observer.observe(card);
        });


    
    async function autoSubmit(){

      const delay = 1000;

      const search = document.getElementById('search');

      const form = document.getElementById("searchForm");

      let timeout;

      search.addEventListener("input" , ()=>{
        clearTimeout(timeout);

        timeout = setTimeout(()=>{form.submit();} , delay);

      })
    }