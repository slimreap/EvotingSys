const passwordError = document.getElementById('passwordSignUp');
const errorpop = document.querySelector('.error');
const registered = document.querySelector('.registered');
const signUpForm = document.getElementById('sign-form-2');
const btnReg = document.getElementById('btn-register');
const btnLogin = document.getElementById('btn-login');
const redirecting = document.querySelector('.redirecting');


btnReg.addEventListener('click', ()=> {

    if((passwordError.value).length < 8){
        setTimeout(() => {
            errorpop.classList.remove('hidden');
          }, 0000);
        setTimeout(() => {
            errorpop.classList.add('hidden');
          }, 3000); 
        } else {
        setTimeout(() => {
            registered.classList.remove('hidden');
          }, 0000);
        setTimeout(() => {
            registered.classList.add('hidden');
          }, 3000); 
          
        }
    })
    
    btnLogin.addEventListener('click', () => {
        setTimeout(() => {
            registered.classList.remove('hidden');
          }, 0000);
        setTimeout(() => {
            registered.classList.add('hidden');
          }, 3000); 
})