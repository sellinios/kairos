import axios from 'axios';

const BASE_URL = process.env.REACT_APP_API_URL;

interface Article {
  id: number;
  slug: string;
  title: string;
  content: string;
  author: string;
  image?: string;
  created_at: string;
  updated_at: string;
}

export const fetchArticle = async (slug: string, language: string = 'en'): Promise<Article> => {
  try {
    const response = await axios.get<Article>(`${BASE_URL}/api/articles/${slug}/?language=${language}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching article with slug ${slug} in language ${language}:`, error);
    throw error;
  }
};

export const fetchLatestArticles = async (language: string): Promise<Article[]> => {
  try {
    const response = await axios.get<Article[]>(`${BASE_URL}/api/articles/latest/?language=${language}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching the latest articles:', error);
    throw error;
  }
};
