(function(){
  var d=document, w=window, reduce=w.matchMedia&&w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $$=function(s,c){return [].slice.call((c||d).querySelectorAll(s))};

  // Mobile menu
  var nav=d.querySelector('nav[aria-label="Main"]'), burger=d.querySelector('.burger');
  if(burger) burger.addEventListener('click',function(){var o=nav.classList.toggle('open');burger.setAttribute('aria-expanded',o)});
  $$('.has-dd>a').forEach(function(a){a.addEventListener('click',function(e){if(w.innerWidth<=1020){e.preventDefault();a.parentNode.classList.toggle('open')}})});
  var yr=d.getElementById('yr'); if(yr) yr.textContent=new Date().getFullYear();

  // Quick-search tabs
  $$('.qs .tabs button').forEach(function(b){b.addEventListener('click',function(){$$('.qs .tabs button').forEach(function(x){x.classList.remove('on')});b.classList.add('on')})});

  // Lazy backgrounds + scroll reveal (one IntersectionObserver each)
  var io=('IntersectionObserver' in w);
  var bgs=$$('[data-lazybg]');
  if(io){var bo=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('bg-in');bo.unobserve(e.target)}})},{rootMargin:'400px'});bgs.forEach(function(el){bo.observe(el)})}
  else bgs.forEach(function(el){el.classList.add('bg-in')});

  function later(){
  // Hero crossfade slider: first image loads with the page, the rest after window load
  var hs=$$('.hero-bg img'), hd=d.querySelector('.hero-dots');
  if(hs.length>1){
    var hi=0, ht;
    hs.forEach(function(_,i){var b=d.createElement('button');b.type='button';b.setAttribute('aria-label','Show image '+(i+1));if(!i)b.className='on';b.onclick=function(){hshow(i)};hd.appendChild(b)});
    function hshow(i){
      var img=hs[i]; if(img.dataset.src){img.srcset=img.dataset.srcset;img.src=img.dataset.src;img.removeAttribute('data-src')}
      hi=i; hs.forEach(function(x,j){x.classList.toggle('on',j===i)}); $$('button',hd).forEach(function(b,j){b.classList.toggle('on',j===i)});
      clearTimeout(ht); if(!reduce) ht=setTimeout(function(){hshow((hi+1)%hs.length)},6500);
    }
    (function(){
      setTimeout(function(){hs.slice(1).forEach(function(img){if(img.dataset.src){img.srcset=img.dataset.srcset;img.src=img.dataset.src;img.removeAttribute('data-src')}})},1200);
      if(!reduce) ht=setTimeout(function(){hshow(1)},6500);
    })();
  }

  // Testimonial carousel (horizontal, autoplay, swipe, pause on hover)
  var car=d.querySelector('.tcar');
  if(car){
    var track=car.querySelector('.ttrack'), slides=$$('.tslide',car), dots=d.getElementById('dots'), cur=0, t, x0=null;
    slides.forEach(function(_,i){var b=d.createElement('button');b.type='button';b.setAttribute('aria-label','Testimonial '+(i+1));b.onclick=function(){go(i)};dots.appendChild(b)});
    function go(i){
      cur=(i+slides.length)%slides.length; track.style.transform='translateX('+(-cur*100)+'%)';
      slides.forEach(function(s,j){s.setAttribute('aria-hidden',j!==cur)}); $$('button',dots).forEach(function(b,j){b.classList.toggle('on',j===cur)});
      play();
    }
    function play(){clearInterval(t); if(!reduce) t=setInterval(function(){go(cur+1)},6000)}
    car.querySelector('.prev').onclick=function(){go(cur-1)}; car.querySelector('.next').onclick=function(){go(cur+1)};
    car.addEventListener('mouseenter',function(){clearInterval(t)}); car.addEventListener('mouseleave',play);
    car.addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
    car.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>40)go(cur+(dx<0?1:-1));x0=null});
    go(0);
  }

  }
  if(d.readyState==='complete') setTimeout(later,0); else w.addEventListener('load',function(){setTimeout(later,0)});

  // Mortgage calculator (Canadian semi-annual compounding)
  var f=d.getElementById('calc');
  if(f){
    var g=function(id){return d.getElementById(id)}, money=function(n){return n.toLocaleString('en-CA',{style:'currency',currency:'CAD',maximumFractionDigits:0})};
    var run=function(){
      var price=+g('c-price').value||0, down=+g('c-down').value||0, rate=(+g('c-rate').value||0)/100, years=+g('c-amort').value||25, freq=g('c-freq').value;
      var P=Math.max(price-down,0), k={monthly:12,biweekly:26,weekly:52}[freq], r=Math.pow(1+rate/2,2/k)-1, n=years*k;
      var pay=r?P*r/(1-Math.pow(1+r,-n)):P/n;
      g('o-pay').textContent=money(pay); g('o-lbl').textContent=freq.charAt(0).toUpperCase()+freq.slice(1)+' payment';
      g('o-principal').textContent=money(P); g('o-interest').textContent=money(pay*n-P); g('o-total').textContent=money(pay*n);
      var pct=price?down/price*100:0; g('o-downpct').textContent=pct.toFixed(1)+'%'; g('o-warn').hidden=!(price&&pct<20);
    };
    f.addEventListener('input',run); run();
  }
})();
