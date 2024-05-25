import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL;

interface Article {
  id: number;
  slug: string;
  title: string;
  content: string;
  author: string;
  image: string;
  created_at: string;
  updated_at: string;
}

// Fetch a single article by slug
export const fetchArticle = async (slug: string): Promise<Article> => {
  try {
    const response = await axios.get<Article>(`${BASE_URL}/api/articles/${slug}/`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching article with slug ${slug}:`, error);
    throw error;
  }
};

// Fetch the latest articles
export const fetchLatestArticles = async (): Promise<Article[]> => {
  try {
    const response = await axios.get<Article[]>(`${BASE_URL}/api/articles/latest/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching the latest articles:', error);
    throw error;
  }
};
