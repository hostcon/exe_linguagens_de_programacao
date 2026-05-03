// ======================
// ESTADO
// ======================
let user = localStorage.getItem("user");

// ======================
// ÁUDIO
// ======================
const spinSound = new Audio("/static/sons/spin.mp3");
const winSound  = new Audio("/static/sons/win.mp3");
const jackpotSound = new Audio("/static/sons/jackpot.mp3");
const bgMusic   = new Audio("/static/sons/bg.mp3");

bgMusic.loop = true;

let savedVolume = parseFloat(localStorage.getItem("volume") || "0.3");
let muted = localStorage.getItem("muted") === "true";

[bgMusic, spinSound, winSound, jackpotSound].forEach(a=>{
  a.volume = savedVolume;
  a.muted = muted;
});

// ======================
// CONFETE (CANVAS)
// ======================
const canvas = document.createElement("canvas");
document.body.appendChild(canvas);
const ctx = canvas.getContext("2d");

canvas.style.position = "fixed";
canvas.style.top = 0;
canvas.style.left = 0;
canvas.style.pointerEvents = "none";

function resize(){
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
}
window.onresize = resize;
resize();

let confetes = [];

function criarConfete(){
  for(let i=0;i<150;i++){
    confetes.push({
      x: Math.random()*canvas.width,
      y: Math.random()*canvas.height,
      r: Math.random()*6+2,
      d: Math.random()*10,
      color: `hsl(${Math.random()*360},100%,50%)`,
      tilt: Math.random()*10
    });
  }
}

function animarConfete(){
  ctx.clearRect(0,0,canvas.width,canvas.height);

  confetes.forEach(c=>{
    ctx.beginPath();
    ctx.fillStyle = c.color;
    ctx.fillRect(c.x, c.y, c.r, c.r);
  });

  confetes.forEach(c=>{
    c.y += Math.cos(c.d) + 2;
    c.x += Math.sin(c.d);

    if(c.y > canvas.height){
      c.y = -10;
    }
  });

  if(confetes.length > 0){
    requestAnimationFrame(animarConfete);
  }
}

function dispararConfete(){
  confetes = [];
  criarConfete();
  animarConfete();

  setTimeout(()=> confetes = [], 3000);
}

// ======================
// LOGIN / AUTO
// ======================
window.onload = () => {
  document.getElementById("volume").value = savedVolume;

  if(user){
    entrarJogo("...");
    fetch("/login",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({user:user, pwd:""})
    })
    .then(r=>r.json())
    .then(d=>{
      if(d.ok) entrarJogo(d.saldo);
      else logout();
    });
  }
};

function login(){
  user = document.getElementById("user").value;

  fetch("/login",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({
      user:user,
      pwd:document.getElementById("pwd").value
    })
  })
  .then(r=>r.json())
  .then(d=>{
    if(d.ok){
      localStorage.setItem("user", user);
      entrarJogo(d.saldo);
    } else alert(d.msg);
  });
}

function register(){
  fetch("/register",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({
      user:document.getElementById("user").value,
      pwd:document.getElementById("pwd").value
    })
  })
  .then(r=>r.json())
  .then(d=>{
    if(d.ok) alert("Cadastrado!");
    else alert(d.msg);
  });
}

function entrarJogo(saldo){
  document.getElementById("login").style.display="none";
  document.getElementById("game").style.display="block";
  document.getElementById("saldo").innerText="Saldo: "+saldo;
  bgMusic.play().catch(()=>{});
}

function logout(){
  localStorage.removeItem("user");
  user = null;
  document.getElementById("game").style.display="none";
  document.getElementById("login").style.display="block";
  bgMusic.pause();
}

// ======================
// 🎰 ANIMAÇÃO SUAVE
// ======================
const ICONS = ["🍊","🌰","🍵","🐂","⭐"];

function girarColuna(el, tempo){
  let start = performance.now();

  function frame(now){
    let t = now - start;

    el.innerText = ICONS[Math.floor(Math.random()*ICONS.length)];

    if(t < tempo){
      requestAnimationFrame(frame);
    }
  }

  requestAnimationFrame(frame);
}

function animarSlots(done){
  let s1 = document.getElementById("s1");
  let s2 = document.getElementById("s2");
  let s3 = document.getElementById("s3");

  girarColuna(s1, 800);
  girarColuna(s2, 1100);
  girarColuna(s3, 1400);

  setTimeout(done, 1500);
}

// ======================
// 🎰 SPIN
// ======================
function spin(){
  spinSound.currentTime = 0;
  spinSound.play();

  animarSlots(()=>{
    fetch("/spin",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({user:user})
    })
    .then(r=>r.json())
    .then(d=>{
      if(!d.ok){ alert(d.msg); return;}

      document.getElementById("s1").innerText=d.r[0];
      document.getElementById("s2").innerText=d.r[1];
      document.getElementById("s3").innerText=d.r[2];

      document.getElementById("saldo").innerText="Saldo: "+d.saldo;

      if(d.premio >= 20){
        jackpotSound.play();
        dispararConfete();
        document.body.classList.add("jackpot");
        setTimeout(()=>document.body.classList.remove("jackpot"),2000);
      }
      else if(d.premio > 0){
        winSound.play();
        document.getElementById("slots").classList.add("win");
        setTimeout(()=>document.getElementById("slots").classList.remove("win"),1000);
      }
      else{
        document.getElementById("slots").classList.add("shake");
        setTimeout(()=>document.getElementById("slots").classList.remove("shake"),500);
      }

      document.getElementById("msg").innerText =
        d.premio > 0 ? "🎉 Ganhou "+d.premio : "😢 Nada";
    });
  });
}

// ======================
// ÁUDIO
// ======================
function setVolume(v){
  [bgMusic, spinSound, winSound, jackpotSound].forEach(a=>a.volume=v);
  localStorage.setItem("volume", v);
}

function toggleMute(){
  muted = !muted;
  [bgMusic, spinSound, winSound, jackpotSound].forEach(a=>a.muted=muted);
  localStorage.setItem("muted", muted);
}