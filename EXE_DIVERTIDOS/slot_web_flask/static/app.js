// ======================
// ESTADO
// ======================
let user = localStorage.getItem("user");

// ======================
// ÁUDIO (CORRIGIDO)
// ======================
const spinSound = new Audio("/static/sons/spin.mp3");
const winSound  = new Audio("/static/sons/win.mp3");
const bgMusic   = new Audio("/static/sons/bg.mp3");

bgMusic.loop = true;

// recuperar volume salvo
let savedVolume = localStorage.getItem("volume") || 0.3;
bgMusic.volume = savedVolume;

// recuperar mute
let muted = localStorage.getItem("muted") === "true";
bgMusic.muted = muted;

// ======================
// AUTO LOGIN
// ======================
window.onload = () => {
    if(user){
        entrarJogo("Carregando...");
        fetch("/login",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({user:user, pwd:""})
        })
        .then(r=>r.json())
        .then(d=>{
            if(d.ok){
                entrarJogo(d.saldo);
            } else {
                logout();
            }
        });
    }
};

// ======================
// LOGIN
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
    })
}

// ======================
// CADASTRO
// ======================
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
        if(d.ok){
            alert("Cadastrado!");
        } else alert(d.msg);
    })
}

// ======================
// ENTRAR
// ======================
function entrarJogo(saldo){
    document.getElementById("login").style.display="none";
    document.getElementById("game").style.display="block";
    document.getElementById("saldo").innerText="Saldo: "+saldo;

    bgMusic.play().catch(()=>{});
}

// ======================
// LOGOUT
// ======================
function logout(){
    localStorage.removeItem("user");
    user = null;
    document.getElementById("game").style.display="none";
    document.getElementById("login").style.display="block";
    bgMusic.pause();
}

// ======================
// 🎰 ANIMAÇÃO REAL
// ======================
function animarSlots(callback){
    let slots = ["s1","s2","s3"];
    let rodadas = 20;
    let delay = 50;

    function loop(){
        if(rodadas > 0){
            slots.forEach(id=>{
                document.getElementById(id).innerText =
                    ["🍵","🌰","🐂","⭐","🍊"][Math.floor(Math.random()*5)];
            });

            rodadas--;
            delay += 8; // desacelera

            setTimeout(loop, delay);
        } else {
            callback();
        }
    }

    loop();
}

// ======================
// SPIN
// ======================
function spin(){
    spinSound.currentTime = 0;
    spinSound.play();

    animarSlots(() => {
        fetch("/spin",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({user:user})
        })
        .then(r=>r.json())
        .then(d=>{
            if(!d.ok){
                alert(d.msg);
                return;
            }

            document.getElementById("s1").innerText=d.r[0];
            document.getElementById("s2").innerText=d.r[1];
            document.getElementById("s3").innerText=d.r[2];

            document.getElementById("saldo").innerText="Saldo: "+d.saldo;

            if(d.premio > 0){
                winSound.currentTime = 0;
                winSound.play();
                document.getElementById("msg").innerText="🎉 Ganhou "+d.premio;
            } else {
                document.getElementById("msg").innerText="😢 Nada";
            }
        });
    });
}

// ======================
// 🔊 VOLUME (CORRIGIDO)
// ======================
function setVolume(v){
    bgMusic.volume = v;
    spinSound.volume = v;
    winSound.volume = v;

    localStorage.setItem("volume", v);
}

// ======================
// 🔇 MUTE (CORRIGIDO)
// ======================
function toggleMute(){
    muted = !muted;

    bgMusic.muted = muted;
    spinSound.muted = muted;
    winSound.muted = muted;

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
    })
}