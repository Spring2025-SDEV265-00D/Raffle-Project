document.getElementById('loginForm').addEventListener('submit', async function(e) {
  e.preventDefault();
  const errorMessage = document.getElementById('errorMessage');
  errorMessage.textContent = '';

  try {
    const formData = new FormData(this);
    const response = await fetch(this.action, {
      method: 'POST',
      body: formData,
      credentials: 'include'
    });

    const data = await response.json();
    console.log('Login response:', data); // Debug log
    
    if (response.ok) {
      // Redirect based on role
      const role = data.role?.role || data.role; // Handle both nested and flat role structure
      console.log('User role:', role); // Debug log
      
      switch(role) {
        case 'Admin':
          window.location.href = '/admin/operations';
          break;
        case 'Cashier':
          window.location.href = '/ticket/info';
          break;
        default: // Seller
          window.location.href = '/event/selection';
      }
    } else {
      errorMessage.textContent = data.message || 'Login failed';
    }
  } catch (error) {
    console.error('Login error:', error); // Debug log
    errorMessage.textContent = 'An error occurred during login';
  }
}); 