// src/services/auth.js
const API_BASE_URL = 'http://127.0.0.1:8000';
export async function login(username, password) {
  console.log("Login Data:", { username, password }); // Add this line for debugging

  try {
    const response = await fetch(`${API_BASE_URL}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('token', data.token);
      localStorage.setItem('username', data.username);
      return true;
    } else {
      const errorData = await response.json();
      throw new Error(extractErrorMessage(errorData));
    }
  } catch (error) {
    throw new Error(error.message);
  }
}

export function isAuthenticated() {
  return !!localStorage.getItem('token');
}

// Helper function to extract error messages from the backend
function extractErrorMessage(errorData) {
  if (typeof errorData === 'string') return errorData;
  if (errorData.non_field_errors) return errorData.non_field_errors[0];
  if (errorData.detail) return errorData.detail;
  if (Array.isArray(errorData)) return errorData.map(item => item[0]).join(', ');
  if (errorData.status_code && errorData.non_field_errors) {
    return errorData.non_field_errors.join(', ');
  }
  return 'An unknown error occurred';
}




export async function register(username, email, password, firstName, lastName) {
  try {
      const response = await fetch(`${API_BASE_URL}/auth/registration/`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username, email, password1: password, password2: password, first_name: firstName, last_name: lastName }), 
      });


    if (response.ok) {
      return true;
    } else {
      const errorData = await response.json();
      throw new Error(extractErrorMessage(errorData) || 'Registration failed');
    }
  } catch (error) {
    throw new Error('Network error or registration failed: ' + error.message);
  }
}



export function logout() {
  localStorage.removeItem('token');
  localStorage.removeItem('username');
}
