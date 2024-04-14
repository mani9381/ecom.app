// const signUpForm = document.getElementById('signUpForm');
// const signInForm = document.getElementById('signInForm');
const signUpContainer = document.querySelector('.sign-up');
const signInContainer = document.querySelector('.sign-in');
const switchButtons = document.querySelectorAll('.switch-btn');

// signUpForm.addEventListener('submit', function(event) {
//   event.preventDefault();
//   const username = document.getElementById('signUpUsername').value;
//   const email = document.getElementById('signUpEmail').value;
//   const password = document.getElementById('signUpPassword').value;
//   console.log('Sign Up:', username, email, password);
// });

// signInForm.addEventListener('submit', function(event) {
//   event.preventDefault();
//   const email = document.getElementById('signInEmail').value;
//   const password = document.getElementById('signInPassword').value;
//   console.log('Sign In:', email, password);
// });

switchButtons.forEach(button => {
  button.addEventListener('click', function() {
    const target = this.dataset.target;
    signUpContainer.classList.remove('active');
    signInContainer.classList.remove('active');
    document.querySelector(`.${target}`).classList.add('active');
    switchButtons.forEach(btn => btn.classList.remove('active'));
    this.classList.add('active');
  });
});