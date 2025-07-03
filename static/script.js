// // intro screen
// let intro = document.querySelector('.intro');
// let letter = document.querySelector('.welcome-header');
// let letterSpan = document.querySelectorAll('.letter');
// // let splashLogo = document.getElementById('pic')

// window.addEventListener('DOMContentLoaded', ()=>{

//     setTimeout(()=>{

//         letterSpan.forEach((span, idx)=>{
//             setTimeout(()=>{
//                 span.classList.add('active');
//             }, (idx + 1) * 400)
//         });

//         setTimeout(()=>{
//             letterSpan.forEach((span, idx) =>{
//                 setTimeout(()=>{
//                     span.classList.remove('active');
//                     span.classList.add('fade');
//                 },(idx + 1) * 50)
//             })
//         },2000)

//         // setTimeout(()=>{
//         //     splashLogo.classList.add('active');
//         // }, 2500)

//         setTimeout(()=>{
//             intro.style.top = '-100vh';
            
//         },2300)
//     })
// })

// // buttons
// document.getElementById("playSound").addEventListener("click", () => {
//   const beep = document.getElementById("beep");
//   beep.currentTime = 0;
//   beep.play();
// });

window.addEventListener('DOMContentLoaded', () => {
  let intro = document.querySelector('.intro');
  let letterSpan = document.querySelectorAll('.letter');

  setTimeout(() => {
    letterSpan.forEach((span, idx) => {
      setTimeout(() => {
        span.classList.add('active');
      }, (idx + 1) * 400);
    });

    setTimeout(() => {
      letterSpan.forEach((span, idx) => {
        setTimeout(() => {
          span.classList.remove('active');
          span.classList.add('fade');
        }, (idx + 1) * 50);
      });
    }, 2000);

    setTimeout(() => {
      intro.style.top = '-100vh';
    }, 2300);
  }, 100);
});
