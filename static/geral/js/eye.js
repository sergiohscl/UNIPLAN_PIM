document.addEventListener('DOMContentLoaded', function () {
    const togglePassword = document.querySelector('#togglePassword');
    const passwordField = document.querySelector('#idSenhaLogin');
  
    if (togglePassword && passwordField) {
      togglePassword.addEventListener('click', function () {
        // Alterna o tipo de input entre 'password' e 'text'
        const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordField.setAttribute('type', type);
  
        // Alterna o ícone entre o olho aberto e fechado
        this.querySelector('i').classList.toggle('fa-eye-slash');
      });
    }
  });

  document.getElementById('togglePassword1').addEventListener('click', function (e) {
    const passwordField = document.getElementById('id_password');
    const icon = this.querySelector('i');
    
    // Toggle password visibility
    const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordField.setAttribute('type', type);
    
    // Toggle icon
    icon.classList.toggle('bi-eye');
    icon.classList.toggle('bi-eye-slash');
});

document.getElementById('togglePassword2').addEventListener('click', function (e) {
    const passwordField = document.getElementById('id_confirm_password');
    const icon = this.querySelector('i');
    
    // Toggle password visibility
    const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordField.setAttribute('type', type);
    
    // Toggle icon
    icon.classList.toggle('bi-eye');
    icon.classList.toggle('bi-eye-slash');
});
