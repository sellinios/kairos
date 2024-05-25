// src/components/ArticleDetail/ArticleDetail.tsx
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';

interface Article {
  id: number;
  slug: string;
  title: string;
  content: string;
  author: string;
  created_at: string;
  updated_at: string;
}

const ArticleDetail: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();  // Use slug instead of id
  const [article, setArticle] = useState<Article | null>(null);

  useEffect(() => {
    const fetchArticle = async () => {
      try {
        const response = await axios.get(`/api/articles/${slug}/`);  // Fetch using slug
        setArticle(response.data);
      } catch (error) {
        console.error('Error fetching the article:', error);
      }
    };

    fetchArticle();
  }, [slug]);

  if (!article) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>{article.title}</h1>
      <div dangerouslySetInnerHTML={{ __html: article.content }} /> {/* Render HTML content */}
      <p>Author: {article.author}</p>
      <p>Published on: {new Date(article.created_at).toLocaleDateString()}</p>
    </div>
  );
};

export default ArticleDetail;
