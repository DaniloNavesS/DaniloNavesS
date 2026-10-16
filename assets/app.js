/* Interface sem dependências. O canvas é decorativo e respeita movimento reduzido. */
const filterButtons = document.querySelectorAll('[data-filter]');
filterButtons.forEach(button => button.addEventListener('click', () => {
  filterButtons.forEach(b => b.setAttribute('aria-pressed', String(b === button)));
  document.querySelectorAll('[data-category]').forEach(card => {
    card.hidden = button.dataset.filter !== 'todos' && card.dataset.category !== button.dataset.filter;
  });
}));
const canvas = document.getElementById('field');
if (canvas) {
 const ctx = canvas.getContext('2d');
 if (ctx) {
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  let width = 0, height = 0, frame = 0, visible = true, time = 0;
  const points = Array.from({length: 760}, (_, i) => {
   const y = 1 - 2 * (i + .5) / 760, r = Math.sqrt(1-y*y), a = i * 2.3999632297;
   return {x: Math.cos(a)*r, y, z: Math.sin(a)*r};
  });
  function resize() {
   const box = canvas.getBoundingClientRect(), dpr = Math.min(devicePixelRatio || 1, 2);
   width = box.width; height = box.height;
   canvas.width = width*dpr; canvas.height = height*dpr;
   ctx.setTransform(dpr,0,0,dpr,0,0); draw();
  }
  function draw() {
   ctx.clearRect(0,0,width,height);
   const mobile = width<600, radius = mobile ? width*.7 : Math.min(width*.33, height*.53);
   const cx = width*(mobile?.94:.79), cy = height*(mobile?.7:.58);
   const a=time*.00012, b=-.32;
   const projected=points.map(p=>{
    const x=p.x*Math.cos(a)-p.z*Math.sin(a), z=p.x*Math.sin(a)+p.z*Math.cos(a);
    const y=p.y*Math.cos(b)-z*Math.sin(b), zz=p.y*Math.sin(b)+z*Math.cos(b);
    const k=2.8/(2.8-zz*.45);
    return {x:cx+x*radius*k,y:cy+y*radius*k,z:zz};
   });
   projected.forEach((p,i)=>{
    if(p.z<-.42)return;
    const alpha=(p.z+1)/2;
    if(i%3===0){const q=projected[(i+21)%points.length];if(q.z>0&&Math.hypot(p.x-q.x,p.y-q.y)<radius*.25){ctx.strokeStyle=`rgba(199,216,137,${alpha*.14})`;ctx.lineWidth=.5;ctx.beginPath();ctx.moveTo(p.x,p.y);ctx.lineTo(q.x,q.y);ctx.stroke();}}
    ctx.fillStyle=`rgba(222,235,175,${alpha*.75})`;ctx.beginPath();ctx.arc(p.x,p.y,alpha*1.5+.3,0,Math.PI*2);ctx.fill();
   });
   ctx.strokeStyle='rgba(206,221,153,.3)';ctx.lineWidth=.7;
   ctx.beginPath();ctx.ellipse(cx,cy,radius*1.18,radius*.36,-.45,0,Math.PI*2);ctx.stroke();
   ctx.strokeStyle='rgba(206,221,153,.12)';ctx.beginPath();ctx.ellipse(cx,cy,radius*1.22,radius*.36,.65,0,Math.PI*2);ctx.stroke();
  }
  function tick(t){frame=0;time=t;draw();if(visible&&!document.hidden&&!motion.matches)frame=requestAnimationFrame(tick);}
  function start(){if(!frame&&visible&&!document.hidden&&!motion.matches)frame=requestAnimationFrame(tick);else draw();}
  new ResizeObserver(resize).observe(canvas);
  new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(!visible&&frame){cancelAnimationFrame(frame);frame=0;}else start();}).observe(canvas);
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&frame){cancelAnimationFrame(frame);frame=0;}else start();});
  motion.addEventListener('change',()=>{if(motion.matches&&frame){cancelAnimationFrame(frame);frame=0;}start();});
  resize(); start();
 }
}
