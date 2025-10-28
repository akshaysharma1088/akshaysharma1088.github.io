function toggleMenu(){
  const el = document.getElementById('nav-links');
  el.classList.toggle('show');
}
document.getElementById('year').textContent = new Date().getFullYear();
