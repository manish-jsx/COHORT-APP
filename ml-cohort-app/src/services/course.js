// src/services/course.js
const API_BASE_URL = 'http://127.0.0.1:8000'; 

export async function getAllCourses() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/courses/`);
    const data = await response.json();
    return data; // Return an array of course objects
  } catch (error) {
    throw error; 
  }
}

export async function getCourseDetails(courseId) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/courses/${courseId}/`);
    const data = await response.json();
    return data; // Return the course object
  } catch (error) {
    throw error; 
  }
}

export async function getEnrolledUsers(courseId) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/courses/${courseId}/enrolled_users/`);
    const data = await response.json();
    return data; // Return an array of user objects
  } catch (error) {
    throw error;
  }
}

export async function getModuleDetails(moduleId) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/modules/${moduleId}/`);
    const data = await response.json();
    return data; // Return the module object
  } catch (error) {
    throw error;
  }
}

// ... you can add more functions as needed (e.g., for notebooks)
