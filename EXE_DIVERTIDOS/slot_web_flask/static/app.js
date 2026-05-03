let user = null;

function login(){
    fetch("/login",{
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
            user = document.getElementById("user").value;
            document.getElementById("login").style.display="none";
            document.getElementById("game").style.display="block";
            document.getElementById("saldo").innerText="Saldo: "+d.saldo;
        }else alert(d.msg);
    })
}

function spin(){
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
        document.getElementById("msg").innerText = d.premio>0 ? "🎉 Ganhou "+d.premio : "😢 Nada";
    })
}

function verRanking(){
    fetch("/ranking")
    .then(r=>r.json())
    .then(d=>{
        let txt="🏆 Ranking\n\n";
        d.forEach((u,i)=> txt+=(i+1)+". "+u[0]+" - "+u[1]+"\n");
        alert(txt);
    })
}