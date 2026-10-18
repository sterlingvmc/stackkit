// Client-side filter for the homepage directory. Works on server-rendered cards (no fetch needed).
(function(){
  var q=document.getElementById('q'); if(!q) return;
  var cards=[].slice.call(document.querySelectorAll('#grid .card[data-cat]'));
  var chips=[].slice.call(document.querySelectorAll('.chip[data-cat]'));
  var free=document.getElementById('f-free'), ss=document.getElementById('f-ss');
  var count=document.getElementById('count'), empty=document.getElementById('empty');
  var cat='all';
  var params=new URLSearchParams(location.search);
  if(params.get('q')) q.value=params.get('q');
  if(params.get('cat')) cat=params.get('cat');
  function norm(s){return (s||'').toLowerCase();}
  function apply(){
    var terms=norm(q.value).split(/\s+/).filter(Boolean), n=0;
    cards.forEach(function(c){
      var hay=c.getAttribute('data-search');
      var ok=(cat==='all'||c.getAttribute('data-cat')===cat)
        &&(!free.checked||c.getAttribute('data-free')==='1')
        &&(!ss.checked||c.getAttribute('data-ss')==='1')
        &&terms.every(function(t){return hay.indexOf(t)>-1;});
      c.hidden=!ok; if(ok) n++;
    });
    chips.forEach(function(ch){ch.setAttribute('aria-pressed',ch.getAttribute('data-cat')===cat?'true':'false');});
    count.textContent=n+' tool'+(n===1?'':'s');
    empty.style.display=n?'none':'block';
    var p=new URLSearchParams(); if(q.value) p.set('q',q.value); if(cat!=='all') p.set('cat',cat);
    history.replaceState(null,'',location.pathname+(p.toString()?'?'+p:'')+location.hash);
  }
  q.addEventListener('input',apply);
  free.addEventListener('change',apply); ss.addEventListener('change',apply);
  chips.forEach(function(ch){ch.addEventListener('click',function(){cat=ch.getAttribute('data-cat');apply();});});
  apply();
})();
// Placeholder checkout buttons: warn instead of navigating while Stripe links are TODO.
document.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('[data-todo]'); if(!a) return;
  e.preventDefault(); alert('TODO: '+a.getAttribute('data-todo'));
});
