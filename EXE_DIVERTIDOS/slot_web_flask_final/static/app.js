// ======================
// ESTADO
// ======================
let user = localStorage.getItem("user");

// ======================
// ÁUDIO
// ======================
const spinSound = new Audio("/static/sons/spin.mp3");
const winSound  = new Audio("/static/sons/win.mp3");
const bgMusic   = new Audio("/static/sons/bg.mp3");

bgMusic.loop = true;

let savedVolume = parseFloat(localStorage.getItem("volume") || "0.3");
let muted = localStorage.getItem("muted") === "true";

[bgMusic, spinSound, winSound].forEach(a=>{
  a.volume = savedVolume;
  a.muted = muted;
});

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

// ======================
// LOGIN/CADASTRO
// ======================
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
// 🎰 ROLAGEM INDEPENDENTE
// ======================
const ICONS = ["🍊","🌰","🍵","🐂","⭐"];

function spinColumn(el, duration, done){
  let t = 0;
  let delay = 40;

  function loop(){
    if(t < duration){
      el.innerText = ICONS[Math.floor(Math.random()*ICONS.length)];
      t += delay;
      delay += 2; // desacelera
      setTimeout(loop, delay);
    } else {
      done && done();
    }
  }
  loop();
}

function animarSlots(done){
  let s1 = document.getElementById("s1");
  let s2 = document.getElementById("s2");
  let s3 = document.getElementById("s3");

  let finished = 0;
  function end(){
    finished++;
    if(finished === 3) done();
  }

  spinColumn(s1, 900, end);
  spinColumn(s2, 1200, end);
  spinColumn(s3, 1500, end);
}

// ======================
// 💥 EFEITOS VISUAIS
// ======================
function efeitoWin(){
  document.getElementById("slots").classList.add("win");
  setTimeout(()=> {
    document.getElementById("slots").classList.remove("win");
  }, 1200);
}

function efeitoJackpot(){
  document.body.classList.add("jackpot");
  setTimeout(()=> {
    document.body.classList.remove("jackpot");
  }, 1500);
}

function efeitoShake(){
  document.getElementById("slots").classList.add("shake");
  setTimeout(()=> {
    document.getElementById("slots").classList.remove("shake");
  }, 600);
}

// ======================
// SPIN
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

      if(d.premio > 0){
        winSound.currentTime = 0;
        winSound.play();

        if(d.premio >= 20){
          efeitoJackpot();
        } else {
          efeitoWin();
        }

        document.getElementById("msg").innerText="🎉 Ganhou "+d.premio;
      } else {
        efeitoShake();
        document.getElementById("msg").innerText="😢 Nada";
      }
    });
  });
}

// ======================
// ÁUDIO
// ======================
function setVolume(v){
  [bgMusic, spinSound, winSound].forEach(a=>a.volume=v);
  localStorage.setItem("volume", v);
}

function toggleMute(){
  muted = !muted;
  [bgMusic, spinSound, winSound].forEach(a=>a.muted=muted);
  localStorage.setItem("muted", muted);
}

// ======================
// RANKING
// ======================
function verRanking(){
  fetch("/ranking")
  .then(r=>r.json())
  .then(d=>{
    let txt="🏆 Ranking\n\n";
    d.forEach((u,i)=> txt+=(i+1)+". "+u[0]+" - "+u[1]+"\n");
    alert(txt);
  });
}