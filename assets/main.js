(function(){
  var d=document, w=window, root=d.documentElement, reduce=(w.matchMedia&&w.matchMedia('(prefers-reduced-motion: reduce)').matches)||root.classList.contains('a11y-still');
  var $$=function(s,c){return [].slice.call((c||d).querySelectorAll(s))};

  // Mobile menu
  var nav=d.querySelector('nav[aria-label="Main"]'), burger=d.querySelector('.burger');
  if(burger) burger.addEventListener('click',function(){var o=nav.classList.toggle('open');burger.setAttribute('aria-expanded',o)});
  $$('.has-dd>a').forEach(function(a){a.addEventListener('click',function(e){if(w.innerWidth<=1020){e.preventDefault();a.parentNode.classList.toggle('open')}})});
  var yr=d.getElementById('yr'); if(yr) yr.textContent=new Date().getFullYear();


  // Back to top (rAF-throttled, passive)
  var top=d.querySelector('.to-top');
  if(top){
    var ticking=false;
    w.addEventListener('scroll',function(){if(ticking)return;ticking=true;requestAnimationFrame(function(){top.hidden=w.scrollY<700;ticking=false})},{passive:true});
    top.addEventListener('click',function(){w.scrollTo({top:0,behavior:root.classList.contains('a11y-still')||reduce?'auto':'smooth'});var s=d.querySelector('.skip');if(s)s.focus({preventScroll:true})});
  }

  // Accessibility panel (choices saved on this device)
  var ab=d.querySelector('.a11y-btn'), ap=d.getElementById('a11y-panel');
  if(ab&&ap){
    var OPTS=['a11y-contrast','a11y-links','a11y-read','a11y-still'], SIZES=['','a11y-t1','a11y-t2','a11y-t3'];
    function size(){for(var i=SIZES.length-1;i>0;i--)if(root.classList.contains(SIZES[i]))return i;return 0}
    function save(){var on=OPTS.filter(function(o){return root.classList.contains(o)});var s=size();if(s)on.push(SIZES[s]);try{localStorage.setItem('a11y',on.join(' '))}catch(e){}}
    function sync(){$$('.a11y-opt',ap).forEach(function(b){b.setAttribute('aria-pressed',root.classList.contains(b.dataset.opt))})}
    function open(o){ap.hidden=!o;ab.setAttribute('aria-expanded',o);if(o){sync();var f=ap.querySelector('button');if(f)f.focus()}}
    ab.addEventListener('click',function(){open(ap.hidden)});
    ap.querySelector('.a11y-close').addEventListener('click',function(){open(false);ab.focus()});
    d.addEventListener('keydown',function(e){if(e.key==='Escape'&&!ap.hidden){open(false);ab.focus()}});
    d.addEventListener('click',function(e){if(!ap.hidden&&!ap.contains(e.target)&&!ab.contains(e.target))open(false)});
    $$('.a11y-opt',ap).forEach(function(b){b.addEventListener('click',function(){root.classList.toggle(b.dataset.opt);if(b.dataset.opt==='a11y-still')reduce=root.classList.contains('a11y-still');sync();save()})});
    $$('.a11y-size button',ap).forEach(function(b){b.addEventListener('click',function(){var s=Math.max(0,Math.min(3,size()+(+b.dataset.size)));SIZES.forEach(function(c){if(c)root.classList.remove(c)});if(s)root.classList.add(SIZES[s]);save()})});
    ap.querySelector('.a11y-reset').addEventListener('click',function(){OPTS.concat(SIZES).forEach(function(c){if(c)root.classList.remove(c)});reduce=w.matchMedia&&w.matchMedia('(prefers-reduced-motion: reduce)').matches;sync();save()});
  }

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
      clearTimeout(ht); if(!reduce) ht=setTimeout(function(){if(!reduce)hshow((hi+1)%hs.length)},6500);
    }
    (function(){
      setTimeout(function(){hs.slice(1).forEach(function(img){if(img.dataset.src){img.srcset=img.dataset.srcset;img.src=img.dataset.src;img.removeAttribute('data-src')}})},1200);
      if(!reduce) ht=setTimeout(function(){if(!reduce)hshow(1)},6500);
    })();
  }

  // Testimonial carousel: endless loop (clones at both ends, silent jump after the slide), autoplay, swipe
  var car=d.querySelector('.tcar');
  if(car){
    var track=car.querySelector('.ttrack'), slides=$$('.tslide',car), n=slides.length, dots=d.getElementById('dots'), pos=1, t, x0=null, busy=false;
    var first=slides[0].cloneNode(true), last=slides[n-1].cloneNode(true);
    [first,last].forEach(function(c){c.setAttribute('aria-hidden','true');$$('img',c).forEach(function(i){i.loading='eager'})});
    track.appendChild(first); track.insertBefore(last,slides[0]);
    function place(anim){track.style.transition=anim?'':'none';track.style.transform='translateX('+(-pos*100)+'%)'}
    function mark(){var real=(pos-1+n)%n;slides.forEach(function(s,j){s.setAttribute('aria-hidden',j!==real)});$$('button',dots).forEach(function(b,j){b.classList.toggle('on',j===real)})}
    slides.forEach(function(_,i){var b=d.createElement('button');b.type='button';b.setAttribute('aria-label','Testimonial '+(i+1));b.onclick=function(){if(!busy){pos=i+1;busy=true;place(true);mark();arm();play()}};dots.appendChild(b)});
    function step(dir){if(busy)return;busy=true;pos+=dir;place(true);mark();arm();play()}
    var st;
    function settle(){clearTimeout(st); busy=false;
      if(pos===n+1){pos=1;place(false)} else if(pos===0){pos=n;place(false)} else return;
      track.offsetWidth; track.style.transition='';
    }
    function arm(){clearTimeout(st); st=setTimeout(settle, reduce?0:900)}   // fallback if transitionend doesn't fire
    track.addEventListener('transitionend',function(e){if(e.target===track)settle()});
    function play(){clearInterval(t); if(!reduce) t=setInterval(function(){if(!reduce)step(1)},6000)}
    car.querySelector('.prev').onclick=function(){step(-1)}; car.querySelector('.next').onclick=function(){step(1)};
    car.addEventListener('mouseenter',function(){clearInterval(t)}); car.addEventListener('mouseleave',play);
    car.addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
    car.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>40)step(dx<0?1:-1);x0=null});
    place(false); track.offsetWidth; track.style.transition=''; mark(); play();
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
