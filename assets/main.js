// Mobile menu + dropdowns
(function(){
  var nav=document.querySelector('nav'), burger=document.querySelector('.burger');
  if(burger) burger.addEventListener('click',function(){
    var open=nav.classList.toggle('open'); burger.setAttribute('aria-expanded',open);
  });
  document.querySelectorAll('.has-dd>a').forEach(function(a){
    a.addEventListener('click',function(e){
      if(window.innerWidth<=1020){e.preventDefault();a.parentNode.classList.toggle('open');}
    });
  });
  var yr=document.getElementById('yr'); if(yr) yr.textContent=new Date().getFullYear();
})();

// Quick-search tabs (fallback until myRealPage widget is embedded)
function qsTab(b){b.parentNode.querySelectorAll('button').forEach(function(x){x.classList.remove('on')});b.classList.add('on');}

// Testimonial carousel
(function(){
  var slides=[].slice.call(document.querySelectorAll('.slide')), dots=document.getElementById('dots');
  if(!slides.length||!dots) return;
  var cur=0, timer;
  slides.forEach(function(_,i){var b=document.createElement('button');b.type='button';b.setAttribute('aria-label','Testimonial '+(i+1));b.onclick=function(){show(i)};dots.appendChild(b);});
  function show(i){
    cur=(i+slides.length)%slides.length;
    slides.forEach(function(s,j){s.classList.toggle('on',j===cur)});
    [].forEach.call(dots.children,function(d,j){d.classList.toggle('on',j===cur)});
    clearInterval(timer); timer=setInterval(function(){show(cur+1)},8000);
  }
  window.go=function(d){show(cur+d)};
  show(0);
})();

// Mortgage calculator (Canadian: interest compounded semi-annually)
(function(){
  var f=document.getElementById('calc'); if(!f) return;
  var $=function(id){return document.getElementById(id)};
  var money=function(n){return n.toLocaleString('en-CA',{style:'currency',currency:'CAD',maximumFractionDigits:0})};
  function run(){
    var price=+$('c-price').value||0, down=+$('c-down').value||0, rate=(+$('c-rate').value||0)/100,
        years=+$('c-amort').value||25, freq=$('c-freq').value;
    var principal=Math.max(price-down,0);
    var perYear={monthly:12,biweekly:26,weekly:52}[freq];
    var r=Math.pow(1+rate/2,2/perYear)-1, n=years*perYear;
    var pay=r?principal*r/(1-Math.pow(1+r,-n)):principal/n;
    $('o-pay').textContent=money(pay);
    $('o-lbl').textContent=freq.charAt(0).toUpperCase()+freq.slice(1)+' payment';
    $('o-principal').textContent=money(principal);
    $('o-interest').textContent=money(pay*n-principal);
    $('o-total').textContent=money(pay*n);
    var pct=price?down/price*100:0;
    $('o-downpct').textContent=pct.toFixed(1)+'%';
    $('o-warn').hidden=!(price&&pct<20);
  }
  f.addEventListener('input',run); run();
})();
