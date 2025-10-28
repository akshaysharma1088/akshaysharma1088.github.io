// UX: mobile menu, theme toggle, section reveal, KPI count-up, card tilt
function qs(sel, el=document){return el.querySelector(sel)}
function qsa(sel, el=document){return [...el.querySelectorAll(sel)]}

function toggleMenu(){
  const el = qs('#nav-links'); el.classList.toggle('show');
}

// Theme toggle with localStorage
(function(){
  const btn = document.getElementById('theme-toggle');
  const root = document.documentElement;
  const saved = localStorage.getItem('theme');
  if(saved === 'light'){ root.classList.add('light'); btn.textContent='☀️'; }
  btn?.addEventListener('click', ()=>{
    root.classList.toggle('light');
    const isLight = root.classList.contains('light');
    btn.textContent = isLight ? '☀️' : '🌙';
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
  });
})();

// Year
document.getElementById('year').textContent = new Date().getFullYear();

// Reveal on scroll
const observer = new IntersectionObserver((entries)=>{
  entries.forEach(e=>{
    if(e.isIntersecting){ e.target.classList.add('in'); observer.unobserve(e.target); }
  });
},{threshold:0.12});
qsa('.reveal').forEach(el=>observer.observe(el));

// KPI count-up
function animateCount(el){
  const end = Number(el.dataset.target||'0'); if(!end) return;
  const dur = 1200, start = performance.now();
  function step(ts){
    const t = Math.min(1, (ts-start)/dur);
    el.textContent = Math.floor(end * (0.5 - Math.cos(Math.PI*t)/2));
    if(t<1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}
qsa('.kpi .num').forEach(animateCount);

// Subtle 3D tilt
qsa('.tilt').forEach(card=>{
  card.addEventListener('mousemove', (e)=>{
    const r = card.getBoundingClientRect();
    const x = (e.clientX - r.left) / r.width;
    const y = (e.clientY - r.top) / r.height;
    const rx = (y - 0.5) * 6;
    const ry = (0.5 - x) * 8;
    card.style.transform = `rotateX(${rx}deg) rotateY(${ry}deg) translateY(-2px)`;
  });
  card.addEventListener('mouseleave', ()=>{
    card.style.transform = '';
  });
});

