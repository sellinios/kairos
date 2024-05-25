// src/services/apiService.ts
import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL;

interface Article {
  id: number;  // Ensure id is always required
  slug: string;
  title: string;
  content: string;
  author: string;
  image: string;  // Include image field
}

interface Place {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
}

// Fetch the nearest place
export const fetchNearestPlace = async (latitude: number, longitude: number): Promise<Place> => {
  try {
    const response = await axios.get<Place>(`${BASE_URL}/api/places/nearest/`, {
      params: { latitude, longitude }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching nearest place:', error);
    throw error;
  }
};

// Fetch all articles
export const fetchArticles = async (): Promise<Article[]> => {
  try {
    const response = await axios.get<Article[]>(`${BASE_URL}/api/articles/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching articles:', error);
    throw error;
  }
};

// Fetch a single article by ID
export const fetchArticle = async (id: number): Promise<Article> => {
  try {
    const response = await axios.get<Article>(`${BASE_URL}/api/articles/${id}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching article with ID ${id}:`, error);
    throw error;
  }
};

// Fetch the latest article
export const fetchLatestArticle = async (): Promise<Article> => {
  try {
    const response = await axios.get<Article>(`${BASE_URL}/api/articles/latest/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching the latest article:', error);
    throw error;
  }
};

// Create a new article
export const createArticle = async (article: Partial<Article>): Promise<Article> => {
  try {
    const response = await axios.post<Article>(`${BASE_URL}/api/articles/`, article);
    return response.data;
  } catch (error) {
    console.error('Error creating article:', error);
    throw error;
  }
};

// Update an existing article
export const updateArticle = async (id: number, article: Partial<Article>): Promise<Article> => {
  try {
    const response = await axios.put<Article>(`${BASE_URL}/api/articles/${id}/`, article);
    return response.data;
  } catch (error) {
    console.error(`Error updating article with ID ${id}:`, error);
    throw error;
  }
};

// Delete an article
export const deleteArticle = async (id: number): Promise<void> => {
  try {
    await axios.delete(`${BASE_URL}/api/articles/${id}/`);
  } catch (error) {
    console.error(`Error deleting article with ID ${id}:`, error);
    throw error;
  }
};
